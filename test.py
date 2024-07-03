from tkinter import ttk
from tkinter import *
from tkinter import filedialog
import os
from datetime import datetime

def my_view():
    global trv
    trv = ttk.Treeview(root, selectmode ='browse',show='headings')
    trv.grid(row=2,column=1,columnspan=3,padx=30,pady=10)
# column identifiers 
    trv["columns"] = ("1", "2","3","4")
    trv.column("1", width = 150, anchor ='w')
    trv.column("2", width = 100, anchor ='c')
    trv.column("3", width = 100, anchor ='c')
    trv.column("4", width = 70, anchor ='c')


    trv.heading(1, text ="Name",anchor='c')
    trv.heading(2, text ="Type",anchor='c')
    trv.heading(3, text ="Date Modified",anchor='c')
    trv.heading(4, text ="Size",anchor='c')
    
def treeViewTrigger(): 
    my_dir = "C:\\Users\\Parth\\Desktop\\Python projects\\Project"
    my_view()
    my_insert(my_dir)
    
    
def my_insert(path):
    global trv
    
    files=os.listdir(path)
    i=1
    for f in files:
        f_path=path+'\\'+f # Path with file name
        t_stamp=os.path.getmtime(f_path) # for file modificaton time
        
        f_name,f_extension=os.path.splitext(f_path) # get file extension
        size=os.path.getsize(f_path) # size of file in bytes 
        dt_mod = datetime.fromtimestamp(t_stamp) # date object 
        
        m_date = datetime.strftime(dt_mod, '%Y-%m-%d') # Change format 
        
        trv.insert("",'end',iid=i,text=i,values=(f, f_extension, m_date,size))
        i=i+1
        vs = ttk.Scrollbar(root,orient="vertical", command=trv.yview) # scrollbar
        trv.configure(yscrollcommand=vs.set)  # connect to Treeview
        vs.grid(row=2,column=4,sticky='ns') # Place on grid 
        


root = Tk()
root.geometry("600x480") 
root.title("www.plus2net.com")

treeViewTrigger()

viewButton = Button(root, text = "View Files", bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
viewButton.place(x = 307, y = 314)






root.mainloop()