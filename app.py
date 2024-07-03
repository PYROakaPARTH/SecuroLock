from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
from PIL import ImageTk, Image
import sqlite3
from email.message import EmailMessage
import ssl
import smtplib
import random
import re
import os 
from cryptography.fernet import Fernet
import shutil
import zipfile as z
from datetime import datetime



def showFrame(frame):
    frame.tkraise()
    
def move_app(e):
    root.geometry(f'+{e.x_root}+{e.y_root}')

def quitApp(event):
    ans = messagebox.askquestion("Attention", "Are you sure you want to quit?", icon ='question')
    if ans == 'yes':
        root.destroy()
    else:
        pass
    
def quitAppinApp(event):
    directoryName = userNameField.get()
    path = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + directoryName
    
    ans = messagebox.askquestion("Attention", "Are you sure you want to quit?", icon ='question')
    if ans == 'yes':
        shutil.make_archive(path, 'zip', path)  
        getKey(directoryName)
        os.remove(path  + ".zip")
        shutil.rmtree(path)
        root.destroy()
    else:
        pass
      
    
def sendOTP():
    userNameQuery = userNameField.get()
    global otp
    otp = random.randint(1000,9999)
    
    db = sqlite3.connect('users.db')

    d = db.cursor()
    
    d.execute("SELECT email FROM userInfo WHERE username = '"+ userNameQuery +"' ")
    emailQuery =  d.fetchone()
    
    d = db.commit()

    d = db.close()

    email_sender = 'trap.ar.services@gmail.com'
    email_password = 'gjwdmtsmdjfppnga'
    email_receiver = str(emailQuery[0])

    subject = 'Your login OTP'
    body = "Your OTP is - " + str(otp)


    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context = context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
        
def verifyOTP():
    enteredOTP = otpField.get()
    user = str(onClickSubmitInLogin.userName)
    
    db = sqlite3.connect('users.db')

    d = db.cursor()
    
    d.execute("SELECT key FROM userInfo WHERE usernameDummy = '"+ user +"' ")
    userKeyQueryGet =  d.fetchone()
    
    d = db.commit()

    d = db.close()
    
    if int(enteredOTP) == int(otp):
        decrypt(userKeyQueryGet[0], user)
        unZip(user)
        deletePath = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + user + "_encrypted.zip"
        os.remove(deletePath)
        showFrame(appFrame)
        treeViewTrigger()
    else:
        messagebox.showerror("Wrong OTP","OTP does not match")
        
