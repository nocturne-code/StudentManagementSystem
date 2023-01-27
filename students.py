from tkinter import *
from tkinter import ttk, messagebox, filedialog
import pymysql
import time
import pandas


# window fields for adding, searching and updating data
def fields_data(title, buttontext, command):
    global idEntry, fnEntry, lnEntry, dobEntry, adEntry, pnEntry, genEntry, emEntry, currentdate, currenttime, screen_window

    currentdate = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')

    screen_window = Toplevel()
    screen_window.title(title)
    screen_window.resizable(0, 0)
    screen_window.grab_set()
    idLabel = Label(screen_window, text='ID', font=('times new roman', 16, 'bold'))
    idLabel.grid(row=0, column=0, padx=10, sticky=W)
    idEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    idEntry.grid(row=0, column=1, padx=40, pady=10)
    fnLabel = Label(screen_window, text='First Name', font=('times new roman', 16, 'bold'))
    fnLabel.grid(row=1, column=0, padx=10, sticky=W)
    fnEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    fnEntry.grid(row=1, column=1, padx=40, pady=10)
    lnLabel = Label(screen_window, text='Last Name', font=('times new roman', 16, 'bold'))
    lnLabel.grid(row=2, column=0, padx=10, sticky=W)
    lnEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    lnEntry.grid(row=2, column=1, padx=40, pady=10)
    dobLabel = Label(screen_window, text='Date Of Birth', font=('times new roman', 16, 'bold'))
    dobLabel.grid(row=3, column=0, padx=10, sticky=W)
    dobEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    dobEntry.grid(row=3, column=1, padx=40, pady=10)
    adLabel = Label(screen_window, text='Address', font=('times new roman', 16, 'bold'))
    adLabel.grid(row=4, column=0, padx=10, sticky=W)
    adEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    adEntry.grid(row=4, column=1, padx=40, pady=10)
    genLabel = Label(screen_window, text='Gender', font=('times new roman', 16, 'bold'))
    genLabel.grid(row=5, column=0, padx=10, sticky=W)
    genEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    genEntry.grid(row=5, column=1, padx=40, pady=10)
    emLabel = Label(screen_window, text='Email', font=('times new roman', 16, 'bold'))
    emLabel.grid(row=6, column=0, padx=10, sticky=W)
    emEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    emEntry.grid(row=6, column=1, padx=40, pady=10)
    pnLabel = Label(screen_window, text='Phone Number', font=('times new roman', 16, 'bold'))
    pnLabel.grid(row=7, column=0, padx=10, sticky=W)
    pnEntry = Entry(screen_window, font=('times new roman', 15), width=24)
    pnEntry.grid(row=7, column=1, padx=40, pady=10)
    screenbutton = Button(screen_window, text=buttontext, command=command)
    screenbutton.grid(row=8, columnspan=2, pady=15)

    if title == 'Update Student Info':
        indexing = table.focus()
        print(indexing)
        content = table.item(indexing)
        listdata = content['values']
        idEntry.insert(0, listdata[0])
        fnEntry.insert(0, listdata[1])
        lnEntry.insert(0, listdata[2])
        dobEntry.insert(0, listdata[3])
        adEntry.insert(0, listdata[4])
        pnEntry.insert(0, listdata[5])
        genEntry.insert(0, listdata[6])
        emEntry.insert(0, listdata[7])


# exit app function
def exit_app():
    result = messagebox.askyesno('Confirm', 'Do you want to exit?')
    if result:
        root.destroy()
    else:
        pass


# export data in excel file
def export_data():
    url = filedialog.asksaveasfilename(defaultextension='.csv')
    indexing = table.get_children()
    newlist = []
    for index in indexing:
        content = table.item(index)
        datalist = content['values']
        newlist.append(datalist)

    pan = pandas.DataFrame(newlist, columns=['ID', 'First Name', 'Last Name', 'Date of birth', 'Address', 'Phone Number', 'Gender', 'Email', 'Date created', 'Time created'])
    pan.to_csv(url, index=False)
    messagebox.showinfo('Success', 'Data exported')


