from io import BytesIO
import os
import sys
from tkinter import messagebox
import customtkinter as ctk
from PIL import Image
import mysql.connector
import bcrypt
import re

class Gui(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title('Test Program')
        window_width = 350
        window_height = 350
        
        #Gets the screen resolution for measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate - 100))
        self.resizable(False, False)
        
        #Adds image to login window
        datafile2 = "twitterbird.png"
        if not hasattr(sys, "frozen"):
            datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
        else:
            datafile2 = os.path.join(sys.prefix, datafile2)
        image= ctk.CTkImage(Image.open(datafile2), size=(80,80))
        self.img_label = ctk.CTkLabel(self, image=image, text="")
        self.img_label.pack(pady=15)
        
        #Username entry label
        self.text1 = ctk.CTkLabel(self, text='Username: ')
        self.text1.pack(pady=5)
        
        #username entrybox
        self.usernameVar = ctk.StringVar()
        self.usernameEntry = ctk.CTkEntry(self, textvariable=self.usernameVar)
        self.usernameEntry.pack(pady=5)
        
        #password entry label
        self.text2 = ctk.CTkLabel(self, text='Password: ')
        self.text2.pack(pady=5)
        
        #password entrybox
        self.passwordVar = ctk.StringVar()
        self.passwordEntry = ctk.CTkEntry(self, textvariable=self.passwordVar, show='*')
        self.passwordEntry.pack(pady=5)
        
        #create account button
        self.button1 = ctk.CTkButton(self, text='Create Account', command=self.createAccount, width=30, height=20)
        self.button1.pack(side='bottom', pady=5)
        
        #login button
        self.button2 = ctk.CTkButton(self, text='Login', command=self.checkAccount)
        self.button2.pack(side='bottom', pady=5)
        
        #modified in
        self.text3 = ctk.CTkLabel(self, text='Incorrect Login')
        
        self.db = mysql.connector.connect(
            host="",
            user="",
            passwd="",
            database=""
        )
        
        self.toplevel_window = None

    def checkAccount(self):
        accessGranted = False
        self.username = self.usernameVar.get()
        password = self.passwordVar.get()

        mycursor = self.db.cursor(buffered=True)

        # Check if the table exists
        mycursor.execute("SHOW TABLES LIKE 'user'")
        table_exists = mycursor.fetchone() is not None

        if table_exists:
            # Fetch the user by username
            mycursor.execute("SELECT * FROM user WHERE name = %s", (self.username,))
            user = mycursor.fetchone()

            if user is not None:
                hashed_password = user[mycursor.column_names.index("password")]

                # Verify the password
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    try:
                        self.text3.destroy()
                    except:
                        pass

                    print("Login successful!")
                    accessGranted = True
                else:
                    self.text3.pack(side='bottom', pady=5)
                    print("Login failed!")
            else:
                messagebox.showinfo('My App', 'Username not found!')

        # Move to the next result set if available
        if mycursor.nextset():
            pass

        mycursor.close()

        if accessGranted:
            self.open_toplevel()
            self.withdraw()

    def createAccount(self):
        # Get variables from entry boxes
        self.username = self.usernameVar.get()
        password = self.passwordVar.get()

        # Input validation
        if not re.match(r'^[a-zA-Z0-9_]+$', self.username):
            self.text3.configure(text='Invalid username format!')
            self.text3.pack(side='bottom')
            return
        
        # Input validation
        if len(self.username) > 20:
            self.text3.configure(text='Username cannot be more than 20 characters!')
            self.text3.pack(side='bottom')
            return
        
        # Input validation
        if len(password) < 8:
            self.text3.configure(text='Password must be at least 8 characters!')
            self.text3.pack(side='bottom')
            return
        
        # Input validation
        if len(password) > 50:
            self.text3.configure(text='Password cannot be more than 50 characters!')
            self.text3.pack(side='bottom')
            return

        contains_upper_case = any([letter.isupper() for letter in password])
        
        # Input validation
        if not contains_upper_case:
            self.text3.configure(text='Must contain atleast one uppercase character!')
            self.text3.pack(side='bottom')
            return
            
        
        mycursor = self.db.cursor(buffered=True)

        #Verifies whether username is taken
        mycursor.execute("SELECT * FROM user WHERE name = %s", (self. username,))
        matchingLogin = mycursor.fetchone()

        # Create new entry into table
        if matchingLogin is None:
            # Hash the password
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            #inserts username and password into user database
            mycursor.execute("INSERT INTO user (name, password) VALUES (%s, %s)", (self.username, hashed_password))
            self.db.commit()

            self.text3.configure(text='Account Created!')
            self.text3.pack(side='bottom')

            #opens main application window and closes login window
            self.open_toplevel()
            self.withdraw()
        else:
            self.text3.configure(text='Username already exists!')
            self.text3.pack(side='bottom')

        # Move to the next result set if available
        if mycursor.nextset():
            pass

        mycursor.close()
        
    def open_toplevel(self):
        #Open toplevel window if none already open
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = MainWindow(self, self.username, self.db) # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it
        
class MainWindow(ctk.CTkToplevel):
    def __init__(self, parent, username, db):
        super().__init__(parent)
        self.username = username
        self.db = db
        self.parent = parent
        
        self.title('Main Window')
        window_width = 800
        window_height = 600
        
        #Gets the screen resolution for measurements
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Coordinates of the upper left corner of the window to make the window appear in the center
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        self.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate - 100))
        #self.resizable(False, False)
        self.mainWindowGui()
        
    def mainWindowGui(self):
        
        usernameLabel = ctk.CTkLabel(self, text=f'Welcome {self.username}!', width=30, height=30)
        usernameLabel.pack()
        
        tabview = ctk.CTkTabview(self)
        tabview.pack(expand=True, fill='both')
        
        #creates tabs on the main window
        self.mainTab = tabview.add('Main')
        self.profileTab = tabview.add('Profile')
        self.tweetTab = tabview.add('Tweet')
        self.settingTab = tabview.add('Settings')
        
        #Update User information
        self.retrieveUserData()
        self.setMainTab()
        self.setProfileTab()
        self.setTweetTab()
        self.setSettingTab()
        
        # Handle window close event
        self.protocol("WM_DELETE_WINDOW", self.on_window_close)
    
    def setMainTab(self):
        #Creates a frame to store all tweets
        self.mainFrame = ctk.CTkScrollableFrame(self.mainTab)
        self.mainFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        mainLabel = ctk.CTkLabel(self.mainFrame, text=f'Main Feed', font=('Ariel',25))
        mainLabel.pack(side='top', anchor='w', pady=5, padx=5, fill="both", expand=True)
        
        #Calls all user tweets from database
        self.retrieveAllTweets()
    
    def setProfileTab(self):
        self.profileFrame = ctk.CTkScrollableFrame(self.profileTab)
        self.profileFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        #If user has a profile picture then use it, otherwise default image
        if self.profilePicture:
            profile_image_stream = BytesIO(self.profile_picture)
            profile_image = ctk.CTkImage(Image.open(profile_image_stream), size=(80,80))
            profileImagelabel = ctk.CTkLabel(self.profileFrame, image=profile_image, text="")
            profileImagelabel.pack(side='top', anchor='w', pady=5, padx=5)
            
        else:
            datafile2 = "defaultImage.png"
            if not hasattr(sys, "frozen"):
                datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
            else:
                datafile2 = os.path.join(sys.prefix, datafile2)
            image= ctk.CTkImage(Image.open(datafile2), size=(80,80))
            imagelabel = ctk.CTkLabel(self.profileFrame, image=image, text="")
            imagelabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        yourProfileUsernameLabel = ctk.CTkLabel(self.profileFrame, text=self.username, font=('Ariel',20))
        yourProfileUsernameLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        profileTabs = ctk.CTkTabview(self.profileFrame)
        profileTabs.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.profileAbout = profileTabs.add('About')
        self.profileTweets = profileTabs.add('Tweets')
        self.profileReplies = profileTabs.add('Replies')
        
        #-----------------ABOUT TAB-----------------
        self.aboutFrame = ctk.CTkFrame(self.profileAbout)
        self.aboutFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        aboutLabel = ctk.CTkLabel(self.aboutFrame, text=f'About', font=('Ariel',25))
        aboutLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        #----------------USER TWEETS TAB------------
        yourTweetsLabel = ctk.CTkLabel(self.profileTweets, text=f'Your Tweets', font=('Ariel',25))
        yourTweetsLabel.pack(side='top', anchor='w', pady=5, padx=5, fill="both", expand=True)
        
        self.retrieveUserTweets()
        
        #----------------REPLIES TAB----------------
        self.receiveUserReplies()
    
    def setTweetTab(self):
        #----------------Tweet Page-----------------
        self.tweetFrame = ctk.CTkFrame(self.tweetTab)
        self.tweetFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        # 800 x 600 window
        
        #blankspace
        blankspace = ctk.CTkLabel(self.tweetFrame,text='')
        blankspace.grid(row=0,column=0)
        
        #If user has a profile picture then use it, otherwise default image
        if self.profilePicture:
            profile_image_stream = BytesIO(self.profile_picture)
            profile_image = ctk.CTkImage(Image.open(profile_image_stream), size=(80,80))
            self.settingImagelabel = ctk.CTkLabel(self.tweetFrame, image=profile_image, text="")
            self.settingImagelabel.grid(row=1, column=0, pady=10)
            
        else:
            datafile2 = "defaultImage.png"
            if not hasattr(sys, "frozen"):
                datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
            else:
                datafile2 = os.path.join(sys.prefix, datafile2)
            image= ctk.CTkImage(Image.open(datafile2), size=(80,80))
            self.tweetImagelabel = ctk.CTkLabel(self.tweetFrame, image=image, text="")
            self.tweetImagelabel.grid(row=1, column=0, pady=10)
        
        #Creates entry boxes and labels for user to input tweet
        self.author = self.username
        
        self.authorLabel = ctk.CTkLabel(self.tweetFrame, text=self.author, font=('Ariel',15))
        self.authorLabel.grid(row=1, column=1, pady=10)
        
        self.userMessageBox = ctk.CTkTextbox(self.tweetFrame, height=200, width=700)
        self.userMessageBox.grid(row=2, column=0, columnspan=20, pady=10, padx=10)
        
        self.sendTweetButton = ctk.CTkButton(self.tweetFrame, text='Send Tweet', command=self.sendTweet, width=50)
        self.sendTweetButton.grid(row=3, column=19)
    
    def setSettingTab(self):
        self.settingFrame = ctk.CTkScrollableFrame(self.settingTab)
        self.settingFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        #BASIC INFO TAB
        self.basicInfoFrame = ctk.CTkFrame(self.settingFrame)
        self.basicInfoFrame.pack(side='top', anchor='w', fill="both", expand=True, pady=5)
        
        #Basic info labels and entries
        basicInfoLabel = ctk.CTkLabel(self.basicInfoFrame, text=f'Basic info', font=('Ariel',25))
        basicInfoLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        pictureLabel = ctk.CTkLabel(self.basicInfoFrame, text='Profile Picture')
        pictureLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        if self.profilePicture:
            profile_image_stream = BytesIO(self.profile_picture)
            profile_image = ctk.CTkImage(Image.open(profile_image_stream), size=(80,80))
            self.settingImagelabel = ctk.CTkLabel(self.basicInfoFrame, image=profile_image, text="")
            self.settingImagelabel.pack(side='top', anchor='w', pady=5, padx=5)
            
        else:
            datafile2 = "defaultImage.png"
            if not hasattr(sys, "frozen"):
                datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
            else:
                datafile2 = os.path.join(sys.prefix, datafile2)
            image= ctk.CTkImage(Image.open(datafile2), size=(80,80))
            self.img_label = ctk.CTkLabel(self.basicInfoFrame, image=image, text="")
            self.img_label.pack(side='top', anchor='w', pady=5, padx=5)
        
        #allows someone to select an image for a profile picture
        changePictureButton = ctk.CTkButton(self.basicInfoFrame, text='Select', width=30, height=20, command=self.selectImage)
        changePictureButton.pack(side='top', anchor='w', pady=5, padx=5)
        
        nameLabel = ctk.CTkLabel(self.basicInfoFrame, text=f'Username')
        nameLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        usernameLabel = ctk.CTkLabel(self.basicInfoFrame, text=self.username, font=('Ariel',15))
        usernameLabel.pack(side='top', anchor='w', pady=5, padx=5)

        birthdayLabel = ctk.CTkLabel(self.basicInfoFrame, text=f'Birthday')
        birthdayLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.birthdayVar = ctk.StringVar()
        birthdayEntry = ctk.CTkEntry(self.basicInfoFrame, textvariable=self.birthdayVar)
        birthdayEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.birthdayVar.set(self.birthday)
        
        genderLabel = ctk.CTkLabel(self.basicInfoFrame, text=f'Gender')
        genderLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.genderVar = ctk.StringVar()
        genderEntry = ctk.CTkEntry(self.basicInfoFrame, textvariable=self.genderVar)
        genderEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.genderVar.set(self.gender)
        
        basicInfoUpdateButton = ctk.CTkButton(self.basicInfoFrame, text='Update', command=self.updateBasicInfo, width=30, height=20)
        basicInfoUpdateButton.pack(side='bottom', anchor='w', pady=10, padx=5)
    
        #CONTACT INFO TAB
        self.contactInfoFrame = ctk.CTkFrame(self.settingFrame)
        self.contactInfoFrame.pack(side='top', anchor='w', fill="both", expand=True, pady=5, padx=5)
        
        #contact info labels and entries
        contactInfoLabel = ctk.CTkLabel(self.contactInfoFrame, text=f'Contact info', font=('Ariel',25))
        contactInfoLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        emailLabel = ctk.CTkLabel(self.contactInfoFrame, text=f'Email')
        emailLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.emailVar = ctk.StringVar()
        emailEntry = ctk.CTkEntry(self.contactInfoFrame, textvariable=self.emailVar)
        emailEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.emailVar.set(self.email)

        phoneNumberLabel = ctk.CTkLabel(self.contactInfoFrame, text=f'Phone Number')
        phoneNumberLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.phoneNumberVar = ctk.StringVar()
        phoneNumberEntry = ctk.CTkEntry(self.contactInfoFrame, textvariable=self.phoneNumberVar)
        phoneNumberEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.phoneNumberVar.set(self.phone_number)
        
        contactInfoUpdateButton = ctk.CTkButton(self.contactInfoFrame, text='Update', command=self.updateContactInfo, width=30, height=20)
        contactInfoUpdateButton.pack(side='bottom', anchor='w', pady=10, padx=5)
        
        #ADDRESS
        self.addressInfoFrame = ctk.CTkFrame(self.settingFrame)
        self.addressInfoFrame.pack(side='top', anchor='w', fill="both", expand=True, pady=5, padx=5)
        
        #address info labels and entries
        addressInfoLabel = ctk.CTkLabel(self.addressInfoFrame, text=f'Address info', font=('Ariel',25))
        addressInfoLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        homeAddressLabel = ctk.CTkLabel(self.addressInfoFrame, text=f'Home')
        homeAddressLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.homeVar = ctk.StringVar()
        homeAddressEntry = ctk.CTkEntry(self.addressInfoFrame, textvariable=self.homeVar)
        homeAddressEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.homeVar.set(self.home_address)
        
        workAddressLabel = ctk.CTkLabel(self.addressInfoFrame, text=f'Work')
        workAddressLabel.pack(side='top', anchor='w', pady=5, padx=5)
        
        self.workVar = ctk.StringVar()
        workAddressEntry = ctk.CTkEntry(self.addressInfoFrame, textvariable=self.workVar)
        workAddressEntry.pack(side='top', anchor='w', pady=5, padx=5)
        self.workVar.set(self.work_address)
        
        addressInfoUpdateButton = ctk.CTkButton(self.addressInfoFrame, text='Update', command=self.updateAddressInfo, width=30, height=20)
        addressInfoUpdateButton.pack(side='bottom', anchor='w', pady=10, padx=5)
    
    def retrieveUserData(self):
        # Create a cursor to execute SQL queries
        cursor = self.db.cursor()

        #Retrieve Profile Picture
        select_query = f"SELECT profile_picture FROM `user` WHERE name = '{self.username}'"
        cursor.execute(select_query)
        profile_picture = cursor.fetchone()
        self.profilePicture = True
        
        if profile_picture:
            self.profile_picture = profile_picture[0]
            print(f"{self.username}'s profile picture: {profile_picture[0]}")
            if profile_picture[0] == None or profile_picture[0] == 'None':
                self.profilePicture = False              
        
        # Retrieve user information for the "birthday" attribute for the logged-in user
        select_query = f"SELECT birthday FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        birthday = cursor.fetchone()
        if birthday:
            self.birthday = birthday[0]
            print(f"{self.username}'s birthday is on {birthday[0]}")

        # Retrieve user information for the "gender" attribute for the logged-in user
        select_query = f"SELECT gender FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        gender = cursor.fetchone()
        if gender:
            self.gender = gender[0]
            print(f"{self.username}'s gender is {gender[0]}")

        # Retrieve user information for the "email" attribute for the logged-in user
        select_query = f"SELECT email FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        email = cursor.fetchone()
        if email:
            self.email = email[0]
            print(f"{self.username}'s email is {email[0]}")

        # Retrieve user information for the "phone_number" attribute for the logged-in user
        select_query = f"SELECT phone_number FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        phone_number = cursor.fetchone()
        if phone_number:
            self.phone_number = phone_number[0]
            print(f"{self.username}'s phone number is {phone_number[0]}")

        # Retrieve user information for the "work_address" attribute for the logged-in user
        select_query = f"SELECT work_address FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        work_address = cursor.fetchone()
        if work_address:
            self.work_address = work_address[0]
            print(f"{self.username}'s work address is {work_address[0]}")

        # Retrieve user information for the "home_address" attribute for the logged-in user
        select_query = f"SELECT home_address FROM user WHERE name = '{self.username}'"
        cursor.execute(select_query)
        home_address = cursor.fetchone()
        if home_address:
            self.home_address = home_address[0]
            print(f"{self.username}'s home address is {home_address[0]}")

        # Close the cursor and connection
        cursor.close()        
    
    def selectImage(self):
        cwd = os.getcwd()
        self.image_path = ctk.filedialog.askopenfilename(title="Select an image", initialdir=cwd)
    
    def retrieveAllTweets(self):
        cursor = self.db.cursor()

        # Retrieve all tweets from the database
        query = "SELECT * FROM tweet"
        cursor.execute(query)

        # Fetch all the rows returned by the query
        tweets = cursor.fetchall()

        # Iterate over the retrieved tweets
        for tweet in reversed(tweets):
            # Access the tweet data as needed
            tweet_id = tweet[0]
            body = tweet[1]
            author = tweet[2]
            time = tweet[3]
            
            # Create a custom Tkinter frame for each tweet
            frame = ctk.CTkFrame(self.mainFrame, border_width=2, fg_color='#3a7ebf')
            frame.pack(padx=10, pady=10, side='top', anchor='w', expand=True, fill='x', ipadx=300)
            
            query = "SELECT profile_picture FROM user WHERE name = %s"
            values = (author,)
            cursor.execute(query, values)

            # Fetch the row returned by the query
            result = cursor.fetchone()
            hasPicture = True
            # Check if a profile picture was found
            if result:
                profile_picture = result[0]
                if profile_picture == None or profile_picture == 'None':
                    hasPicture = False
            
            if hasPicture:
                    profile_image_stream = BytesIO(profile_picture)
                    profile_image = ctk.CTkImage(Image.open(profile_image_stream), size=(50,50))
                    profileImageTweet = ctk.CTkLabel(frame, image=profile_image, text="")
                    profileImageTweet.grid(row=1, column=0, pady=10)
                    
            else:
                datafile2 = "defaultImage.png"
                if not hasattr(sys, "frozen"):
                    datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
                else:
                    datafile2 = os.path.join(sys.prefix, datafile2)
                image= ctk.CTkImage(Image.open(datafile2), size=(50,50))
                profileImageTweet = ctk.CTkLabel(frame, image=image, text="")
                profileImageTweet.grid(row=1, column=0, pady=10)
                
            # Create labels to display the tweet data within the frame
            author_label = ctk.CTkLabel(frame, text=f"{author}")
            author_label.grid(row=1, column=1, pady=10)
            
            body_label = ctk.CTkLabel(frame, text=f"{body}")
            body_label.grid(row=2, column=0, columnspan=20, pady=10, padx=10)

        # Close the cursor and database connection
        cursor.close()
    
    def retrieveUserTweets(self):
        cursor = self.db.cursor()

        # Set the username
        username = self.username

        # Retrieve all tweets by the specified username
        query = "SELECT * FROM tweet WHERE author = %s"
        values = (username,)
        cursor.execute(query, values)

        # Fetch all the rows returned by the query
        tweets = cursor.fetchall()

        # Iterate over the retrieved tweets
        for tweet in reversed(tweets):
            # Access the tweet data as needed
            tweet_id = tweet[0]
            body = tweet[1]
            author = tweet[2]
            time = tweet[3]
            
            # Create a custom Tkinter frame for each tweet
            frame = ctk.CTkFrame(self.profileTweets, border_width=2, fg_color='#3a7ebf')
            frame.pack(padx=10, pady=10, side='top', anchor='w', expand=True, fill='x', ipadx=300)
            
            if self.profilePicture:
                profile_image_stream = BytesIO(self.profile_picture)
                profile_image = ctk.CTkImage(Image.open(profile_image_stream), size=(50,50))
                profileImageTweet = ctk.CTkLabel(frame, image=profile_image, text="")
                profileImageTweet.grid(row=1, column=0, pady=10)
                
            else:
                datafile2 = "defaultImage.png"
                if not hasattr(sys, "frozen"):
                    datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
                else:
                    datafile2 = os.path.join(sys.prefix, datafile2)
                image= ctk.CTkImage(Image.open(datafile2), size=(50,50))
                profileImageTweet = ctk.CTkLabel(frame, image=image, text="")
                profileImageTweet.grid(row=1, column=0, pady=10)
            
            # Create labels to display the tweet data within the frame
            author_label = ctk.CTkLabel(frame, text=f"{author}")
            author_label.grid(row=1, column=1, pady=10)
            
            body_label = ctk.CTkLabel(frame, text=f"{body}")
            body_label.grid(row=2, column=0, columnspan=20, pady=10, padx=10)
        

        # Close the cursor and database connection
        cursor.close()
    
    def receiveUserReplies(self):
        self.repliesFrame = ctk.CTkFrame(self.profileReplies)
        self.repliesFrame.pack(side='top', anchor='w', fill="both", expand=True)
        
        repliesLabel = ctk.CTkLabel(self.repliesFrame, text=f'Replies', font=('Ariel',25))
        repliesLabel.pack(side='top', anchor='w', pady=5, padx=5)
        print('user replies')
    
    def sendTweet(self):
        # Set the tweet author and body
        author = self.author
        tweet_body = self.userMessageBox.get("1.0", "end")

        print(len(tweet_body))
        if len(tweet_body) > 280:
            messagebox.showinfo('My App', 'Cannot be over 280 characters!')
            return
        
        # Create a cursor object to interact with the database
        cursor = self.db.cursor()

        # Write the tweet data to the database
        query = "INSERT INTO tweet (author, content) VALUES (%s, %s)"
        values = (author, tweet_body)
        cursor.execute(query, values)

        # Commit the changes to the database
        self.db.commit()

        # Close the cursor
        cursor.close()
        messagebox.showinfo('My App', 'Tweet Sent!')
        self.userMessageBox.delete("0.0", "end")
        
        try:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.mainWindowGui()
        except:
            print('Refresh Failed')        
        
    def updateBasicInfo(self):
        cursor = self.db.cursor()
        
        try:
            #update profile picture
            with open(self.image_path, 'rb') as file:
                image_data = file.read()
            update_query = f"UPDATE user SET profile_picture = %s WHERE name = '{self.username}'"
            cursor.execute(update_query, (image_data,))   
        except:
            print('Not Changing Profile Picture') 
        
        try:
            # Update the "birthday" attribute for the user specified by self.username
            update_query = f"UPDATE user SET birthday = '{self.birthdayVar.get()}' WHERE name = '{self.username}'"
            cursor.execute(update_query)
        except:
            ('Not changing birthday')
            
        try:
            # Update the "gender" attribute for the user specified by self.username
            update_query = f"UPDATE user SET gender = '{self.genderVar.get()}' WHERE name = '{self.username}'"
            cursor.execute(update_query)
        except:
            print('Not changing gender')

        # Commit the changes to the database
        self.db.commit()

        # Close the cursor and connection
        cursor.close()
        messagebox.showinfo('My App', 'Basic Information Updated!')
        
        try:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.mainWindowGui()
        except:
            print('Refresh Failed')    
    
    def updateContactInfo(self):
        # Create a cursor to execute SQL queries
        cursor = self.db.cursor()

        # Update the "email" attribute for the user specified by self.username
        update_query = f"UPDATE user SET email = '{self.emailVar.get()}' WHERE name = '{self.username}'"
        cursor.execute(update_query)

        # Update the "phone_number" attribute for the user specified by self.username
        update_query = f"UPDATE user SET phone_number = '{self.phoneNumberVar.get()}' WHERE name = '{self.username}'"
        cursor.execute(update_query)

        # Commit the changes to the database
        self.db.commit()

        # Close the cursor and connection
        cursor.close()
        messagebox.showinfo('My App', 'Contact Information Updated!')
        
        try:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.mainWindowGui()
        except:
            print('Refresh Failed')    
        
    def updateAddressInfo(self):
        # Create a cursor to execute SQL queries
        cursor = self.db.cursor()

        # Update the "home_address" attribute for the user specified by self.username
        update_query = f"UPDATE user SET home_address = '{self.homeVar.get()}' WHERE name = '{self.username}'"
        cursor.execute(update_query)

        # Update the "work_address" attribute for the user specified by self.username
        update_query = f"UPDATE user SET work_address = '{self.workVar.get()}' WHERE name = '{self.username}'"
        cursor.execute(update_query)

        # Commit the changes to the database
        self.db.commit()

        # Close the cursor and connection
        cursor.close()
        messagebox.showinfo('My App', 'Address Information Updated!')
        
        try:
            for widgets in self.winfo_children():
                widgets.destroy()
            self.mainWindowGui()
        except:
            print('Refresh Failed')    
    
    def on_window_close(self):
        self.db.close()
        self.parent.destroy()

root = Gui()
root.mainloop()