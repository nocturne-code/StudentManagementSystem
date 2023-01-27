from tkinter import *
from tkinter import messagebox
from PIL import ImageTk


# login function
def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'Test' and passwordEntry.get() == '1234':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import students
    else:
        messagebox.showerror('Error', 'Please enter correct details')


# window configuration and background image
window = Tk()

window.geometry('1280x700+0+0')
window.title('Login')
window.resizable(False, False)
backgroundImage = ImageTk.PhotoImage(file='notes.jpg')
bglabel = Label(window, image=backgroundImage)
bglabel.place(x=0, y=0)


# login frame
loginFrame = Frame(window)
loginFrame.place(x=480, y=260)

usernameLabel = Label(loginFrame, text='Username', font=('times new roman', 20, 'bold'))
usernameLabel.grid(row=0, column=0, padx=20, pady=10)

usernameEntry = Entry(loginFrame, font=('times new roman', 16))
usernameEntry.grid(row=0, column=1, padx=20, pady=10)


passwordLabel = Label(loginFrame, text='Password', font=('times new roman', 20, 'bold'))
passwordLabel.grid(row=1, column=0, padx=20, pady=10)
passwordEntry = Entry(loginFrame, font=('times new roman', 16))
passwordEntry.grid(row=1, column=1, padx=20, pady=10)

loginBtn = Button(loginFrame, text='Login', font=('times new roman', 16, 'bold'), width=15, cursor='hand2', command=login)
loginBtn.grid(row=2, column=1, padx=20, pady=10)


window.mainloop()