# update student info
def update_data():
    query = 'update student set firstname=%s,lastname=%s,dob=%s,address=%s,number=%s,gender=%s,email=%s,date=%s,time=%s where id=%s'
    mycursor.execute(query, (fnEntry.get(), lnEntry.get(), dobEntry.get(), adEntry.get(), pnEntry.get(), genEntry.get(), emEntry.get(), currentdate, currenttime, idEntry.get()))
    con.commit()
    messagebox.showinfo('Success', 'Updated!', parent=screen_window)
    screen_window.destroy()
    show_students()


# show all data from database
def show_students():
    query = 'select * from student'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    table.delete(*table.get_children())
    for data in fetched_data:
        table.insert('', END, values=data)


# delete data from database
def delete_student():
    indexing = table.focus()
    print(indexing)
    content = table.item(indexing)
    content_id = content['values'][0]
    query = 'delete from student where id=%s'
    mycursor.execute(query, content_id)
    con.commit()
    messagebox.showinfo('Success', 'Deleted!')
    show_students()


# search data from database
def search_data():
    query = 'select * from student where id=%s or firstname=%s or lastname=%s or dob=%s or address=%s or number=%s or gender=%s or email=%s'
    mycursor.execute(query, (idEntry.get(), fnEntry.get(), lnEntry.get(), dobEntry.get(), adEntry.get(), pnEntry.get(), genEntry.get(), emEntry.get()))
    table.delete(*table.get_children())
    fetched_data = mycursor.fetchall()
    for data in fetched_data:
        table.insert('', END, values=data)


# add data to database
def add_data():
    if idEntry.get() == '' or fnEntry.get() == '' or lnEntry.get() == '' or dobEntry.get() == '' or adEntry.get() == '' or genEntry.get() == '' or emEntry.get() == '' or pnEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty', parent=screen_window)
    else:
        try:
            query = 'insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            mycursor.execute(query, (idEntry.get(), fnEntry.get(), lnEntry.get(), dobEntry.get(), adEntry.get(), pnEntry.get(), genEntry.get(), emEntry.get(), currentdate, currenttime))
            con.commit()
            messagebox.showinfo('Success', 'You submitted the form', parent=screen_window)
            idEntry.delete(0, END)
            fnEntry.delete(0, END)
            lnEntry.delete(0, END)
            dobEntry.delete(0, END)
            genEntry.delete(0, END)
            emEntry.delete(0, END)
            adEntry.delete(0, END)
            pnEntry.delete(0, END)

        except:
            messagebox.showerror('Error', 'ID already exists', parent=screen_window)
            return

        show_students()


