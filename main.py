# -*- coding: iso-8859-1 -*-
import logging, re, time
import threading

from tkinter import (Tk, Label, Frame, Entry, Button, StringVar, PhotoImage, DISABLED, GROOVE, SUNKEN, RAISED,
 W, E, LEFT, RIGHT, CENTER, BOTTOM, X, BOTH, TOP, END)
from tkinter import ttk, filedialog
import tkinter.messagebox as tkmb
import tkinter.simpledialog as tksd
import tkinter.filedialog as tkfd
from Data.send_mail import Mail

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)#, filename="Data\log.txt")

user, status = "", False
to, sbj, message = "", "", ""
files = []
sendBt = None

def exit(event=None):
	logging.debug("Exit button is pressed")
	window.withdraw()
	window.destroy()
	window.quit()

def toggle(event=None):
	emailId.configure(show="") if emailId["show"] == "\u2022" else emailId.configure(show="\u2022")
	logging.info("toggle password to '{}'".format(emailId["show"]))
	emailId.focus()
	window.update()
	return

def send_mail(event=None):
    global to, message, sbj, files, sendBt
    def mail_thread():
        sent_status = user.sendmail(to.get(), sbj.get(), message.get(), files)

    send_mail_thread = threading.Thread(target=mail_thread)
    send_mail_thread.start()
    sendBt['state'] = DISABLED
    reportLabel = ttk.Label(window, text="", background="SkyBlue3", foreground="Green")
    reportLabel.pack()

    while(send_mail_thread.is_alive()):
        reportLabel.configure(text="Sending, please wait")
        window.update()

    sendBt['state'] = 'normal'
    if user.server_status:
        reportLabel.configure(text="Email Sent to {}".format(to.get()))

    else:
        ttk.Label(window, text="Unable to send, retry!", background="SkyBlue3", foreground="Red").pack()

def start_mail(event=None):
    sp_time, w_update = 0, 4
    frame.destroy()
    msg = "WELCOME\nTo EDS\n\nSETTING UP ACCOUNT\nWait!"
    welcmLabel = Label(window, text=msg[0], font=('Helvetica-bold', 22))
    welcmLabel.configure(fg="white")
    welcmLabel.pack(fill=BOTH, expand=True)
    msg_size, left_msg = (len(msg)), (len(msg)-1)
    while(sp_time <= 4):
        time.sleep(1/(10.0**100.0))
        w, h = 340 + w_update, 340 + w_update
        ws, hs = window.winfo_screenwidth(), window.winfo_screenheight()
        x_axis, y_axis = ((ws/2) - (w/2)), ((hs/2) - (h/2))
        window.geometry('%dx%d+%d+%d' % (w, h, x_axis, y_axis))
        window.configure(background="cyan4")
        welcmLabel.configure(background="cyan4")
        window.update()

        if left_msg >= 0:
            welcmLabel.configure(text=msg[0:(msg_size - left_msg)])

        left_msg -= 1
        sp_time += 0.1
        w_update += 4

    window.configure(background="SkyBlue3")
    welcmLabel.configure(background="SkyBlue3")
    time.sleep(1)
    welcmLabel.forget()
    window.update()
    newframe = Frame(window, bg="SkyBlue3")
    newframe.pack(fill=BOTH)
    admin = Label(newframe, image=emailId.image, text=" {0}".format(id), bg="SkyBlue4", fg="limegreen", font=('times', 14), anchor='w')
    admin.configure(bd=2, relief=GROOVE, compound=LEFT)
    admin.pack(side=TOP, ipady=4, pady=1, padx=1, fill=X)
    timelabel = Label(newframe, text=time.strftime('%a %I:%M %p'), font=('times', 14), bg="SkyBlue4", anchor='e', fg="white", bd=0, relief=GROOVE)
    timelabel.place(x=382, y=6)
    window.update()

    global to
    ttk.Label(newframe, text="To:", background="SkyBlue3", font=('times', 12, 'bold')).place(x=75, y=62)
    to = ttk.Entry(newframe, width=45)
    to.pack(pady=20, ipady=4)

    global sbj
    ttk.Label(newframe, text="Sbj:", background="SkyBlue3", font=('times', 12, 'bold')).place(x=75, y=130)
    sbj = ttk.Entry(newframe, width=45)
    sbj.pack(pady=20, ipady=4)

    global message
    ttk.Label(newframe, text="Msg:", background="SkyBlue3", font=('times', 12, 'bold')).place(x=70, y=194)
    message = ttk.Entry(newframe, width=45)
    message.pack(pady=15, ipady=4)

    global files
    def att_file(event=None):
        files.append(tkfd.askopenfilename(filetypes=[("All Files", "*.*")]))
        attLabel.configure(text="Attachments = {}".format(len(files)))

    attbt = ttk.Button(newframe, text="Attachment", image=imgAtt, command=att_file, width=5)
    attbt.place(x=400, y=190)

    attLabel = ttk.Label(newframe, text="Attachments = {}".format(len(files)), background="SkyBlue3", foreground="white", font=('times', 12))
    attLabel.place(x=270, y=220)

    global sendBt
    sendBt = ttk.Button(newframe, image=imgSend, command=send_mail, width=20)
    sendBt.pack(pady=50, ipadx=20)

