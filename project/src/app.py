import sys
import os
import tkinter as tk
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import ImageTk, Image
from tkcalendar import DateEntry
from employee import *
import cv2
from database import *
from functions import *


createfilepath()

createdb()

# Creating the color palette
bg_color = '#363536'
fg_color = '#ffffff'
green = '#30ba55'
red = '#d10202'
blue = '#1757b0'

base = Tk()
base.iconbitmap(r'assets/facivon_bl.ico')
base.title('Advanced Attendance System')
height = base.winfo_screenheight() // 2  # Centering the window
width = int(base.winfo_screenwidth() * 0.05)  # Moving the window 5% down from the top
base.geometry('600x500+' + str(height) + '+' + str(width))  # Setting the size and the location
base.configure(bg=bg_color)
base.resizable(False, False)

# Creating Screens
homescreen = tk.Frame(base, width=600, height=500, bg=bg_color)
signup = tk.Frame(base, width=600, height=500, bg=bg_color)
signin = tk.Frame(base, width=600, height=500, bg=bg_color)
hr = tk.Frame(base, width=600, height=500, bg=bg_color)
sector = tk.Frame(base, width=600, height=500, bg=bg_color)
for frame in (homescreen, signup, signin, hr, sector):
    frame.grid(row=0, column=0, sticky='nesw')


# Removes all widget's that belong to screen
def clear_screen(screen):
    for widget in screen.winfo_children():
        widget.destroy()


def load_homescreen():
    clear_screen(signup)
    clear_screen(signin)
    clear_screen(hr)
    clear_screen(sector)
    homescreen.tkraise()
    homescreen.pack_propagate(False)

    # Homescreen widgets
    # Adding the logo
    logo_img = ImageTk.PhotoImage(file="assets/logo_wh.jpg")
    logo = tk.Label(homescreen, image=logo_img, bg=bg_color)
    logo.imge = logo_img
    logo.grid(row=1, column=1, columnspan=2, pady=25, padx=20)

    # Buttons
    signupbtn = Button(homescreen, text="Sign up", command=lambda: load_signup(), height=2, width=10, font='Raleway',
                       cursor='hand2')
    signupbtn.grid(row=2, column=1, pady=45)
    signinbtn = Button(homescreen, text="Sign in", command=lambda: load_signin(), bg=blue, fg='#dedede', height=2,
                       width=10, font='Raleway', cursor='hand2')
    signinbtn.grid(row=2, column=2, pady=45)


