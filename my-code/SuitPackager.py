from datetime import datetime
import os
import pathlib
import sys
import tkinter
import customtkinter
from PyPDF2 import PdfMerger, PdfReader

def gui():
    # Main GUI window initialization
    customtkinter.set_appearance_mode("Dark")
    customtkinter.set_default_color_theme("dark-blue")
    global root
    root = customtkinter.CTk()
    root.title("Suit Packager")
    root.geometry("300x250")
    root.configure(bg='#D3D3D3')
    root.resizable(width=False, height=False)
    
    # Progress bar initialization
    global my_progress, my_button
    my_progress = customtkinter.CTkProgressBar(root, width=215, mode="determinate")   
    global my_status, my_button, my_button2
    main_text = customtkinter.CTkLabel(root, text ="  Suit Packager", font=('Arial',18,'bold'),width=2)
    main_text.pack()   
    
    # "Start merge" button initialization
    my_button = customtkinter.CTkButton(root, text="Start Merge", command=process)
    my_button.pack(side="bottom", pady= 30)
    
    # "Merging Files" text displayed below progress bar initialization
    my_status = customtkinter.CTkLabel(root, text="Merging Files...")
    
    # "Finish" button initialization
    my_button2 = customtkinter.CTkButton(root, text="Finish",command=root.destroy)

def process():
    # Set the directory path where to find the PDFs to merge
    cwd = os.getcwd()
    # Define input directory for the pdf files
    pdf_dir = tkinter.filedialog.askdirectory(title="Select a folder", initialdir=cwd)

    #initialize gui
    my_button.destroy()
    my_progress.pack(pady=20)
    my_status.pack(pady=20)
    root.update()

    # Define & create output directory
    output_folder_name = "Output_folder"
    pdf_output_dir = pathlib.Path(pdf_dir) / output_folder_name
    pdf_output_dir.mkdir(parents=True, exist_ok=True)

    # Get all the PDF files in the directory
    pdf_files = os.listdir(pdf_dir)
    now = datetime.now()
    time = now.time()
    date = now.date()
    sys.stdout = open(f"{pdf_output_dir}\\Console({date}).txt", 'w')
    print("Date: ", date)
    print("Time: ", time)
    print("output_folder - ", pdf_output_dir)
    print("PDFs in Directory: ", pdf_files)
    
    # Create lists for each category and sort them in order
    account_nums = sorted([pdf for pdf in pdf_files if "_" not in pdf])
    nmc_nums = sorted([pdf for pdf in pdf_files if "_NMC" in pdf])
    stm_nums = sorted([pdf for pdf in pdf_files if "_STM" in pdf])
    tnc_nums = sorted([pdf for pdf in pdf_files if "_TNC" in pdf])
    aff_nums = sorted([pdf for pdf in pdf_files if "_AFF" in pdf])
    
    # Concatenate the sorted lists into one list in the desired order
    sorted_pdf_files = account_nums + nmc_nums + stm_nums + tnc_nums + aff_nums
    print("Sorted PDF Files: ", sorted_pdf_files)
    
    #gather total count for progress bar
    totalProg = len(sorted_pdf_files)
    totalProg = 50 / totalProg
    
    # Create a dictionary with first 10 characters of pdf names as keys and pdf names as values
    pdf_dict = {}
    try:
        for pdf_file in sorted_pdf_files:
            key = pdf_file[:10]
            if key not in pdf_dict:
                pdf_dict[key] = [pdf_file]
            else:
                pdf_dict[key].append(pdf_file)
            my_progress.set(totalProg)
            totalProg += totalProg
            my_progress.update()
    except Exception as error:
        print("ERROR CREATING DICTIONARY: ", error)
        
    # Merge pdfs with the same first 10 characters
    try:
        merger = PdfMerger()
        for key, value in pdf_dict.items():
            print("WORKING ON: ", pdf_dict[key])
            if len(value) > 1:
                output_path = pdf_output_dir / f"{key}.pdf"
                for pdf_file in value:
                    file_path = os.path.join(pdf_dir, pdf_file)
                    with open(file_path, 'rb') as f:
                        merger.append(PdfReader(f))
                with open(output_path, 'wb') as f:
                    merger.write(f)
                merger = PdfMerger()
            my_progress.set(totalProg)
            totalProg += totalProg
            my_progress.update()
    except Exception as error:
        print("ERROR MERGING PDFs: ", error)
    
    my_progress.set(100)
    my_status.destroy()
    my_button2.pack(side="bottom", pady= 30)
    root.update()
    sys.stdout.close()
            
def main():
    gui()
    
main()
root.mainloop()