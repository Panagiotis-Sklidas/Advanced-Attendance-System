import sys
import re
import cv2
import tkinter as tk
import sqlite3
from tkinter import *
from tkinter.messagebox import *
from tkinter import ttk
from PIL import ImageTk, Image
from smartcard.Exceptions import *
from tkcalendar import DateEntry
import database as databasefile
import functions as functionsfile

# Initialize app
functionsfile.createfilepath()

databasefile.createdb()

# Creating the color palette
darkgrey = '#363536'
white = '#ffffff'
green = '#30ba55'
red = '#d10202'
blue = '#1757b0'

# Build main window
base = Tk()
base.iconbitmap(r'assets/favicon_64x64.ico')
base.title('Advanced Attendance System')
height = int(base.winfo_screenheight() / 10)
width = int(base.winfo_screenwidth() * 0.01)  # Moving the window 1% down from the top
# base.geometry('1200x700+' + str(height) + '+' + str(width))  # Setting the size and the location
base.configure(bg=darkgrey)
base.resizable(False, False)

# Creating Screens
homescreen = tk.Frame(base, bg=darkgrey)
signup = tk.Frame(base, bg=darkgrey)
adminpanel = tk.Frame(base, bg=darkgrey)
employees = tk.Frame(base, bg=darkgrey)
sector = tk.Frame(base, bg=darkgrey)
for frame in (homescreen, signup, adminpanel, employees, sector):
    frame.grid(row=0, column=0, sticky='nesw')


# Removes all widget's that belong to screen
def clear_screen(screen):
    for widget in screen.winfo_children():
        widget.destroy()


# Create homescreen
def load_homescreen():
    base.geometry('1100x650+' + str(height) + '+' + str(width))
    clear_screen(signup)
    clear_screen(adminpanel)
    clear_screen(employees)
    clear_screen(sector)
    homescreen.tkraise()
    homescreen.pack_propagate(False)

    # Homescreen widgets
    # Adding the logo
    logo_img = ImageTk.PhotoImage(file="assets/logo_wh.jpg")
    logo = tk.Label(homescreen, image=logo_img, bg=darkgrey)
    logo.imge = logo_img
    logo.grid(row=1, column=1, columnspan=2, pady=50, padx=275)

    # Buttons
    signupbtn = Button(homescreen, text="Sign up", command=lambda: load_signup(), height=2, width=10, font='Raleway',
                       cursor='hand2')
    signupbtn.grid(row=2, column=1, pady=45)
    adminpanelbtn = Button(homescreen, text="Enter work area", command=lambda: login(), bg=blue, fg=white, height=2,
                       width=15, font='Raleway', cursor='hand2', activeforeground=white, activebackground=blue)
    adminpanelbtn.grid(row=2, column=2, pady=45)
    signoutbtn = Button(homescreen, text="Exit work area", command=lambda: logout(), bg=red,
                        fg=white, height=2, width=15, font='Raleway', cursor='hand2', activeforeground=white,
                        activebackground=red)
    signoutbtn.grid(row=3, column=2, pady=45)


