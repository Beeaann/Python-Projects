from datetime import datetime
import os
import pathlib
import sys
import tkinter
from tkinter import messagebox
import customtkinter
from PyPDF2 import PdfReader, PdfWriter
import threading

#os for directories
#pathlib also for directories
#tkinter for progressbar and gui
#PyPDF2 for pdf manipulation

#Once directory is saved, for loop iterates through and adds all pdfs with an account number in their name to a dictionary
#After that another for loop iterates through the dictionary keys and adds pages to the pdfwriter unless it is the page I want to remove.
#If statements are used to determine where to add the pages from. Main pages are pulled from the normal suit package, and it only pulls from the NMC file if certain pages in main file

def gui():
    # Main GUI window initialization
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("dark-blue")
    global root
    root = customtkinter.CTk()
    root.title("Suit Packager")
    root.geometry("300x250")
    root.resizable(width=False, height=False)

    # Progress bar initialization
    global my_progress, my_buttonCity, num_entry
    my_progress = customtkinter.CTkProgressBar(root, width=215, mode="determinate")   
    global my_status, my_button2, num, my_status2
    main_text = customtkinter.CTkLabel(root, text ="  NMC TO PACKAGE", font=('Arial',18,'bold'), width=2)
    main_text.pack()

    # "Start merge" button initialization
    my_buttonCity = customtkinter.CTkButton(root, text="Start Merge", command=threading.Thread(target=process).start)
    my_buttonCity.pack(side="bottom", pady= 10)
    num = customtkinter.StringVar()
    num_entry = customtkinter.CTkEntry(root,textvariable=num, font=('calibre',10,'normal'))
    num_entry.pack(side="bottom", pady=10)
    my_buttonCity.pack(side="bottom", pady= 10)
    # "Merging Files" text displayed below progress bar initialization
    my_status = customtkinter.CTkLabel(root, text="Merging Files...")
    my_status2 = customtkinter.CTkLabel(root, text="Enter the NMC Page Number:")
    # "Finish" button initialization
    my_button2 = customtkinter.CTkButton(root, text="Finish",command=root.destroy)
    my_status2.pack(pady=20)
    
def process():
    endNum = int(num.get())
    startNum = endNum - 1
    
    # Set the directory path where to find the PDFs to merge
    cwd = os.getcwd()

    # Define input directory for the pdf files
    try:
        pdf_dir = tkinter.filedialog.askdirectory(title="Select a folder", initialdir=cwd)
    except Exception as error:
        print("ERROR CHOOSING DIRECTIORY: ", error)
        
    #initialize gui
    num_entry.destroy()
    my_buttonCity.destroy()
    my_progress.pack(pady=20)
    my_status2.destroy()
    my_status.pack(pady=20)
    root.update()

    # Define & create output directory
    output_folder_name = "Output_folder"
    pdf_output_dir = pathlib.Path(pdf_dir) / output_folder_name
    pdf_output_dir.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    time = now.time()
    date = now.date()
    sys.stdout = open(f"{pdf_output_dir}\\Console({date}).txt", 'w')
    print("Date: ", date)
    print("Time: ", time)
    print("output_folder - ", pdf_output_dir)
    start = True     
    # Get all the PDF files in the directory
    pdf_files = os.listdir(pdf_dir)
    pdf_files = ([file for file in pdf_files if file.endswith('.pdf') or file.endswith('.PDF')])
    
    for file in pdf_files:
        for letter in file:
            if letter == ' ' or letter == '  ':
                start = False
                break
    
    if start == False:
        messagebox.showinfo('Error', 'No spaces in PDF names!')
    
    if start:
        # Create a dictionary with first 10 characters of pdf names as keys and pdf names as values
        try:
            pdf_dict = {}
            for pdf_file in pdf_files:
                key = pdf_file[:10]
                if key not in pdf_dict:
                    pdf_dict[key] = [pdf_file]
                else:
                    pdf_dict[key].append(pdf_file)
                    
        except Exception as error:
            print(f"ERROR CREATING DICTIONARY: {error}")
            
        counter = 0
        for pdf_file in pdf_dict:
            counter += 1
        myValue = 1 / counter   
        print("PDF Dictionary: ")
        print(pdf_dict)
        skip = False
        for key in pdf_dict:
            if len(pdf_dict[key]) <= 10:
                
                print("Reading: ", pdf_dict[key])
                input_path = os.path.join(pdf_dir, f"{key}.pdf")
                input_pdf = PdfReader(open(input_path, "rb"))
                output_path = os.path.join(pdf_output_dir, f"{key}.pdf")
                writer = PdfWriter()
                skip = False
                for i in range(len(input_pdf.pages)):
                    
                    #removes whatever page that is set
                    if i != startNum and i != endNum:
                        page = input_pdf.pages[i]
                        writer.add_page(page)
                        
                    #adds the nmc pdf into whatever pages that are set    
                    elif i == startNum or i == endNum:
                        try:
                            if f"{key}_NMC.pdf" or f"{key}_NMC.PDF" in pdf_dict[key]:
                                nmcFile = os.path.join(pdf_dir, f"{key}_NMC.pdf")
                                nmc_obj = PdfReader(open(nmcFile, "rb"))
                                if i == startNum:
                                    nmcPage = nmc_obj.pages[0]
                                elif i == endNum:
                                    nmcPage = nmc_obj.pages[1]
                                writer.add_page(nmcPage) 
                        except Exception as error:
                            skip = True
                try:
                    if skip == False:
                        print(f"Writing {pdf_dict[key]} to Output Path")       
                        writer.write(open(output_path, "wb"))
                    else:
                        messagebox.showinfo('Error', f'Error: No NMC File Found for {key}.  Double Check NMC File!')
                except:
                    print(f"ERROR, COULD NOT WRITE {pdf_dict[key]} TO OUTPUT FOLDER")
                my_progress.set(myValue)
                myValue += myValue
                my_progress.update()
    
        
    my_progress.set(100)
    my_status.destroy()
    my_button2.pack(side="bottom", pady= 30)
    root.update()
    sys.stdout.close()

gui()
root.mainloop()
