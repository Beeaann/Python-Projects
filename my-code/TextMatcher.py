from datetime import datetime
import pathlib
import customtkinter as ctk
import pandas as pd
import os
import sys
from PIL import Image
import threading
import re 

def gui():
    global root, textbox, mainFrame, button1, filetype, fileSelect
    ctk.set_appearance_mode("Dark") #darkmode
    ctk.set_default_color_theme("dark-blue")
    root = ctk.CTk() 
    root.title("Excel Word Search")
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
    
    textbox = ctk.CTkTextbox(mainFrame, width=450, height=300)
    textbox.pack(pady=5)
    textbox.insert(ctk.END, f"Instructions: \n")
    textbox.insert(ctk.END, f"1. Hit Start Process\n")
    textbox.insert(ctk.END, f"2. Select the Directory\n")
    
    textbox.configure(state="disabled")
    
    global progress
    progress = ctk.CTkProgressBar(mainFrame, mode="determinate", width=425)
    progress.set(0)
    
    button1 = ctk.CTkButton(mainFrame, command=threading.Thread(target=main).start, text="Start Process", width=140)
    button1.pack(pady= 5, side="bottom") 
    
    filetype = ctk.StringVar()
    fileSelect = ctk.CTkComboBox(mainFrame, values=['Single File', 'Multiple Files'], variable=filetype)
    filetype.set('Single File')
    fileSelect.pack()
    
def getSearchList():
    try:
        SearchExcel = pd.read_excel('searchwords.xlsx')
        searchWords = list(SearchExcel['SearchWords'])
        textbox.insert(ctk.END, f"Search Words:\n")
        
        for word in searchWords:
            if word == " ":
                searchWords.remove(word)
            elif word == "  ":
                searchWords.remove(word)
            elif word == "   ":
                searchWords.remove(word)
            elif word == "    ":
                searchWords.remove(word)
            elif word == None:
                searchWords.remove(word)
                
    except Exception as error:
        print(error)
        textbox.insert(ctk.END, f"Error: {error}\n")
    return searchWords

def applyHighlight(value):
    try:
        for word in searchList: 
            match = re.search(word, value, re.IGNORECASE)
            if match:
                print(f"word found: {word} in {value}")
                return 'background-color: #00FFFF'
        return ''
    except Exception as e:
        print(e)


def main():
    textbox.configure(state="normal")
    textbox.delete("0.0", "end")
    button1.destroy()
    selectedType = filetype.get()
    fileSelect.destroy()
    progress.pack(pady=20, side='bottom')
    root.update() 
    
    pathname = os.path.dirname(sys.argv[0])  
    output_folder_name = "output"
    output_dir = pathlib.Path(pathname) / output_folder_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    
    if selectedType == 'Single File':
        excel_dir = ctk.filedialog.askopenfile(title="Select the Excel File", initialdir=pathname)
        excel_files = [excel_dir]
        prog = 1
    elif selectedType == 'Multiple Files':   
        excel_dir= ctk.filedialog.askdirectory(title="Select the Excel Directory", initialdir=pathname)
        excel_files = ([f for f in os.listdir(excel_dir) if f.endswith(".xlsx") or f.endswith(".XLSX")])
        prog = 1 / len(excel_files)
    
    
    global searchList
    searchList = getSearchList()
    print(searchList)
    now = datetime.now() #gets date
    date = now.date()
    
    sys.stdout = open(f"{output_dir}\\searchWords({date}).txt", 'w')
    for file in excel_files:
        
        if file == 'searchwords.xlsx':
            print('skip')
            continue
        textbox.insert(ctk.END, f"Starting {file}!\n")
        print(f'Starting {file}!')
        
        if selectedType == 'Multiple Files':
            filePath = os.path.join(excel_dir, file)
            output_path = os.path.join(output_dir, file)
        elif selectedType == 'Single File':
            filePath = os.path.abspath(file.name)
            output_path = os.path.join(output_dir, os.path.basename(file.name))
                
        textbox.insert(ctk.END, f"{filePath}\n") 
        textbox.see("end")   
        excel_file = pd.read_excel(filePath)
        
        with pd.ExcelWriter(output_path) as writer:
            excel_file.style.applymap(applyHighlight)\
                .to_excel(writer, index=False)
            
            worksheet = writer.sheets['Sheet1']
            for idx, col in enumerate(excel_file):  # loop through all columns
                series = excel_file[col]
                max_len = max((series.astype(str).map(len).max(),len(str(series.name)))) + 1  
                worksheet.set_column(idx, idx, max_len)
        textbox.insert(ctk.END, f"{file} finished!\n")
        textbox.see("end")
        print(f"{file} finished!")
        progress.set(prog)
         
    textbox.insert(ctk.END, f"Process Complete!\n")    
    sys.stdout.close()             
    textbox.configure(state="disabled")
gui()
root.mainloop()