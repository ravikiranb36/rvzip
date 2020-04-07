from tkinter import *
from tkinter import filedialog, messagebox
import os
from zipfile import ZipFile
import threading

class rvzip(Tk):

    def __init__(self):
        Tk.__init__(self)
        self.zip=True
        self.unzip= False
        self.zipdir=''
        self.unzip_file=''
        self.window_size()
        self.window()

    #Defining window size
    def window_size(self):
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        self.ww = int(sw / 3)
        self.wh = int(sh / 3)

    def window(self):
        self.geometry("%sx%s"%(self.ww, self.wh))
        self.lift()
        self.title("RVZIP")
        self.resizable(False, False)
        self.menubar = Menu(self)

        #Menu options
        self.menubar.add_command(label= 'Zip', command= self.Zip)
        self.menubar.add_command(label="Unzip", command = self.Unzip)

        #ZIP and Unzip window
        Label(self, text="Select dir").place(x=10, y=10)
        self.dir = StringVar()
        self.dir_entry= Entry(self, width =40, textvariable=self.dir )
        self.dir_entry.place(x=80, y= 10)
        Button(self, text="OPEN", command=self.OpenFolder).place(x=330,y=10)
        self.button=Button(self, text="Zip", width=10, command=lambda :threading.Thread(target=self.ZipUnzip).start())
        self.button.place(x=200, y=50)
        self.output = Text(self, width=40, height=7)
        self.output.place(x=40, y=90)

        self.config(menu= self.menubar)

    #filedialog to ask folder
    def OpenFolder(self):
        if self.zip:
            self.zipdir=filedialog.askdirectory()
            self.dir_entry.delete(0, END)
            self.zip_folder_name=os.path.split(self.zipdir)
            self.dir_entry.insert(INSERT, self.zip_folder_name[1])

        else:
            self.unzip_file= filedialog.askopenfilename(filetypes=(('zip files', '*.zip'), ))
            self.dir_entry.delete(0, END)
            self.unzip_filename=os.path.split(self.unzip_file)
            print(self.unzip_file, type(self.unzip_file))
            self.dir_entry.insert(INSERT, self.unzip_filename[1])
    def Zip(self):
        self.zip= True
        self.unzip=False
        self.button.config(text="Zip")

    def Unzip(self):
        self.unzip=True
        self.zip= False
        self.button.config(text="UnZip")
    def ZipUnzip(self):
        self.button.config(state=DISABLED)
        if self.zip and self.zipdir:
            #Finding all files in selcted folder
            paths=[]
            os.chdir(self.zip_folder_name[0])
            for root, directories, files in os.walk(self.zip_folder_name[1]):
                for file in files:
                    filepath = os.path.join(root, file)
                    paths.append(filepath)

            #Zipping all files


            with ZipFile(f"{self.zip_folder_name[1]}_zipped_by_rvzip.zip",'w') as zip:
                self.output.insert(END, "Zipping: \n")
                for file in paths:
                    zip.write(file)
                    zipping_file = os.path.split(file)
                    zip.setpassword(pwd=b"1234")
                    self.output.insert(END,f"{zipping_file[1]}\n")
                    self.output.see(END)
                self.output.insert(END, f"Zipped {self.zip_folder_name[1]} successfully")


        elif self.unzip and self.unzip_file:
            os.chdir(self.unzip_filename[0])
            with ZipFile(f"{self.unzip_filename[1]}", "r") as unzip:
                unzip.extractall(path=f"{self.unzip_filename[1]}_unzipped_by_rvzip")
                self.output.insert(END, f"{self.unzip_filename[1]} successfully")

        else:
            messagebox.showinfo("File Error", "Please select any file or directory")
        self.button.config(state=NORMAL)

if __name__=="__main__":
    rvzip().mainloop()