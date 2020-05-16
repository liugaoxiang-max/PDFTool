from tkinter import filedialog, StringVar, IntVar, W, N, S, ttk, messagebox, mainloop
from ttkthemes import ThemedTk
import os
from os import listdir
from os.path import isfile, join
from functions import PdfImgFunctions
from pathlib import Path
import pkg_resources.py2_warn
#import time

initial_dir = 'C:\\'
dir_text = 'Select a Folder or a File'
image_formats = ["png", "jpg"]
d_options = ["pdf"] + image_formats

global folder_name, file_name


class ButtonSelect:
    def __init__(self, initial_dir):
        self.initial_dir = initial_dir

    def select_folder(self):
        global folder_name, file_name
        folder_name = filedialog.askdirectory(initialdir=self.initial_dir,
                                              title="Select A Folder")
        file_name = None
        return folder_name

    def select_file(self):
        global file_name, folder_name
        file_name = filedialog.askopenfilename(initialdir=self.initial_dir,
                                               title="Select A File")
        folder_name = None
        return file_name


class ButtonConvert:
    def __init__(self, from_format, to_format, MerSpli, dpi):
        #start_time = time.time()
        exitobj = []
        out_folder = str()
        if file_name == None:
            for f in os.listdir(folder_name):
                if f.endswith(from_format):
                    exitobj.append(os.path.join(folder_name, f))
                    file_extension = Path(os.path.join(folder_name, f)).suffix
            out_folder = folder_name
        else:
            exitobj = file_name
            path = Path(file_name)
            out_folder = path.parent
            file_extension = Path(file_name).suffix

        funcs = PdfImgFunctions(exitobj, out_folder, to_format, dpi)
        #Handling errors
        if file_extension != "." + from_format:
            messagebox.showinfo(
                "wrong operation",
                "the file you selected is not {}".format(from_format))
        elif from_format == "pdf" and to_format == "pdf" and not isinstance(
                exitobj, list) and MerSpli == 0:
            messagebox.showinfo(
                "wrong operation",
                "there is only one file, merge not possible, please select a folder"
            )
        elif from_format == "pdf" and to_format == "pdf" and isinstance(
                exitobj, list) and MerSpli == 1:
            messagebox.showinfo(
                "wrong operation",
                "please select a PDF file to split, not a folder")
        elif from_format in image_formats and to_format in image_formats:
            messagebox.showinfo(
                "wrong operation",
                "please find some other way to convert images")

        #PDF to Image
        elif from_format == "pdf" and to_format in image_formats:
            funcs.PDFtoImg(exitobj, out_folder, to_format)
            print("PDF to image")

        #Image to PDF
        elif from_format in image_formats and to_format == "pdf":
            funcs.ImgtoPDF(exitobj, out_folder, dpi)
            print("image to PDF")

        #PDF Merge
        elif from_format == "pdf" and to_format == "pdf" and MerSpli == 0:
            funcs.PDFMerge(exitobj, out_folder)
            print("PDF merge")

        #PDF Split
        elif from_format == "pdf" and to_format == "pdf" and MerSpli == 1:
            funcs.PDFSplit(exitobj, out_folder)
            print("PDF split")
        #print(exitobj, from_format, to_format, MerSpli, dpi, exitobj, out_folder)
        #print(file_extension)
        #print("--- %s seconds ---" % (time.time() - start_time))


class PdfToolGui(ThemedTk):
    def __init__(self, *args, **kwargs):
        ThemedTk.__init__(self, *args, **kwargs)
        self.title('PDF Tool')
        self.s = ttk.Style()
        self.s.configure("BSelect.TButton", font=('Helvetica', '12', 'bold'))
        self.s.configure("BConvert.TButton", font=('Helvetica', '14', 'bold'))
        self.button_select = ButtonSelect(initial_dir)
        self.b_select_folder()
        self.b_select_file()
        self.info_label(dir_text)
        self.frame = SetupBox()
        self.frame.grid(row=2, column=0, columnspan=2, padx=20, pady=10)

    def b_select_folder(self):
        b_select_folder = ttk.Button(
            self,
            text='Select Folder',
            command=lambda: [
                self.dir_info.destroy(),
                self.info_label(self.button_select.select_folder())
            ],
            style="BSelect.TButton")
        b_select_folder.grid(row=0, column=0, pady=20, ipadx=40, ipady=10)

    def b_select_file(self):
        b_select_file = ttk.Button(
            self,
            text='Select File',
            command=lambda: [
                self.dir_info.destroy(),
                self.info_label(self.button_select.select_file())
            ],
            style="BSelect.TButton")
        b_select_file.grid(row=0, column=1, pady=20, ipadx=40, ipady=15)

    def info_label(self, dir_text):
        self.dir_info = ttk.Label(text=dir_text)
        self.dir_info.grid(row=1, column=0, columnspan=2)


class SetupBox(ttk.LabelFrame):
    def __init__(self):
        ttk.LabelFrame.__init__(self, text='setup')
        self.combo_box_from()
        self.combo_box_to()
        self.input_box()
        self.radiobutton()
        self.button_convert()

    def combo_box_from(self):
        #DropDown menu to format
        self.d_from = ttk.Combobox(self, values=d_options)
        self.d_from.current(2)
        self.d_from.grid(row=0, column=0, padx=20, pady=20, ipadx=15)

    def combo_box_to(self):
        self.d_to = ttk.Combobox(self, values=d_options)
        self.d_to.current(0)
        self.d_to.grid(row=0, column=1, padx=20, pady=20, ipadx=15)

    def radiobutton(self):
        #Merge Split radio button
        self.radio_value = IntVar()
        self.r_merge = ttk.Radiobutton(self,
                                       text='PDF Merge',
                                       variable=self.radio_value,
                                       value=0)
        self.r_merge.grid(row=1, column=0, padx=40, sticky=W)
        self.r_split = ttk.Radiobutton(self,
                                       text='PDF Split',
                                       variable=self.radio_value,
                                       value=1)
        self.r_split.grid(row=2, column=0, padx=40, sticky=W)

    def input_box(self):
        #Target Size input box
        self.l_dpi = ttk.Label(self, text="output PDF dpi")
        self.l_dpi.grid(row=1, column=1, padx=20, pady=5, sticky=S)
        self.i_dpi = ttk.Entry(self)
        self.i_dpi.grid(row=2, column=1, padx=20, ipadx=20, sticky=N)
        self.i_dpi.insert(0, "200")

    def button_convert(self):
        b_convert = ttk.Button(
            self,
            text='Convert',
            command=lambda: [
                ButtonConvert(self.d_from.get(), self.d_to.get(),
                              self.radio_value.get(), self.i_dpi.get()),
            ],
            style='BConvert.TButton')
        b_convert.grid(row=3, column=0, padx=20, pady=20, ipadx=30, ipady=22)


if __name__ == '__main__':
    app = PdfToolGui(theme="plastik")
    app.mainloop()