def load_signup():
    clear_screen(homescreen)
    signup.tkraise()
    signup.pack_propagate(False)

    # Signup widgets
    # Labels
    lbl = tk.Label(signup, text='UID:', bg=bg_color, fg=fg_color, padx=10, pady=10, justify='right')
    lbl.grid(row=1, column=1)
    lbl1 = tk.Label(signup, text='First name:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl1.grid(row=2, column=1)
    lbl2 = tk.Label(signup, text='Last name:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl2.grid(row=3, column=1)
    lbl3 = tk.Label(signup, text='Email:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl3.grid(row=4, column=1)
    lbl4 = tk.Label(signup, text='Phone:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl4.grid(row=5, column=1)
    lbl5 = tk.Label(signup, text='Date of birth:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl5.grid(row=6, column=1)
    lbl6 = tk.Label(signup, text='Joined Date:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl6.grid(row=7, column=1)
    lbl7 = tk.Label(signup, text='Job position:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl7.grid(row=8, column=1)
    lbl8 = tk.Label(signup, text='Sector:', bg=bg_color, fg=fg_color, padx=10, pady=10)
    lbl8.grid(row=9, column=1)

    # Entry fields
    global cid, fn, ln, email, phone, dob, jd, jp, se, acceptbtn, sectors
    cid = tk.Entry(signup, width=30, bg=fg_color)
    cid.configure(state='disabled')  # Make field read-only
    cid.grid(row=1, column=2)
    fn = tk.Entry(signup, width=30, bg=fg_color)
    fn.grid(row=2, column=2)
    ln = tk.Entry(signup, width=30, bg=fg_color)
    ln.grid(row=3, column=2)
    email = tk.Entry(signup, width=30, bg=fg_color)
    email.configure(state='disabled')
    email.grid(row=4, column=2)
    phone = tk.Entry(signup, width=30, bg=fg_color)
    phone.grid(row=5, column=2)
    dob = DateEntry(signup, selectmode='day', width=27, date_pattern='yyyy-MM-dd')  # Date entry
    dob.grid(row=6, column=2)
    jd = DateEntry(signup, selectmode='day', width=27, date_pattern='yyyy-MM-dd')
    jd.grid(row=7, column=2)
    jp = tk.Entry(signup, width=30, bg=fg_color)
    jp.grid(row=8, column=2)

    # Drop down
    sectors = ['Select working sector . . .', ]
    results = fetchsectors()
    for result in results:
        data = '%s %s' % (result[0], result[1])
        sectors.append(data)
    se = ttk.Combobox(signup, values=sectors, width=27, state='readonly')
    se.current(0)
    se.grid(row=9, column=2)

    # Buttons
    cidbtn = Button(signup, text="Get card's uid", command=lambda: cuid(), cursor='hand2')
    cidbtn.grid(row=1, column=3, padx=10)
    gemailbtn = Button(signup, text="Generate email", command=lambda: gemail(), cursor='hand2')
    gemailbtn.grid(row=4, column=3, padx=10)
    photobtn = Button(signup, text="Capture face image", command='?', font='Raleway', cursor='hand2')
    photobtn.grid(row=10, column=1, columnspan=2)

    backbtn = Button(signup, text="Back", command=lambda: load_homescreen(), height=1, width=10, font='Raleway',
                     cursor='hand2')  # activebackground='#badee2'
    backbtn.grid(row=11, column=1, pady=50, padx=10)
    acceptbtn = Button(signup, text="Accept", command=lambda: accept(), bg='#1757b0', fg='#dedede', height=1,
                       width=10, font='Raleway', cursor='hand2')
    acceptbtn.grid(row=11, column=2, pady=50, padx=20)


def cuid():
    cid.configure(state='normal')
    cid.delete(0, END)
    try:
        id = readuid()
        cid.insert(0, id)
        cid.configure(state='disabled')
    except:
        showerror('Error', 'Check if the RFID/NFC reader is connected to the system or if its light is solid green'
                           ' and try again.')


def gemail():
    email.configure(state='normal')
    email.delete(0, END)
    if (len(fn.get()) > 0) and (len(ln.get()) > 0):
        email.insert(0, generateemail(fn.get(), ln.get()))
        email.configure(state='disabled')
    else:
        showerror('Error', 'Make sure that you have filled your first and last name and try again.')


def accept():
    if (len(cid.get()) == 0) or (len(fn.get()) == 0) or (len(ln.get()) == 0) or (len(email.get()) == 0) or \
            (len(phone.get()) < 10) or (len(dob.get()) == 0) or (len(jd.get()) == 0) or (len(jp.get()) == 0) or \
            (se.get() == sectors[0]):
        deleteuser(cid.get())
        showerror('Error',
                  'All or some values are been missing.\nMake sure that you have fill all of them and try again.')
    else:
        sector = se.get().split()
        dt = dob.get_date()
        db = dt.strftime("%Y-%m-%d")
        dt1 = jd.get_date()
        dj = dt1.strftime("%Y-%m-%d")
        try:
            insertemployee(cid.get(), fn.get(), ln.get(), email.get(), phone.get(), db, dj,
                           jp.get(), sector[0])
            userAdded = tk.Label(signup, text='Added user succeeded', bg=bg_color, fg=green, font='Raleway')
            userAdded.grid(row=11, column=3)
            # userAdded.after(1500, userAdded.grid_forget())
        except:
            showerror('Error', 'This uid already exist.\nPlease ask for a different card')


def load_signin():
    clear_screen(homescreen)
    signin.tkraise()
    signin.pack_propagate(False)
    hrbtn = tk.Button(signin, text='HR', command=lambda: load_hr())
    hrbtn.grid(row=0, column=2, pady=50, padx=20)
    sectorbtn = tk.Button(signin, text='SECTORS', command=lambda: load_sector())
    sectorbtn.grid(row=1, column=2, pady=50, padx=20)


def load_hr():
    clear_screen(homescreen)
    hr.tkraise()
    hr.pack_propagate(False)
    res = fetchemployees()
    for i in range(0, len(res)):
        result = res[i]
        lbl = tk.Label(hr, text=result, bg=bg_color, fg=fg_color)
        lbl.pack()
    hrback = tk.Button(hr, text='Back', command=lambda: load_homescreen(), height=1, width=10, font='Raleway',
                       cursor='hand2')
    hrback.pack()


def load_sector():
    clear_screen(homescreen)
    sector.tkraise()
    sector.pack_propagate(False)
    res = fetchsectors()

    # Create table to show the data
    sectortable = ttk.Treeview(sector)
    # table.configure(height=290)
    sectortable['columns'] = ("id", "name")  # Create columns
    sectortable.column("#0", width=0)  # Phantom column
    sectortable.column("id", anchor=CENTER, width=100, minwidth=25)
    sectortable.column("name", anchor=W, width=290, minwidth=30)
    # Setting headers
    sectortable.heading("#0", text="", anchor=W)
    sectortable.heading("id", text="Sector ID", anchor=CENTER)
    sectortable.heading("name", text="Sector Name", anchor=W)

    for i in range(0, len(res)):
        result = res[i]
        # lbl = tk.Label(sector, text=result, bg=bg_color, fg=fg_color)
        # lbl.grid(row=1, column=0, rowspan=100, columnspan=3, pady=20, padx=20)
        # lbl.pack(pady=15, padx=20)
        sectortable.insert(parent='', index='end', iid=i+1, values=result)
        sectortable.grid(row=0, column=1, rowspan=4, sticky='new', pady=20, padx=20)

    insrtsec = tk.Button(sector, text='Insert Sector', command=lambda: insec(), height=1, width=13, font='Raleway',
                         cursor='hand2')
    insrtsec.grid(row=0, column=0, pady=20, padx=10)
    updsec = tk.Button(sector, text='Update Sector', command=lambda: '?', height=1, width=13, font='Raleway',
                       cursor='hand2')
    updsec.grid(row=1, column=0, pady=20, padx=10)
    dltsec = tk.Button(sector, text='Delete', command=lambda: '?', height=1, width=13, font='Raleway',
                       cursor='hand2')
    dltsec.config(bg=red, fg=fg_color, activebackground=red, activeforeground=fg_color)
    dltsec.grid(row=2, column=0, pady=20, padx=10)
    secback = tk.Button(sector, text='Back', command=lambda: load_homescreen(), height=1, width=13, font='Raleway',
                        cursor='hand2')
    secback.grid(row=3, column=0, pady=200, padx=10)


def insec():
    global insert, secnameentry
    insert = Toplevel()
    insert.title('AAS - Add new sector')
    insert.focus()
    insert.tkraise()
    insert.config(background=bg_color)
    insert.pack_propagate(False)
    insert.geometry('350x200+' + str(height+175) + '+' + str(width+125))
    insert.resizable(False, False)
    secnamelbl = tk.Label(insert, text='New sectors name:', bg=bg_color, fg=fg_color)
    secnamelbl.grid(row=0, column=0, pady=20, padx=10)
    # insertsector('web')
    secnameentry = tk.Entry(insert, width=30)
    secnameentry.grid(row=0, column=1, pady=20, padx=8)
    addsector = tk.Button(insert, text='Add sector', command=lambda: insertsec(), height=1,
                          width=10, font='Raleway', cursor='hand2')
    addsector.config(bg=blue, fg=fg_color)
    addsector.grid(row=1, column=1, pady=20, padx=20)
    cancelsector = tk.Button(insert, text='Cancel', command=lambda: insert.destroy(), height=1,
                             width=10, font='Raleway', cursor='hand2')
    cancelsector.grid(row=1, column=0, pady=20, padx=15)


def insertsec():
    if len(secnameentry.get()) > 0:
        try:
            insertsector(secnameentry.get())
            showinfo('Info', 'New sector has been inserted succesfully.')
            insert.after(2000, insert.destroy())
        except:
            showerror('Error', 'Something went wrong.\nPlease try again')
    else:
        showerror('Error', 'Please make sure you add a sector name and try again')


# Start applicadtionaq
load_homescreen()

base.mainloop()