def met_valid(*args):
	pattern = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
	exp = emailId.get()

	if (" " in exp) and (emailLabel['text'] == "Email  \t\t\t\t"):
		loginBt['state'], passLabel['state'] = DISABLED, DISABLED
		return

	elif (re.match(pattern, exp) == None) and (emailLabel['text'] == "Email  \t\t\t\t"):
		loginBt['state'], passLabel['state'] = DISABLED, DISABLED
		return

	else:
		loginBt['state'], passLabel['state'] = 'normal', 'normal'
		return

def validatePass(event=None):
	passw = emailId.get()
	if (passw == ""):
		logging.warn("bad request for password validation!")
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter a password\t\t\t", fg="red")
		emailId.delete(0, END)
		emailId.focus()
		window.update()
		return

	else:
		logging.info("password received and validated!")
		emailLabel.configure(fg='black')
		warnLabel.configure(text="Connecting, please wait   \t\t", fg="black")
		window.update()

		def start_server_thread():
			global user
			user = Mail(id, passw)

		server_thread = threading.Thread(target=start_server_thread)
		server_thread.start()
		time.sleep(0.25)
		window.update()

		if server_thread.is_alive():
			logging.debug("server status : {0} \nDEBUG:thread status : {1}".format(user, server_thread))
			s_time, gf, gf_i = 1, "\u2022", 1

			while(server_thread.is_alive()):
				warnLabel.configure(text="Connecting, please wait {}     \t".format(gf * gf_i), fg="lightgreen")
				window.update()
				time.sleep(0.15)
				gf_i = (gf_i + 1) if (gf_i < 5) else (gf_i - 4)

			logging.debug("server status : {0} \nDEBUG:thread status : {1}".format(user, server_thread))

			try:
				status, service_status = user.server_status, user.start_service
				if status == True:
					warnLabel.configure(text="Connected\t\t\t", fg="green")
					window.update()
					return start_mail()

				elif service_status == True:
					warnLabel.configure(text="Incorrect password\t\t", fg="red")
					window.update()
					del server_thread
					emailId.select_range(0, END)
					emailId.focus()
					return #start_mail()

				else:
					warnLabel.configure(text="Connection Error, try again\t\t", fg="red")
					window.update()
					del server_thread
					emailId.select_range(0, END)
					emailId.focus()
					return #start_mail()

			except Exception as exp:
				logging.error("Exception : {}".format(exp))
				warnLabel.configure(text="Connection Error, try again\t\t", fg="red")
				window.update()
				del server_thread
				emailId.select_range(0, END)
				emailId.focus()
				return #start_mail()

		else:
			warnLabel.configure(text="No internet connection\t\t", fg="red")
			window.update()
			del server_thread
			emailId.select_range(0, END)
			emailId.focus()
			return #start_mail()

