from datetime import datetime
from pathlib import Path
import pathlib
import customtkinter as ctk
import pandas as pd
import os
import sys
from PIL import Image
import threading

#from datetime import datetime  *Used to get Date
#from pathlib import Path *Used to get Path from current directory
#import pathlib *used to get Path from current directory
#import customtkinter as ctk  *used to make GUI
#import pandas as pd *used to read and manipulate Excel File
#import os #used to get CWD
#import sys #used to get image, textfile, path
#rom PIL import Image *used for image on GUI

#Creates main window
def gui():
    global root, textbox, progress, button1
    ctk.set_appearance_mode("Dark") #darkmode
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk() 
    root.title("Routing Database")
    root.resizable(False, False)
    window_width = 550
    window_height = 550

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
        # Coordinates of the upper left corner of the window to make the window appear in the center
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    root.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))
    
    mainFrame = ctk.CTkFrame(root)
        
    datafile2 = "logo.png" #image name
    if not hasattr(sys, "frozen"):
        datafile2 = os.path.join(os.path.dirname(__file__), datafile2)
    else:
        datafile2 = os.path.join(sys.prefix, datafile2)
    image= ctk.CTkImage(Image.open(datafile2), size=(150,115))
    img_label = ctk.CTkLabel(root, image=image, text="")
    img_label.pack()
    
    mainFrame.pack(side="top", fill="both", expand=True, padx=25, pady=25)
    
    progress = ctk.CTkProgressBar(mainFrame, mode="indeterminate", width=425)
    
    textbox = ctk.CTkTextbox(mainFrame, width=450, height=300)
    textbox.pack(pady=5)
    textbox.insert(ctk.END, f"Instructions: \n")
    textbox.insert(ctk.END, f"1. Hit Start Process\n")
    textbox.insert(ctk.END, f"2. Select the Database\n")
    textbox.insert(ctk.END, f"3. Select the Routing File\n")
    textbox.configure(state="disabled")
    
    button1 = ctk.CTkButton(mainFrame, command=threading.Thread(target=main).start, text="Start Process", width=140)
    button1.pack(pady= 5, side="bottom") 

def addToExcel(database, searchExcel):
    now = datetime.now() #gets date
    date = now.date()
    
    #Reading database file and routing number excel file
    database = pd.read_excel(database, dtype='str')
    searchExcel = pd.read_excel(searchExcel, dtype='str')
    
    #Adding different columns for future data
    searchExcel['BankName'] = ''
    searchExcel['PhoneNumber'] = ''
    searchExcel['Address'] = ''
    searchExcel['City'] = ''
    searchExcel['State'] = ''
    searchExcel['Zip'] = ''
    
    global notInDatabase
    #List for missing data output text file
    notInDatabase = []
    def find_match(value):
        textbox.update()
        if value in database["routing_number"].values:
            index = database.loc[database['routing_number'] == value].index[0]
            textbox.insert(ctk.END, f"Match Found: {value}\n")
            textbox.see("end")
            return (database.loc[index, 'biz_name'], database.loc[index, 'biz_phone'],database.loc[index, 'e_address'],
                    database.loc[index, 'e_city'],database.loc[index, 'e_state'],database.loc[index, 'e_zip_full'])
        else:
            textbox.insert(ctk.END, f"{value} not found in database\n")
            textbox.see("end")
            print(str(value))
            notInDatabase.append(value)
                
            return ('','','','','','')
        
    #Creates text file
    sys.stdout = open(f"{output_dir}\\Missing({date}).txt", 'w')    
    try:
        #writes excel file to output folder
        with pd.ExcelWriter(output) as writer:
                #uses Apply to add routing data
                searchExcel[['BankName', 'PhoneNumber','Address','City','State','Zip']] = searchExcel['RoutingNumber'].apply(find_match).apply(pd.Series)
                searchExcel.to_excel(writer, index=False)
                worksheet = writer.sheets['Sheet1']
                for idx, col in enumerate(searchExcel):  # loop through all columns
                    series = searchExcel[col]
                    max_len = max((series.astype(str).map(len).max(),len(str(series.name)))) + 1  
                    worksheet.set_column(idx, idx, max_len)   
    except Exception as error:
        print(error)        
    sys.stdout.close() 
    
def main():    
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    cwd = os.getcwd()
    
    database = ctk.filedialog.askopenfilename(title="Select the Database Excel File", initialdir=cwd)
    textbox.insert(ctk.END, f"Database Selected: {database}\n")
    
    bankInfo = ctk.filedialog.askopenfilename(title="Select the Routing Number Excel File", initialdir=cwd)  
    textbox.insert(ctk.END, f"Routing Num Excel: {bankInfo}\n")
    
    if database.endswith(".csv") or database.endswith(".CSV") or bankInfo.endswith(".csv") or bankInfo.endswith(".CSV"):
        textbox.insert(ctk.END, f"Error: CSV Detected, File must be xlsx filetype\n")
    else:
        try:
            #Creates Output Folder
            global output_dir
            pathname = os.path.dirname(sys.argv[0])  
            output_folder_name = "output"
            output_dir = pathlib.Path(pathname) / output_folder_name
            output_dir.mkdir(parents=True, exist_ok=True)
        except Exception as error:
            print(error)
        
        button1.destroy()
        progress.pack()
        progress.start()
        root.update()
        global output
        fileName = "RoutingInfo.xlsx"
        output = Path(output_dir) / fileName 
        addToExcel(database, bankInfo)
        
        textbox.insert(ctk.END, f"Process Complete!\n")
        textbox.see("end")
        progress.stop()
    textbox.configure(state="disabled")

gui()
root.mainloop()