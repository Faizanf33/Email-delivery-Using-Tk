# -*- coding: iso-8859-1 -*-
import logging, re
from tkinter import Tk, Label, Frame, Entry, SUNKEN, RAISED, W, E, LEFT, RIGHT, CENTER, BOTTOM, BOTH, TOP, END
from tkinter import ttk, filedialog
import tkinter.messagebox as tkmb
import tkinter.simpledialog as tksd

#from Data.send_mail import sendmail

def exit(event=None):
    logging.debug("Exit button is pressed")
    window.quit()
    window.destroy()

def validatePass(event=None):
	passw = emailId.get()
	if passw == "":
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter a password\t\t\t")
		window.update()
		emailId.focus()

	else:
		emailLabel.configure(fg='black')
		warnLabel.configure(text="")		

def validateId(event=None):
	logging.debug("Validating email or phone")
	id = emailId.get()
	pattern = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
	if id == "":
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter an email or phone number\t")
		window.update()

	elif not re.match(pattern, id):
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter a valid email or phone number  ")
		window.update()

	else:
		info = id.split("@")
		emailLabel.configure(fg='black')
		warnLabel.configure(text="")
		welcomeLabel.configure(text="{}\n\nWelcome\n{}".format(info[1].upper(), info[0]))
		emailLabel.configure(text="Enter your password\t\t")
		emailId.delete(0, END)
		emailId.focus()
		emailId.configure(show="\u2022")
		emailId.bind("<Return>", validatePass)
		loginBt.configure(command=validatePass)
		loginBt.bind("<Return>", validatePass)
		window.update()

########################### SETTING UP WINDOWS ##################################
window = Tk()
window.title("Email Delivery Service")
### Setting up windows geometry
w, h = 360, 340
## to open window in the centre of screen
ws = window.winfo_screenwidth()
hs = window.winfo_screenheight()
x_axis = (ws/2) - (w/2)
y_axis = (hs/2) - (h/2)

window.geometry('%dx%d+%d+%d' % (w, h, x_axis, y_axis))
window.resizable(0,0)

window.configure(background="grey")

frame = Frame(window, bg="SkyBlue3", bd=2, colormap="new", height=(h-20), relief=SUNKEN)
frame.pack(fill=BOTH, side=TOP, padx=0, pady=0, ipadx=0, ipady=0)

#welcome label
welcomeLabel = Label(frame, text="Welcome To Mailing Service!\n\nSign in\nwith your Mail Account", fg="white", bg="cyan4", anchor=CENTER, font=('times', 14), bd=3, relief=SUNKEN)
welcomeLabel.pack(fill=BOTH, padx=4, pady=20, ipady=20)

#userid label
emailLabel = Label(frame, text="Email or phone\t\t\t", bg="SkyBlue3", font=('times', 11))
emailLabel.pack(padx=0, pady=0, ipadx=36, ipady=0, fill=BOTH)

#userid entry
emailId = Entry(frame, font=('times', 12, 'italic'), bg="white", fg="black")
emailId.pack(padx=10, ipadx=34, ipady=4, pady=2)
emailId.focus()
emailId.bind("<Return>", validateId)

#warning label
warnLabel = Label(frame, text="", bg="SkyBlue3", fg='red', font=('times', 11))
warnLabel.pack(padx=0, pady=0, ipadx=36, ipady=0, fill=BOTH)


# login button
ttk.Style().configure("TButton", padding=2, borderwidth=2, relief=RAISED, foreground="grey1", background="cyan4", font=('times', 12, 'italic'))
loginBt = ttk.Button(frame, text="Next", command=validateId)
loginBt.pack(side=RIGHT, padx=60, pady=10, ipadx=8)
loginBt.bind("<Return>", validateId)

#copyright status bar
status = Label(window, text="Faizanf33 Apps {} 2018".format(chr(0xa9)), bd=2, relief=SUNKEN, anchor=CENTER, bg="SkyBlue4", fg="white")
status.pack(side=BOTTOM, fill=BOTH, ipady=2)
window.mainloop()