def validateId(event=None):
	global id
	id = emailId.get()
	pattern = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"

	if (id.isspace()) or (id == ""):
		logging.warn("bad request for email validation!")
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter an email\t\t\t")
		emailId.delete(0, END)
		emailId.focus()
		window.update()
		return

	elif (re.match(pattern, id)):
		info = id.split("@")
		logging.info("email '{}' validated using regular expressions".format(id))
		#avatarlabel
		imageLabel.configure(image=imgAvatar)
		passLabel.configure(image=emailId.image2, command=toggle)
		passLabel.bind("<Return>", toggle)
		time.sleep(0.3)

		emailLabel.configure(fg='black')
		warnLabel.configure(text="")
		welcomeLabel.configure(text="\u2022 {}\n\nWelcome\n{}".format(info[1].upper(), info[0]))

		emailLabel.configure(text="Enter your password\t\t")
		emailId.configure(show="\u2022", font=('times', 12, 'bold'))
		emailId.delete(0, END)
		emailId.focus()
		emailId.bind("<Return>", validatePass)
		loginBt.configure(command=validatePass)
		loginBt.bind("<Return>", validatePass)
		window.update()
		return

	else:
		logging.warn("bad request for email validation : '{}'".format(id))
		emailLabel.configure(fg='red')
		warnLabel.configure(text="Enter a valid email\t\t\t")
		emailId.select_range(0, END)
		emailId.focus()
		window.update()
		return

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

img = PhotoImage(file="img/icon.png")
window.tk.call('wm', 'iconphoto', window._w, img)

frame = Frame(window, bg="SkyBlue3", bd=2, colormap="new", relief=SUNKEN)
frame.pack(fill=BOTH)

#welcome label
welcomeLabel = Label(frame, text="Welcome To Mailing Service!\n\nSign in\nwith your Email Account", fg="white", bg="cyan4", anchor=CENTER, font=('times', 14), bd=3, relief=SUNKEN)
welcomeLabel.pack(fill=BOTH, padx=4, pady=20, ipady=20)

#iconlabel
imgWeb = PhotoImage(file="img/web.png")
imgAvatar = PhotoImage(file="img/avatar.png")
imgSend = PhotoImage(file="img/document-send.png")
imgAtt = PhotoImage(file="img/attachment.png")
imageLabel = Label(frame, image=imgWeb, bg="cyan4")
imageLabel.place(x=16, y=60)

#userid label
emailLabel = Label(frame, text="Email  \t\t\t\t", bg="SkyBlue3", font=('times', 11))
emailLabel.pack(padx=0, pady=0, ipadx=36, ipady=0, fill=BOTH)

#userid entry
valid = StringVar()
valid.trace('w', met_valid)
emailId = Entry(frame, font=('times', 12), bg="white", fg="black", textvariable=valid)
emailId.image = PhotoImage(file="img/sAvatar.png")
emailId.image2 = PhotoImage(file="img/pass.png")
passLabel = Button(frame, image=emailId.image, bg="white", bd=0, command=validateId)
passLabel.place(x=266, y=204)
passLabel.bind("<Return>", validateId)
emailId.pack(padx=10, ipadx=34, ipady=4, pady=2)
emailId.focus()
emailId.bind("<Return>", validateId)

#warning label
warnLabel = Label(frame, text="", bg="SkyBlue3", fg='red', font=('times', 11))
warnLabel.pack(padx=0, pady=0, ipadx=36, ipady=0, fill=BOTH)

# login button
ttk.Style().configure("TButton", padding=2, borderwidth=2, relief=RAISED, foreground="grey1", background="cyan4", font=('times', 12, 'italic'))
loginBt = ttk.Button(frame, text="Next", command=validateId, state=DISABLED)
loginBt.pack(side=RIGHT, padx=60, pady=12, ipadx=8)
loginBt.bind("<Return>", validateId)

#copyright status bar
status = Label(window, text="Faizanf33 EDS {} 2018".format(chr(0xa9)), bd=2, relief=SUNKEN, anchor=CENTER, bg="SkyBlue4", fg="white")
status.pack(side=BOTTOM, fill=BOTH, ipady=5)
window.mainloop()
