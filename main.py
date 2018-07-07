# -*- coding: iso-8859-1 -*-
import logging, re
from tkinter import *
from tkinter import messagebox

from Data.send_mail import sendmail


window = Tk()
window.title("Email Delivery Service")
# window.geometry("480x480")
window.configure(background="silver")

def exit(event=None):
    logging.debug("Exit button is pressed")
    window.bell()
    window.quit()
    messagebox.showinfo("Closing" , "Thanks for using email service")
    window.destroy()

def hover(event,msg,z,v):      # for showing hovering text over buttons
    global SR
    SR=Label(window,text=msg,bg='grey')
    SR.place(x=z,y=v)


def Main():


    def click(event=None):
        window.bell()
        pattern = r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$"
        sender, passw, receiver, sbj, msg = sender_address.get(), sender_pass.get(), address.get(), subject.get(), message.get()
        if not re.match(pattern, sender):
            logging.warn("Invalid mail address : {}".format(sender))
            window.bell()
            messagebox.showwarning("Invalid Email", "Address : {} is invalid".format(sender))

        elif not re.match(pattern, receiver):
            logging.warn("Invalid mail address : {}".format(receiver))
            messagebox.showwarning("Invalid Email", "Address : {} is invalid".format(receiver))

        else:
            logging.info("Sending mail to={}".format(receiver))
            status = sendmail(sender, passw, receiver, msg, sbj)
            logging.info("status : {}".format(status))
            print("Status:{}".format(status))
            if status == True:
                window.bell()
                messagebox.showinfo("Confirmation", "Your email was successfully sent to {}".format(receiver))

            else:
                window.bell()
                messagebox.showerror("Failed", "Problem occured, try again later!")

     ### my photo
    #photo1 = PhotoImage(file="atm.png")
    #logging.debug("adding photo with background={}".format("black"))
    #Label (window, image=photo1, bg="black") .grid(row=0, column=0, sticky=E)


    Label (window, text="Email").grid(row=0, column=1)
    Label (window, text="Password").grid(row=0, column=2)

    #create a text entry box
    sp=StringVar()
    sp.set('YourEmail@example.com')
    sender_address = Entry(window,textvariable=sp, width=25, bg="white")
    logging.info("creating a text entry box as {}".format(sender_address))
    sender_address.grid(row=1, column=1, sticky=W)

    #create a text entry box
    bullet = "\u2022"

    sender_pass = Entry(window, width=20, bg="white", show=bullet)
    logging.info("creating a text entry box as {}".format(sender_pass))
    sender_pass.grid(row=1, column=2, padx=10, sticky=W)


    #create another label
    logging.debug("creating another label")
    Label (window, text="To : ", bg="silver", fg="dark slate grey", font="none 12 bold") .grid(row=2, column=0, sticky=W)

    #create a text entry box
    ad=StringVar()
    ad.set('ReceiverEmail@exaple.com')
    address = Entry(window,textvariable=ad, width=25, bg="white")
    logging.info("creating a text entry box as {}".format(address))
    address.grid(row=2, column=1, sticky=W)

    #create another label
    logging.debug("creating another label")
    Label (window, text="Subject :", bg="silver", fg="dark slate grey", font="none 12 bold") .grid(row=3, column=0, sticky=W)

    #create a text entry box
    sb=StringVar()
    sb.set('Example')
    subject = Entry(window,textvariable=sb ,width=25, bg="white")
    logging.info("creating a text entry box as {}".format(address))
    subject.grid(row=3, column=1, sticky=W)


    #create another label
    logging.debug("creating another label")
    Label (window, text="Message : ", bg="silver", fg="dark slate grey", font="none 12 bold") .grid(row=4, column=0, sticky=W)

    #create a text entry box
    ms=StringVar()
    ms.set('Message')
    message = Entry(window, textvariable=ms, width=25, bg="white")
    logging.info("creating a text entry box as {}".format(message))
    message.grid(column=1, row=4, columnspan=1, rowspan=3, sticky=N+S)

    #add a send button
    logging.info("adding a button with text={}".format("send"))
    send_bt = Button(window, text="SEND", width=6, command=click)
    send_bt.grid(row=7, column=1, sticky=W)
    send_bt.bind('<Return>', click)
    send_bt.bind('<Enter>',lambda eventt: (hover(eventt,'click to send',400,140)))
    send_bt.bind('<Leave>',  lambda x :(SR.config(text='',bg='silver')))

    #add a submit button
    logging.info("adding a button with text={}".format("Exit"))
    exit_btn = Button(window, text="Exit", width=6, command=exit)
    exit_btn.grid(row=7, column=1, sticky=E)
    exit_btn.bind('<Return>', exit)
    exit_btn.bind('<Enter>',lambda eventt: (hover(eventt,'click to exit',400,190)))
    exit_btn.bind('<Leave>',  lambda x :(SR.config(text='',bg='silver')))

    #copyright status bar
    status = Label(text="{} Copyright 2018".format(chr(0xa9)), relief=SUNKEN, anchor=W)
    status.grid(row=8, column=0, columnspan=3, sticky=E)

    window.mainloop()


Main()