def onClickSubmitInRegister():
    global folder_name
    userNameQuery = userNameRegisterField.get()
    passwordFlag = 1
    flag = 0
    db = sqlite3.connect('users.db')

    d = db.cursor()
    
    d.execute("SELECT username FROM userInfo WHERE usernameDummy = '"+ userNameQuery +"' ")
    userNameQueryGet =  d.fetchone()
    
    d = db.commit()

    d = db.close()
    
    if userNameQueryGet == None:
        flag = 0
    elif userNameRegisterField.get() == userNameQueryGet[0]:
        flag = 1
    else:
        flag = 0
    
    if len(nameRegisterField.get()) == 0 or len(emailRegisterField.get()) == 0 or len(userNameRegisterField.get()) == 0 or len(passwordRegisterField.get()) == 0:  #checks if all fields are filled
        passwordErrorLabel = Label(registerFrame, text = "Please fill all the details!", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 20)
        passwordErrorLabel.place(x = 382, y = 380)
    
    #username validation  
    elif re.search("[0-9]", nameRegisterField.get()):    
        usernameValidityErrorLabel = Label(registerFrame, text = "Numbers not allowed in Name", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        usernameValidityErrorLabel.place(x = 260, y = 380)
    elif re.search("[~`!@#$%^&*()_+-=\][|}{?></.,';:]", nameRegisterField.get()):  
        usernameValidityErrorLabel = Label(registerFrame, text = "Special characters not allowed in Name", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        usernameValidityErrorLabel.place(x = 260, y = 380)  
        
    #password validation       
    elif (len(passwordRegisterField.get())<=8):
        passwordValidityErrorLabel1 = Label(registerFrame, text = "Password needs to have 8 or more characters", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        passwordValidityErrorLabel1.place(x = 258, y = 380)
    elif not re.search("[a-z]", passwordRegisterField.get()):
        passwordValidityErrorLabel2 = Label(registerFrame, text = "Password needs to have atleast one alphabet", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        passwordValidityErrorLabel2.place(x = 258, y = 380)
    elif not re.search("[A-Z]", passwordRegisterField.get()):
        passwordValidityErrorLabel3 = Label(registerFrame, text = "Password needs to have atleast one upper case letter", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        passwordValidityErrorLabel3.place(x = 257, y = 380)
    elif not re.search("[0-9]", passwordRegisterField.get()):
        passwordValidityErrorLabel3 = Label(registerFrame, text = "Password needs to have atleast one number", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        passwordValidityErrorLabel3.place(x = 259, y = 380)
    elif re.search("\s" , passwordRegisterField.get()):
        passwordValidityErrorLabel4 = Label(registerFrame, text = "Password cannot have blank spaces", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 50)
        passwordValidityErrorLabel4.place(x = 260, y = 380)
        
        
        
    elif flag == 1: #checks if username is unique
        repeatUserNameErrorLabel = Label(registerFrame, text = "Username already taken", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 20)
        repeatUserNameErrorLabel.place(x = 380, y = 380)
    else:
        folder_name = userNameRegisterField.get()
        #key = generateKey()
        db = sqlite3.connect('users.db')

        d = db.cursor()

        # d.execute("""CREATE TABLE userInfo(
        #    name text,
        #    email text,
        #    username text,
        #    password text,
        #    usernameDummy text
        #    )""")
        
        #d.execute("DELETE from userInfo WHERE oid = 4")
        d.execute("INSERT INTO userInfo VALUES (:name, :email, :username, :password, :usernameDummy, :key)",
                {
                    'name' : nameRegisterField.get(),
                    'email' : emailRegisterField.get(),
                    'username' : userNameRegisterField.get(),
                    'password' : passwordRegisterField.get(),
                    'usernameDummy' : userNameRegisterField.get(),
                    'key' : generateKey()
                })
            
        d = db.commit()

        d = db.close()
        
        nameRegisterField.delete(0, END)
        emailRegisterField.delete(0, END)
        userNameRegisterField.delete(0, END)
        passwordRegisterField.delete(0, END)
        
        messagebox.showinfo("Successfully registered!","Log in to continue")
        
        createFolder(folder_name)
   
    
def createFolder(folder_name):
    global zipName
    zipName = folder_name
    path = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folder_name
    os.mkdir(path) 
    file = open("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folder_name + "/dummy.txt", "w") 
    file.write("Do not delete")
    file.close()
    
    shutil.make_archive(path, 'zip', path)  
    shutil.rmtree(path)
    getKey(folder_name)
    
    deletePath = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folder_name + ".zip"
    os.remove(deletePath)
 
        
def unZip(fileName):
    target = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + fileName + "_decrypted.zip"
    
    root = z.ZipFile(target)
    
    root.extractall("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + fileName)
    
    root.close()
    
    deletePath = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + fileName + "_decrypted.zip"
    os.remove(deletePath)
    
  
def getKey(userName):
    db = sqlite3.connect('users.db')

    d = db.cursor()
    
    d.execute("SELECT key FROM userInfo WHERE usernameDummy = '"+ userName +"' ")
    userKeyQueryGet =  d.fetchone()
    
    d = db.commit()

    d = db.close()
    
    encrypt(userKeyQueryGet[0], userName)
    
def getKeyForDecryption(userName):
    db = sqlite3.connect('users.db')

    d = db.cursor()
    
    d.execute("SELECT key FROM userInfo WHERE usernameDummy = '"+ userName +"' ")
    userKeyQueryGet =  d.fetchone()
    
    d = db.commit()

    d = db.close()
    
    decrypt(userKeyQueryGet[0], userName)
    
    
def encrypt(key, folderName):
    f = Fernet(key)
    
    with open("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folderName + ".zip", 'rb') as original_file:
        original = original_file.read()
        
    encrypted = f.encrypt(original)
    
    with open("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folderName + "_encrypted.zip", 'wb') as encrypted_file:
        encrypted_file.write(encrypted)
        
def decrypt(key, folderName):
    f = Fernet(key)
    
    with open("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folderName + "_encrypted.zip", 'rb') as encrypted_file:
        encrypted = encrypted_file.read()
        
    decrypted = f.decrypt(encrypted)
    
    with open("C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + folderName + "_decrypted.zip", 'wb') as decrypted_file:
        decrypted_file.write(decrypted)
    
def generateKey():
    key = Fernet.generate_key()  
    return key
    

def onClickSubmitInLogin():
    onClickSubmitInLogin.userName = userNameField.get()
    userNameQuery = userNameField.get()
    db = sqlite3.connect('users.db')
    
    d = db.cursor()
    
    d.execute("SELECT password FROM userInfo WHERE username = '"+ userNameQuery +"' ")
    passwordQuery =  d.fetchone()
    
    d = db.commit()
    
    d = db.close()
    
    if str(passwordField.get()) == passwordQuery[0]:
        showFrame(otpFrame)
    else:
        passwordErrorLabel = Label(loginFrame, text = "Wrong Password!", bg = '#AA95C5',fg = 'red', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 18)
        passwordErrorLabel.place(x = 387, y = 315)

def treeViewTrigger(): 
    directoryName = userNameField.get()
    my_dir = "C:\\Users\\Parth\\Desktop\\Python projects\\Project\\User Folders\\" + directoryName
    my_view()
    my_insert(my_dir)
    
def my_view():
    global trv
    style = ttk.Style()
    style.configure("Treeview", background='#c8ebd7', fieldbackground='#c8ebd7', foreground="black", font=('Helvetica', 9, 'bold'))
    style.configure("Treeview.Heading", font=('Helvetica', 10, 'bold'))
    
    trv = ttk.Treeview(appFrame, selectmode ='browse',show ='headings')
    trv.place( x = 240, y =80)
    
    
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
        vs = ttk.Scrollbar(appFrame, orient="vertical", command=trv.yview) # scrollbar
        trv.configure(yscrollcommand=vs.set)  # connect to Treeview
        vs.place( x = 660, y = 81, width = 15, height = 224) # Place on grid 
        
def addFiles():
    directoryName = userNameField.get()
    appFrame.filename = filedialog.askopenfilename(initialdir = "Desktop", title = "Select files to import")
    baseName = os.path.basename(appFrame.filename)
    shutil.copyfile(appFrame.filename, "C:\\Users\\Parth\\Desktop\\Python projects\\Project\\User Folders\\" + directoryName + "\\" + baseName)
    treeViewTrigger() 
      
    
def removeFiles():
    directoryName = userNameField.get()
    appFrame.filename = filedialog.askopenfilename(initialdir = "C:\\Users\\Parth\\Desktop\\Python projects\\Project\\User Folders\\" + directoryName, title = "Select file to delete")
    baseName = os.path.basename(appFrame.filename)   
    os.remove("C:\\Users\\Parth\\Desktop\\Python projects\\Project\\User Folders\\" + directoryName + "\\" + baseName)
    treeViewTrigger()
    

def exportFiles():
    directoryName = userNameField.get()
    appFrame.filename = filedialog.askopenfilename(initialdir = "C:\\Users\\Parth\\Desktop\\Python projects\\Project\\User Folders\\" + directoryName, title = "Select file to export")
    baseName = os.path.basename(appFrame.filename)   
    shutil.copyfile(appFrame.filename, "C:\\Users\\Parth\\Desktop\\Python projects\\Project\\Exported Folders\\" + baseName)
    treeViewTrigger()
    
def logout():
    directoryName = userNameField.get()
    path = "C:/Users/Parth/Desktop/Python projects/Project/User Folders/" + directoryName
    
    ans = messagebox.askquestion("Attention", "Are you sure you want to logout?", icon ='question')
    if ans == 'yes':
        shutil.make_archive(path, 'zip', path)  
        getKey(directoryName)
        os.remove(path  + ".zip")
        shutil.rmtree(path)
        showFrame(mainFrame)
    else:
        pass
    
        
#db = sqlite3.connect('users.db')

#d = db.cursor()

#d.execute("""CREATE TABLE userInfo(
#   name text,
#   email text,
#   username text,
#   password text,
#   usernameDummy text
#   )""")
        

        
            
#d = db.commit()

#d = db.close()

root = Tk()
root.title('Project App')
app_width = 920
app_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (app_width / 2)
y = (screen_height / 2) - (app_height / 2)
root.geometry(f'{app_width}x{app_height}+{int(x)}+{int(y)}')
#root.geometry("920x500")
root.overrideredirect(1)
root.wm_attributes('-transparentcolor', '#4b00ff')
#root.eval('tk::PlaceWindow . center')
root.resizable(False,False)
root.rowconfigure(0, weight = 1)
root.columnconfigure(0, weight = 1)

    
#Defining Frames
mainFrame = Frame(root)
loginFrame = Frame(root)
registerFrame = Frame(root)
otpFrame = Frame(root)
appFrame = Frame(root)

mainFrame.grid(row = 0, column = 0, sticky = 'NSEW')
loginFrame.grid(row = 0, column = 0, sticky = 'NSEW')
registerFrame.grid(row = 0, column = 0, sticky = 'NSEW')
otpFrame.grid(row = 0, column = 0, sticky = 'NSEW')
appFrame.grid(row = 0, column = 0, sticky = 'NSEW')

for frame in (mainFrame, loginFrame, registerFrame, otpFrame, appFrame):
    frame.grid(row = 0, column = 0, sticky = 'NSEW')

showFrame(mainFrame)


#Main Frame Code
bgImage = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\home_bg3.png'))
bgImageLabel = Label(mainFrame, image = bgImage, bg = '#4b00ff')
bgImageLabel.place(x = 0, y = 0, relwidth = 1, relheight = 1)
bgImageLabel.bind("<B1-Motion>", move_app)

canvas = Canvas(mainFrame, width = 30, height = 30, borderwidth = 0, bg = '#f6f8d1')
canvas.place(x = 830, y = 15)
bgImage1 = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\transparent_dummy.png')) 
bg = canvas.create_image(0, 0, image=bgImage1)
quitImage = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\close_button.png'))
quitButton = canvas.create_image(17, 17, image=quitImage)
canvas.tag_bind(quitButton, "<Button-1>", quitApp)

loginButton = Button(mainFrame, text = "Login", command = lambda: showFrame(loginFrame), bg = "#F6F9D1", activebackground = '#f6f8d1', font = ('Arial', 14, 'bold'), width = 10, borderwidth = 0)
loginButton.place(x = 255, y = 277)

registerButton = Button(mainFrame, text = "Register", command = lambda: showFrame(registerFrame), bg = "#F6F9D1", activebackground = '#f6f8d1', font = ('Arial', 14, 'bold'), width = 10, borderwidth = 0)
registerButton.place(x = 534, y = 277)

#Login Frame Code
bgImageLogin = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\login_bg.png'))
bgImageLabelLogin = Label(loginFrame, image = bgImageLogin, bg = '#4b00ff')
bgImageLabelLogin.place(x = 0, y = 0, relwidth = 1, relheight = 1)
bgImageLabelLogin.bind("<B1-Motion>", move_app)

canvasLogin = Canvas(loginFrame, width = 30, height = 30, borderwidth = 0, bg = '#f6f8d1')
canvasLogin.place(x = 830, y = 15)
bg = canvasLogin.create_image(0, 0, image = bgImage1)
quitButtonLogin = canvasLogin.create_image(17, 17, image = quitImage)
canvasLogin.tag_bind(quitButtonLogin, "<Button-1>", quitApp)

userNameField = Entry(loginFrame, bg = '#f6f8d1', width = 18, borderwidth = 0, font = ('Arial', 13, 'bold'))
userNameField.place(x = 390, y = 199)

passwordField = Entry(loginFrame, bg = '#f6f8d1',show = 'x', width = 18, borderwidth = 0, font = ('Arial', 13, 'bold'))
passwordField.place(x = 390, y = 280)

submitButtonLogin = Button(loginFrame, text = "Submit", bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10, command = onClickSubmitInLogin)
submitButtonLogin.place(x = 417, y = 349)

registerButtonLogin = Button(loginFrame, text = "Register", bg = '#AA95C5', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10, command = lambda: showFrame(registerFrame))
registerButtonLogin.place(x = 418, y = 433)

homeButtonLogin = Button(loginFrame, text = "Home",bg = '#AA95C5', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), command = lambda: showFrame(mainFrame))
homeButtonLogin.place(x = 60, y = 444)


#Register Frame Code

bgImageRegister = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\register_bg.png'))
bgImageLabelRegister = Label(registerFrame, image = bgImageRegister, bg = '#4b00ff')
bgImageLabelRegister.place(x = 0, y = 0, relwidth = 1, relheight = 1)
bgImageLabelRegister.bind("<B1-Motion>", move_app)

canvasRegister = Canvas(registerFrame, width = 30, height = 30, borderwidth = 0, bg = '#f6f8d1')
canvasRegister.place(x = 830, y = 15)
bg = canvasRegister.create_image(0, 0, image = bgImage1)
quitButtonRegister = canvasRegister.create_image(17, 17, image = quitImage)
canvasRegister.tag_bind(quitButtonRegister, "<Button-1>", quitApp)

nameRegisterField = Entry(registerFrame, bg = '#f6f8d1', width = 22, borderwidth = 0, font = ('Arial', 13, 'bold'))
nameRegisterField.place(x = 219, y = 177)

emailRegisterField = Entry(registerFrame, bg = '#f6f8d1', width = 22, borderwidth = 0, font = ('Arial', 13, 'bold'))
emailRegisterField.place(x = 502, y = 177)

userNameRegisterField = Entry(registerFrame, bg = '#f6f8d1', width = 20, borderwidth = 0, font = ('Arial', 13, 'bold'))
userNameRegisterField.place(x = 240, y = 280)

passwordRegisterField = Entry(registerFrame, bg = '#f6f8d1', show = 'x', width = 20, borderwidth = 0, font = ('Arial', 13, 'bold'))
passwordRegisterField.place(x = 520, y = 280)

submitButtonRegister = Button(registerFrame, text = "Submit", bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10, command = onClickSubmitInRegister)
submitButtonRegister.place(x = 417, y = 349)

loginButtonRegister = Button(registerFrame, text = "Login", bg = '#AA95C5', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10, command = lambda: showFrame(loginFrame))
loginButtonRegister.place(x = 418, y = 433)

homeButtonRegister= Button(registerFrame, text = "Home", bg = '#AA95C5', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), command = lambda: showFrame(mainFrame))
homeButtonRegister.place(x = 60, y = 444)

#OTP Frame code

bgImageOTP = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\otp_bg.png'))
bgImageLabelOTP = Label(otpFrame, image = bgImageOTP, bg = '#4b00ff')
bgImageLabelOTP.place(x = 0, y = 0, relwidth = 1, relheight = 1)
bgImageLabelOTP.bind("<B1-Motion>", move_app)

canvasOTP = Canvas(otpFrame, width = 30, height = 30, borderwidth = 0, bg = '#f6f8d1')
canvasOTP.place(x = 830, y = 15)
bg = canvasOTP.create_image(0, 0, image = bgImage1)
quitButtonOTP = canvasOTP.create_image(17, 17, image = quitImage)
canvasOTP.tag_bind(quitButtonOTP, "<Button-1>", quitApp)

otpField = Entry(otpFrame, bg = '#f6f8d1', width = 8, borderwidth = 0, font = ('Arial', 13, 'bold'))
otpField.place(x = 440, y = 240)

sendOTPButton = Button(otpFrame, text = "Send OTP", command = sendOTP, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
sendOTPButton.place(x = 307, y = 314)

resendOTPButton = Button(otpFrame, text = "Resend OTP", command = sendOTP,bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
resendOTPButton.place(x = 528, y = 314)

verifyOTPButton = Button(otpFrame, text = "Verify OTP", command = verifyOTP, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
verifyOTPButton.place(x = 418, y = 383)

backButtonOTP= Button(otpFrame, text = "Home", bg = '#AA95C5', activebackground = '#AA95C5', borderwidth = 0, font = ('Arial', 10, 'bold'), command = lambda: showFrame(mainFrame))
backButtonOTP.place(x = 60, y = 444)

#App Frame code

bgImageApp = ImageTk.PhotoImage(Image.open('C:\\Users\\Parth\Desktop\\Python projects\\Project\\app_bg.png'))
bgImageLabelApp = Label(appFrame, image = bgImageApp, bg = '#4b00ff')
bgImageLabelApp.place(x = 0, y = 0, relwidth = 1, relheight = 1)
bgImageLabelApp.bind("<B1-Motion>", move_app)

canvasApp = Canvas(appFrame, width = 30, height = 30, borderwidth = 0, bg = '#f6f8d1')
canvasApp.place(x = 830, y = 15)
bg = canvasApp.create_image(0, 0, image = bgImage1)
quitButtonApp = canvasApp.create_image(17, 17, image = quitImage)
canvasApp.tag_bind(quitButtonApp, "<Button-1>", quitAppinApp)


# viewButton = Button(appFrame, text = "View", command = treeViewTrigger, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
# viewButton.place(x = 200, y = 314)

importButton = Button(appFrame, text = "Import", command = addFiles, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
importButton.place(x = 256, y = 353)

exportButton = Button(appFrame, text = "Export", command = exportFiles, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
exportButton.place(x = 416, y = 353)

deleteButton = Button(appFrame, text = "Delete", command = removeFiles, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
deleteButton.place(x = 574, y = 353)

logoutButton = Button(appFrame, text = "Logout", comman = logout, bg = '#f6f8d1', activebackground = '#f6f8d1', borderwidth = 0, font = ('Arial', 10, 'bold'), width = 10)
logoutButton.place(x = 52, y = 29)


root.mainloop()






#    db = sqlite3.connect('app.db')
#
#    d = db.cursor()
#
#   d = db.commit()
#
#   d = db.close()