def connecttodatabase():
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(user=usernameEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
        except:
            messagebox.showerror('Error', 'Incorrect data', parent=connectwindow)
            return
        try:
            query = 'create database students'
            mycursor.execute(query)
            query = 'use students'
            mycursor.execute(query)
            query = 'create table student(id int not null primary key,firstname varchar(30),lastname varchar(30), ' \
                    'dob varchar(20),address varchar(50),number varchar(20),gender varchar(20),email varchar(50), ' \
                    'date varchar(20),time varchar(20))'
            mycursor.execute(query)
        except:
            query = 'use students'
            mycursor.execute(query)
        messagebox.showinfo('Success', 'You are connected', parent=connectwindow)
        connectwindow.destroy()
        addBtn.config(state=NORMAL)
        searchBtn.config(state=NORMAL)
        updateBtn.config(state=NORMAL)
        deleteBtn.config(state=NORMAL)
        showBtn.config(state=NORMAL)
        exportBtn.config(state=NORMAL)

# login window to database
    connectwindow = Toplevel()
    connectwindow.grab_set()
    connectwindow.geometry("400x150+150+200")
    connectwindow.title('Connection')
    connectwindow.resizable(0, 0)

    usernameLabel = Label(connectwindow, text='Username', font=('times new roman', 16, 'bold'))
    usernameLabel.grid(row=0, column=0, padx=20)
    usernameEntry = Entry(connectwindow, font=('times new roman', 15))
    usernameEntry.grid(row=0, column=1, padx=40, pady=10)
    passwordLabel = Label(connectwindow, text='Password', font=('times new roman', 16, 'bold'))
    passwordLabel.grid(row=1, column=0, padx=20)
    passwordEntry = Entry(connectwindow, font=('times new roman', 15))
    passwordEntry.grid(row=1, column=1, padx=40, pady=10)
    connectbutton = Button(connectwindow, text='CONNECT', command=connect)
    connectbutton.grid(row=2, columnspan=2)


# window configuration
root = Tk()
root.geometry('1280x700+0+0')
root.title('Student Management System')
root.resizable(False, False)

# button that connects to mysql database
connectBtn = Button(root, text='Connect', command=connecttodatabase)
connectBtn.place(x=50, y=20)

# left frame with buttons
leftFrame = Frame(root)
leftFrame.place(x=50, y=80)

addBtn = Button(leftFrame, text='Add Student', width=20, cursor='hand2', state=DISABLED, command= lambda :fields_data("Add Student", "SUBMIT", add_data))
addBtn.grid(row=0, column=0, pady=20, padx=20)

searchBtn = Button(leftFrame, text='Search Students', width=20, cursor='hand2', state=DISABLED, command= lambda :fields_data('Search Students', 'SEARCH', search_data))
searchBtn.grid(row=1, column=0, pady=20, padx=20)

updateBtn = Button(leftFrame, text='Update Student Info', width=20, cursor='hand2', state=DISABLED, command= lambda :fields_data('Update Student Info', 'UPDATE', update_data))
updateBtn.grid(row=2, column=0, pady=20, padx=20)

deleteBtn = Button(leftFrame, text='Delete Student', width=20, cursor='hand2', state=DISABLED, command=delete_student)
deleteBtn.grid(row=3, column=0, pady=20, padx=20)

showBtn = Button(leftFrame, text='Show Students', width=20, cursor='hand2', state=DISABLED, command=show_students)
showBtn.grid(row=4, column=0, pady=20, padx=20)

exportBtn = Button(leftFrame, text='Export', width=20, cursor='hand2', state=DISABLED, command=export_data)
exportBtn.grid(row=5, column=0, pady=20, padx=20)

exitBtn = Button(leftFrame, text='Exit', width=20, cursor='hand2', command=exit_app)
exitBtn.grid(row=6, column=0, pady=20, padx=20)

# right frame and table with data
rightFrame = Frame(root)
rightFrame.place(x=280, y=40, width=950, height=600)

# table config
scrollx = Scrollbar(rightFrame, orient=HORIZONTAL)
scrolly = Scrollbar(rightFrame, orient=VERTICAL)

table = ttk.Treeview(rightFrame, columns=('ID', 'First Name', 'Last Name', 'Date of birth', 'Address', 'Phone Number',
                                          'Gender', 'Email', 'Added Date', 'Added Time'),
                                        xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

scrollx.config(command=table.xview)
scrolly.config(command=table.yview)
scrollx.pack(side=BOTTOM, fill=X)
scrolly.pack(side=RIGHT, fill=Y)
table.pack(fill=BOTH, expand=1)

table.heading('ID', text='ID')
table.heading('First Name', text='First Name')
table.heading('Last Name', text='Last Name')
table.heading('Date of birth', text='Date of birth')
table.heading('Address', text='Address')
table.heading('Phone Number', text='Phone Number')
table.heading('Gender', text='Gender')
table.heading('Email', text='Email')
table.heading('Added Date', text='Added Date')
table.heading('Added Time', text='Added Time')

table.config(show='headings')

root.mainloop()