# Create signup
def load_signup():
    base.geometry('475x600+' + str(height) + '+' + str(width))
    clear_screen(homescreen)
    signup.tkraise()
    signup.pack_propagate(True)

    # Signup widgets
    # Labels
    # spacer = tk.Label(signup, bg=darkgrey, fg=white, padx=200, pady=25)
    # spacer.grid(row=0, column=0)
    lbl = tk.Label(signup, text='UID:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl.grid(row=1, column=1)
    lbl1 = tk.Label(signup, text='First name:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl1.grid(row=2, column=1)
    lbl2 = tk.Label(signup, text='Last name:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl2.grid(row=3, column=1)
    lbl3 = tk.Label(signup, text='Email:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl3.grid(row=4, column=1)
    lbl4 = tk.Label(signup, text='Phone:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl4.grid(row=5, column=1)
    lbl5 = tk.Label(signup, text='Date of birth:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl5.grid(row=6, column=1)
    lbl6 = tk.Label(signup, text='Joined Date:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl6.grid(row=7, column=1)
    lbl7 = tk.Label(signup, text='Job position:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl7.grid(row=8, column=1)
    lbl8 = tk.Label(signup, text='Sector:', bg=darkgrey, fg=white, padx=10, pady=10)
    lbl8.grid(row=9, column=1)

    # Entry fields
    global cid, fn, ln, email, phone, dob, jd, jp, se, acceptbtn, sectors, hasimage
    cid = tk.Entry(signup, width=30, bg=white)
    cid.configure(state='disabled')  # Make field read-only
    cid.grid(row=1, column=2)
    fn = tk.Entry(signup, width=30, bg=white)
    fn.grid(row=2, column=2)
    ln = tk.Entry(signup, width=30, bg=white)
    ln.grid(row=3, column=2)
    email = tk.Entry(signup, width=30, bg=white)
    email.configure(state='disabled')
    email.grid(row=4, column=2)
    phone = tk.Entry(signup, width=30, bg=white)
    phone.grid(row=5, column=2)
    dob = DateEntry(signup, selectmode='day', width=27, date_pattern='yyyy-MM-dd')  # Date entry
    dob.grid(row=6, column=2)
    jd = DateEntry(signup, selectmode='day', width=27, date_pattern='yyyy-MM-dd')
    jd.grid(row=7, column=2)
    jp = tk.Entry(signup, width=30, bg=white)
    jp.grid(row=8, column=2)

    # Drop down
    sectors = ['Select working sector . . .', ]
    results = databasefile.fetchsectors()
    for result in results:
        data = '%s %s' % (result[0], result[1])
        sectors.append(data)
    se = ttk.Combobox(signup, values=sectors, width=27, state='readonly')
    se.current(0)
    se.grid(row=9, column=2)
    hasimage = False

    # Buttons
    cidbtn = Button(signup, text="Get card's uid", command=lambda: cuid(), cursor='hand2')
    cidbtn.grid(row=1, column=3, padx=10)
    gemailbtn = Button(signup, text="Generate email", command=lambda: gemail(), cursor='hand2')
    gemailbtn.grid(row=4, column=3, padx=10)
    photobtn = Button(signup, text="Capture face image", command=lambda: takephoto(), font='Raleway',
                      cursor='hand2')
    photobtn.grid(row=10, column=1, columnspan=2, pady=20)

    backbtn = Button(signup, text="Back", command=lambda: load_homescreen(), height=1, width=10, font='Raleway',
                     cursor='hand2')
    backbtn.grid(row=12, column=1, pady=50, padx=10)
    acceptbtn = Button(signup, text="Accept", command=lambda: accept(), bg='#1757b0', fg='#dedede', height=1,
                       width=10, font='Raleway', cursor='hand2')
    acceptbtn.grid(row=12, column=3, pady=50, padx=20)


def takephoto():
    # Opens photo booth window showing video feed from the webcam
    global photoboothlbl, camera, photobooth
    hasimage = False
    if len(cid.get()) > 0:
        photobooth = Toplevel()
        photobooth.title('AAS - Take picture')
        photobooth.geometry('644x545')
        photobooth.resizable(False, False)
        photobooth.focus()
        photoboothlbl = tk.Label(photobooth)
        photoboothlbl.grid(row=0, column=0)
        camera = cv2.VideoCapture(0)  # Create the capturing 'device'
        show_frames()

        captureimage = tk.Button(photobooth, text='Capture', command=lambda: capture())
        captureimage.configure(background=blue, foreground=white, activebackground=blue, activeforeground=white,
                               font='Raleway', cursor='hand2')
        captureimage.grid(row=1, column=0, pady=10)
    else:
        showerror('Error', 'Please fill first the card\'s id and try again')


def close():
    photobooth.destroy()
    # Release camera
    camera.release()
    cv2.destroyAllWindows()


def show_frames():
    global img
    """
    Pass a video frame every 20ms to the photobooth label

    :return:
    """
    cv2image = cv2.cvtColor(camera.read()[1], cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    videofeed = ImageTk.PhotoImage(image=img)
    photoboothlbl.imgtk = videofeed
    photoboothlbl.configure(image=videofeed)
    photoboothlbl.after(20, show_frames)


def capture():
    # Shows a preview of the taken photo and asks if is it ok to save it
    global preview
    hasimage = False
    preview = Toplevel()
    preview.title('AAS - Preview picture')
    preview.geometry('644x545')
    preview.resizable(False, False)
    preview.focus()
    lblimg = tk.Label(preview)
    lblimg.grid(row=0, column=0, columnspan=2)
    btnimgsave = tk.Button(preview, text='Save', command=lambda: savefaceimg())
    btnimgsave.configure(background=blue, foreground=white, activebackground=blue, activeforeground=white,
                         font='Raleway', cursor='hand2')
    btnimgsave.grid(row=1, column=1, pady=10)
    btnimgcancel = tk.Button(preview, text='Try again', command=lambda: preview.destroy())
    btnimgcancel.configure(font='Raleway', cursor='hand2')
    btnimgcancel.grid(row=1, column=0, pady=10)

    pr = ImageTk.PhotoImage(image=img)
    lblimg.imgtk = pr
    lblimg.configure(image=pr)


def savefaceimg():
    """
    Save image

    :return: True if image is saved
    """
    hasimage = True
    imgpreview = img
    if len(sys.argv) < 2:
        imgsavepath = 'C:/AdvancedAttendanceSystem/FaceImages/' + cid.get() + '.jpg'
    else:
        imgsavepath = sys.argv[1]

    imgpreview.save(imgsavepath)

    preview.destroy()
    close()
    return hasimage


# Tries to read the card's uid and display it on screen
def cuid():
    cid.configure(state='normal')
    cid.delete(0, END)
    try:
        cardid = functionsfile.readuid()
        cid.insert(0, cardid)
        cid.configure(state='disabled')
    except NoCardException:
        showerror('Error', 'Either the smart card has been removed, so that further communication is not possible or '
                           'there are more than one smart cards near the reader')
    except IndexError:
        showerror('Error', 'Check if the RFID/NFC reader is connected to the system and try again')


# Tries to generate email using the function generateemail from functions.py
def gemail():
    email.configure(state='normal')
    email.delete(0, END)
    if (len(fn.get()) > 0) and (len(ln.get()) > 0):
        email.insert(0, functionsfile.generateemail(fn.get(), ln.get()))
        email.configure(state='disabled')
    else:
        showerror('Error', 'Make sure that you have filled your first and last name and try again')


def uemail():
    eemail.delete(0, END)
    if (len(efn.get()) > 0) and (len(eln.get()) > 0):
        eemail.insert(0, functionsfile.generateemail(efn.get(), eln.get()))
    else:
        showerror('Error', 'Make sure that you have filled your first and last name and try again')
# Performing the neccesery checks before attempting to insert employee to db


def accept():
    isadult = int(jd.get().split('-')[0]) - int(dob.get().split('-')[0])
    # Checks if all fields are filled and if the person is 18 years old
    if (len(cid.get()) == 0) or (len(fn.get()) == 0) or (len(ln.get()) == 0) or (len(email.get()) == 0) or \
            (len(phone.get()) < 10 or (re.search('[a-zA-Z]', phone.get()) is not None)) or (len(dob.get()) == 0) or \
            (len(jd.get()) == 0) or (len(jp.get()) == 0) or (se.get() == sectors[0] or
                                                             (isadult < 18) or (not savefaceimg())):
        showerror('Error',
                  'Something went wrong:\n1) All or some values may be missing\n2) There are some letters in phone '
                  'number\n3) The employee is not old enough (18 years old)\n4) There is not a saved face image for the'
                  ' employee\nMake sure that you have check all of the above and try again')
    elif (databasefile.admincount() == 1) and jp.get().upper() == 'ADMIN':
        showerror('Error', 'There is already an ADMIN\nChange your job position and try again')
    else:
        # Tries to insert umployee
        sector = se.get().split()
        dt = dob.get_date()
        db = dt.strftime("%Y-%m-%d")
        dt1 = jd.get_date()
        dj = dt1.strftime("%Y-%m-%d")
        try:
            databasefile.insertemployee(cid.get(), fn.get(), ln.get(), email.get(), phone.get(), db, dj, jp.get(),
                                        int(sector[0]))
            useradded = tk.Label(signup, text='User added successfully', bg=darkgrey, fg=green, font='Raleway')
            useradded.grid(row=11, column=0, columnspan=3)
            # userAdded.after(1500, userAdded.grid_forget())
        except sqlite3.IntegrityError:
            showerror('Error', 'There is already a user with this id\nGet a new card and try again')


global inemployee


def login():
    try:
        readercarduid = functionsfile.readuid()
        cameraemployeename = functionsfile.f_recognition(readercarduid)
        inemployee = databasefile.selectemployee(readercarduid)
        if (inemployee is not None) and (cameraemployeename == readercarduid):
            functionsfile.enter_work_area(inemployee)
            showinfo('Info', 'Welcome ' + inemployee[1] + ' ' + inemployee[2] + ' have a nice day')
            if inemployee[8] == 1:
                load_adminpanel(inemployee)
        else:
            showinfo('Info', 'The card\'s uid does not match the face image\nMake sure to use your card or talk to HR')
            supervisoraccess(True)
    except NoCardException:
        showerror('Error', 'Either the smart card has been removed, so that further communication is not possible or '
                           'there are more than one smart cards near the reader')
    except IndexError:
        showerror('Error', 'Check if the RFID/NFC reader is connected to the system and try again or talk to HR')
        supervisoraccess(True)


def supervisoraccess(enter: bool):
    global grantaccess
    grantaccess = Toplevel()
    grantaccess.configure(bg=darkgrey)
    grantaccess.resizable(False, False)
    lbl = tk.Label(grantaccess, text='Provide the unique id of the user to whom you want to grant access', font='Relaway')
    lbl.grid(column=0, row=0)
    lbl.configure(bg=darkgrey, fg=white, pady=20, padx=20)
    uidfield = tk.Entry(grantaccess)
    uidfield.configure(font='Relaway')
    uidfield.grid(column=0, row=1)
    grantbtn = tk.Button(grantaccess, text='Grant Access', font='Relaway', bg=green, activebackground=green, fg=white,
                         activeforeground=white, command=lambda: grant(enter, uidfield.get().upper()))
    grantbtn.grid(column=0, row=2, pady=20)

    if enter:
        grantaccess.title('Supervisor Grant Access - Entering')
    else:
        grantaccess.title('Supervisor Grant Access - Exiting')


def grant(enter: bool, uid: str):
    inemployee = databasefile.selectemployee(uid)

    if enter:
        if inemployee is not None:
            functionsfile.enter_work_area(inemployee)
            showinfo('Info', 'Welcome ' + inemployee[1] + ' ' + inemployee[2] + ' have a nice day')
            if inemployee[8] == 1:
                load_adminpanel(inemployee)
            grantaccess.destroy()
    else:
        if inemployee is not None:
            functionsfile.exit_work_area(inemployee[0])
            showinfo('Info', 'Your exiting time has been stored successfully')
            grantaccess.destroy()


def logout():
    try:
        readercarduid = functionsfile.readuid()
        outemployee = databasefile.selectemployee(readercarduid)
        if outemployee is not None:
            functionsfile.exit_work_area(outemployee[0])
            showinfo('Info', 'Your exiting time has been stored successfully')
        else:
            showinfo('Error', 'The card\'s uid does not match any uid in the database\nMake sure to use your card or '
                              'talk to HR')
            supervisoraccess(False)
    except NoCardException:
        showerror('Error', 'Either the smart card has been removed, so that further communication is not possible or '
                           'there are more than one smart cards near the reader')
    except IndexError:
        showerror('Error', 'Check if the RFID/NFC reader is connected to the system and try again')
        supervisoraccess(False)


# Create adminpanel screen
def load_adminpanel(employee):
    base.geometry('350x400+' + str(height) + '+' + str(width))
    if employee[8] == 1:
        clear_screen(homescreen)
        adminpanel.tkraise()
        adminpanel.pack_propagate(False)

        # spacer = tk.Label(adminpanel, bg=darkgrey, fg=white, padx=200, pady=25)
        # spacer.grid(row=0, column=0)
        admnpnllbl = tk.Label(adminpanel, text='Admin Panel', font='Relaway', bg=darkgrey, fg=white)
        admnpnllbl.grid(row=0, column=1, columnspan=4, pady=50, padx=20)
        hrbtn = tk.Button(adminpanel, text='Human Resources', command=lambda: load_employees(employee), font='Relaway')
        hrbtn.grid(row=1, column=2, pady=50, padx=20)
        sectorbtn = tk.Button(adminpanel, text='Sectors', command=lambda: load_sector(employee), font='Relaway')
        sectorbtn.grid(row=1, column=3, pady=50, padx=20)
        backbtn = tk.Button(adminpanel, text='Back', command=lambda: load_homescreen(), font='Relaway')
        backbtn.grid(row=2, column=0, columnspan=4, pady=50, padx=20, sticky='nesw')


# Create employee screen
def load_employees(user):
    base.geometry('1150x675+' + str(height) + '+' + str(width))
    clear_screen(homescreen)
    employees.tkraise()
    employees.pack_propagate(False)

    # Create table to show the data
    style = ttk.Style()
    style.configure('Treeview',
                    background=white,
                    foreground='black',
                    fieldbackground=white
                    )
    style.map('Treeview', background=[('selected', blue)])
    # Create table to show the data
    global employeetable
    employeetable = ttk.Treeview(employees)
    employeetable.configure(height=30)
    employeetable['columns'] = ("id", "fn", "ln", "em", "ph", "dob", "jd", "jp", "sid")  # Create columns
    # employeetable.column("#0", width=25)  # Phantom column
    employeetable.column("#0", width=0)
    employeetable.column("id", anchor=CENTER, width=70, minwidth=70)
    employeetable.column("fn", anchor=W, width=80, minwidth=80)
    employeetable.column("ln", anchor=W, width=80, minwidth=80)
    employeetable.column("em", anchor=W, width=165, minwidth=80)
    employeetable.column("ph", anchor=W, width=80, minwidth=80)
    employeetable.column("dob", anchor=W, width=80, minwidth=80)
    employeetable.column("jd", anchor=W, width=80, minwidth=80)
    employeetable.column("jp", anchor=W, width=165, minwidth=80)
    employeetable.column("sid", anchor=W, width=85, minwidth=85)
    # Setting headers
    # employeetable.heading("#0", text="A/A", anchor=W)
    employeetable.heading("#0", text="")
    employeetable.heading("id", text="Unique ID", anchor=CENTER)
    employeetable.heading("fn", text="First Name", anchor=W)
    employeetable.heading("ln", text="Last Name", anchor=W)
    employeetable.heading("em", text="Email", anchor=W)
    employeetable.heading("ph", text="Phone", anchor=W)
    employeetable.heading("dob", text="Date of Birth", anchor=W)
    employeetable.heading("jd", text="Joined Date", anchor=W)
    employeetable.heading("jp", text="Position", anchor=W)
    employeetable.heading("sid", text="Sector ID", anchor=W)
    employeetable.tag_configure('even', background='silver')
    employeetable.tag_configure('odd', background=white)

    counter = 0
    # Creating the table
    res = databasefile.fetchemployees()
    for i in range(0, len(res)):
        result = res[i]
        if counter % 2 == 0:
            employeetable.insert(parent='', index='end', iid=str(i), values=result, tags=('even',))
        else:
            employeetable.insert(parent='', index='end', iid=str(i), values=result, tags=('odd',))
        counter += 1
    employeetable.grid(row=0, column=1, rowspan=5, sticky='new', pady=30, padx=40)
    updtempl = tk.Button(employees, text='Update Employee', command=lambda: updempl(user), height=1, width=15,
                         font='Raleway', cursor='hand2')
    updtempl.configure(bg=blue, fg=white, activebackground=blue, activeforeground=white)
    updtempl.grid(row=0, column=0, pady=30, padx=20)

    if databasefile.isadmin(user[0]):
        dltempl = tk.Button(employees, text='Delete', command=lambda: deleteempl(user), height=1, width=15,
                            font='Raleway', cursor='hand2')
        dltempl.configure(bg=red, fg=white, activebackground=red, activeforeground=white)
        dltempl.grid(row=1, column=0, pady=30, padx=20)
        backempl = tk.Button(employees, text='Back', command=lambda: load_adminpanel(user), height=1, width=15,
                             font='Raleway',
                             cursor='hand2')
        backempl.grid(row=3, column=0, pady=417, padx=20)
    else:
        backempl = tk.Button(employees, text='Back', command=lambda: load_adminpanel(user), height=1, width=15,
                             font='Raleway', cursor='hand2')
        backempl.grid(row=3, column=0, pady=513, padx=20)


# Creating update employee pop up
def updempl(user):
    if employeetable.focus() != "" and employeetable.item(employeetable.focus()).get('values')[7] != 'ADMIN':
        global empludtpu
        empludtpu = Toplevel()
        empludtpu.title('AAS - Update employee')
        empludtpu.iconbitmap(r'assets/favicon_bl.ico')
        empludtpu.focus_force()
        empludtpu.tkraise()
        empludtpu.configure(background=darkgrey)
        empludtpu.pack_propagate(False)
        empludtpu.geometry('500x500')
        empludtpu.resizable(False, False)

        lbl = tk.Label(empludtpu, text='UID:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl.grid(row=1, column=0, pady=10, padx=20)
        lbl1 = tk.Label(empludtpu, text='First name:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl1.grid(row=2, column=0, pady=10, padx=20)
        lbl2 = tk.Label(empludtpu, text='Last name:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl2.grid(row=3, column=0, pady=10, padx=20)
        lbl3 = tk.Label(empludtpu, text='Email:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl3.grid(row=4, column=0, pady=10, padx=20)
        lbl4 = tk.Label(empludtpu, text='Phone:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl4.grid(row=5, column=0, pady=10, padx=20)
        lbl5 = tk.Label(empludtpu, text='Job position:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl5.grid(row=6, column=0, pady=10, padx=20)
        lbl6 = tk.Label(empludtpu, text='Sector:', bg=darkgrey, fg=white, padx=10, pady=10)
        lbl6.grid(row=7, column=0, pady=10, padx=20)

        # Filling the entrys with employees data
        global eid, efn, eln, eemail, ephone, ejp, esec
        eid = tk.Entry(empludtpu, width=30, bg=white)
        eid.insert(0, employeetable.item(employeetable.focus()).get('values')[0])
        eid.configure(state='disabled')  # Make field read-only
        eid.grid(row=1, column=1, pady=10, padx=20)
        efn = tk.Entry(empludtpu, width=30, bg=white)
        efn.insert(0, employeetable.item(employeetable.focus()).get('values')[1])
        efn.grid(row=2, column=1, pady=10, padx=20)
        eln = tk.Entry(empludtpu, width=30, bg=white)
        eln.insert(0, employeetable.item(employeetable.focus()).get('values')[2])
        eln.grid(row=3, column=1, pady=10, padx=20)
        eemail = tk.Entry(empludtpu, width=30, bg=white)
        eemail.insert(0, employeetable.item(employeetable.focus()).get('values')[3])
        # eemail.configure(state='disabled')
        eemail.grid(row=4, column=1, pady=10, padx=20)
        ephone = tk.Entry(empludtpu, width=30, bg=white)
        ephone.insert(0, employeetable.item(employeetable.focus()).get('values')[4])
        ephone.grid(row=5, column=1, pady=10, padx=20)
        ejp = tk.Entry(empludtpu, width=30, bg=white)
        ejp.insert(0, employeetable.item(employeetable.focus()).get('values')[7])
        ejp.grid(row=6, column=1, pady=10, padx=20)

        egemailbtn = Button(empludtpu, text="Generate email",
                            command=lambda: uemail(), cursor='hand2')
        egemailbtn.grid(row=4, column=2, padx=10)

        sctr = []
        results = databasefile.fetchsectors()
        for result in results:
            data = '%s %s' % (result[0], result[1])
            sctr.append(data)

        esec = ttk.Combobox(empludtpu, values=sctr, width=27, state='readonly')
        for s in sctr:
            if s.startswith(str(employeetable.item(employeetable.focus()).get('values')[8])):
                esec.current(sctr.index(s))
            else:
                pass
        esec.grid(row=7, column=1, pady=20, padx=20)

        updemp = tk.Button(empludtpu, text='Update',
                           command=lambda: employeeupdate(user), height=1, width=10, font='Raleway', cursor='hand2')
        updemp.configure(bg=blue, fg=white, activebackground=blue, activeforeground=white)
        updemp.grid(row=8, column=1, pady=20, padx=20)
        cancelemp = tk.Button(empludtpu, text='Cancel', command=lambda: empludtpu.destroy(), height=1, width=10,
                              font='Raleway', cursor='hand2')
        cancelemp.grid(row=8, column=0, pady=20, padx=20)
    elif employeetable.item(employeetable.focus()).get('values')[7] == 'ADMIN':
        showerror('Error', 'Admin\'s data can not be edited')
    else:
        showerror('Error', 'Select the employee you want to edit and try again')


def employeeupdate(user):
    if not ejp.get().upper() == 'ADMIN':

        try:
            databasefile.updateemployee(eid.get(), efn.get(), eln.get(), eemail.get(), ephone.get(), ejp.get(),
                                        esec.get().split()[0]),
            load_employees(user)
            empludtpu.destroy()
        except sqlite3.Error as e:
            showerror('Error', e)
        # finally:
        #     showerror('Error', 'Something went wrong\nPlease try again')
    else:
        showerror('Error', 'There is already an ADMIN\nChange your job position and try again')



# Delete the selected employee
def deleteempl(user):
    if employeetable.item(employeetable.focus()).get('values')[7] != 'ADMIN':
        try:
            selection = employeetable.item(employeetable.focus()).get('values')[0]  # Grabbing employee's unique id
            databasefile.deleteemployee(selection)
            load_employees(user)
        except sqlite3.Errorc as e:
            showerror('Error', e)
        finally:
            showerror('Error', 'Something went wrong\nPlease try again')
    else:
        showerror('Error', 'Admin can not be deleted')


# Create sector screen
def load_sector(user):
    base.geometry('725x675+' + str(height) + '+' + str(width))
    clear_screen(homescreen)
    sector.tkraise()
    sector.pack_propagate(False)

    # Create table to show the data
    global sectortable  # , sctridentry
    style = ttk.Style()
    style.configure('Treeview',
                    background=white,
                    foreground='black',
                    fieldbackground=white
                    )
    style.map('Treeview', background=[('selected', blue)])
    sectortable = ttk.Treeview(sector)
    sectortable.configure(height=30)
    sectortable['columns'] = ("sid", "name")  # Create columns
    sectortable.column("#0", width=0)  # Phantom column
    sectortable.column("sid", anchor=CENTER, width=100, minwidth=25)
    sectortable.column("name", anchor=W, width=290, minwidth=30)
    # Setting headers
    sectortable.heading("#0", text="", anchor=W)
    sectortable.heading("sid", text="Sector ID", anchor=CENTER)
    sectortable.heading("name", text="Sector Name", anchor=W)

    sectortable.tag_configure('even', background='silver')
    sectortable.tag_configure('odd', background=white)

    counter = 0

    res = databasefile.fetchsectors()
    for i in range(0, len(res)):
        result = res[i]
        if counter % 2 == 0:
            sectortable.insert(parent='', index='end', iid=str(i), values=result, tags=('even',))
        else:
            sectortable.insert(parent='', index='end', iid=str(i), values=result, tags=('odd',))
        counter += 1
    sectortable.grid(row=1, column=1, rowspan=6, sticky='new', pady=30, padx=40)

    insrtsec = tk.Button(sector, text='Insert Sector', command=lambda: insec(user), height=1, width=13, font='Raleway',
                         cursor='hand2')
    insrtsec.configure(bg=green, fg=white, activebackground=green, activeforeground=white)
    insrtsec.grid(row=1, column=0, pady=30, padx=20)
    updsec = tk.Button(sector, text='Update Sector', command=lambda: updtsec(user), height=1, width=13, font='Raleway',
                       cursor='hand2')
    updsec.configure(bg=blue, fg=white, activebackground=blue, activeforeground=white)
    updsec.grid(row=2, column=0, pady=30, padx=20)
    dltsec = tk.Button(sector, text='Delete', command=lambda: deletesec(user), height=1, width=13, font='Raleway',
                       cursor='hand2')
    dltsec.configure(bg=red, fg=white, activebackground=red, activeforeground=white)
    dltsec.grid(row=3, column=0, pady=30, padx=20)
    secback = tk.Button(sector, text='Back', command=lambda: load_adminpanel(user), height=1, width=13, font='Raleway',
                        cursor='hand2')
    secback.grid(row=6, column=0, pady=113, padx=20)
    minutes_spent_week_in_all_sectors_btn = tk.Button(sector, text='Week Sector Stats',
                                                      command=lambda: functionsfile.create_week_graphs(),
                                                      height=1, width=18, font='Raleway', cursor='hand2')
    minutes_spent_week_in_all_sectors_btn.grid(row=4, column=0, pady=30, padx=20)
    hours_spent_year_in_all_sectors_btn = tk.Button(sector, text='Year Sector Stats',
                                                      command=lambda: functionsfile.create_year_graphs(),
                                                      height=1, width=18, font='Raleway', cursor='hand2')
    hours_spent_year_in_all_sectors_btn.grid(row=5, column=0, pady=30, padx=20)


# Delete the selected sector
def deletesec(user):
    # if (len(sctridentry.get()) == 0) and (sectortable.focus() == ""):
    #     showerror('Error', 'Something went wrong\nPlease try again')
    # else if
    try:
        selection = sectortable.item(sectortable.focus()).get('values')[0]  # Grabbing sector's id
        databasefile.deletesector(int(selection))
        load_sector(user)
    except sqlite3.Error:
        showerror('Error', 'There are employees working in this sector\n'
                           'Delete or move them to another sector and try again')
    finally:
        showerror('Error', 'Something went wrong\nPlease try again')


def insec(user):
    global sctrinsrtpu, secnameentry
    sctrinsrtpu = Toplevel()
    sctrinsrtpu.title('AAS - Add new sector')
    sctrinsrtpu.iconbitmap(r'assets/favicon_bl.ico')
    sctrinsrtpu.focus_force()
    sctrinsrtpu.tkraise()
    sctrinsrtpu.configure(background=darkgrey)
    sctrinsrtpu.pack_propagate(False)
    sctrinsrtpu.geometry('350x200+' + str(height + 175) + '+' + str(width + 125))
    sctrinsrtpu.resizable(False, False)
    secnamelbl = tk.Label(sctrinsrtpu, text='New sector\'s name:', bg=darkgrey, fg=white)
    secnamelbl.grid(row=0, column=0, pady=20, padx=10)
    secnameentry = tk.Entry(sctrinsrtpu, width=30)
    secnameentry.grid(row=0, column=1, pady=20, padx=8)
    secnameentry.focus()
    addsector = tk.Button(sctrinsrtpu, text='Add sector', command=lambda: insertsec(user), height=1,
                          width=10, font='Raleway', cursor='hand2')
    addsector.configure(bg=blue, fg=white)
    addsector.grid(row=1, column=1, pady=20, padx=20)
    cancelsector = tk.Button(sctrinsrtpu, text='Cancel', command=lambda: sctrinsrtpu.destroy(), height=1,
                             width=10, font='Raleway', cursor='hand2')
    cancelsector.grid(row=1, column=0, pady=20, padx=15)


def insertsec(user):
    if len(secnameentry.get()) > 0:
        try:
            databasefile.insertsector(secnameentry.get())
            showinfo('Info', 'New sector has been inserted succesfully')
            sctrinsrtpu.destroy()
            load_sector(user)
        except sqlite3.Error:
            showerror('Error', 'Something went wrong\nPlease try again')
    else:
        showerror('Error', 'Please make sure you add a sector name and try again')


# Create sector's update pop up
def updtsec(user):
    global sctrupdtpu, secnameup
    if sectortable.focus() != "":
        sctrupdtpu = Toplevel()
        sctrupdtpu.title('AAS - Update sector')
        sctrupdtpu.iconbitmap(r'assets/favicon_bl.ico')
        sctrupdtpu.focus_force()
        sctrupdtpu.tkraise()
        sctrupdtpu.configure(background=darkgrey)
        sctrupdtpu.pack_propagate(False)
        sctrupdtpu.geometry('350x200+' + str(height + 175) + '+' + str(width + 125))
        sctrupdtpu.resizable(False, False)
        secnamelbl = tk.Label(sctrupdtpu, text='New sector\'s name:', bg=darkgrey, fg=white)
        secnamelbl.grid(row=0, column=0, pady=20, padx=10)
        secnameup = tk.Entry(sctrupdtpu, width=30)
        secnameup.grid(row=0, column=1, pady=20, padx=8)
        secnameup.focus()
        updtsector = tk.Button(sctrupdtpu, text='Update', command=lambda: updatesector(user), height=1, width=10,
                               font='Raleway', cursor='hand2')
        updtsector.configure(bg=blue, fg=white)
        updtsector.grid(row=1, column=1, pady=20, padx=20)
        cancelsector = tk.Button(sctrupdtpu, text='Cancel', command=lambda: sctrupdtpu.destroy(), height=1,
                                 width=10, font='Raleway', cursor='hand2')
        cancelsector.grid(row=1, column=0, pady=20, padx=15)
    else:
        showerror('Error', 'Select a sector first and then try again')


def updatesector(user):
    if len(secnameup.get()) > 0:
        try:
            selection = sectortable.item(sectortable.focus()).get('values')[0]  # Grabbing sector's id
            databasefile.updatesector(selection, secnameup.get().upper())
            showinfo('Info', 'Sector has been updated succesfully')
            sctrupdtpu.destroy()
            load_sector(user)
        except sqlite3.Error:
            showerror('Error', 'Something went wrong\nPlease try again')
    else:
        showerror('Error', 'Please make sure you add a sector name and try again')


# Start application
load_homescreen()

base.mainloop()
