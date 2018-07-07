from __future__ import print_function
import logging
from logging import basicConfig as bC
import smtplib

bC(format='[Mail]:[%(asctime)s]:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG, filename='mail.log')

def sendmail(sender_address, sender_pass, address, msg, sbj = "Confirmation Mail"):
    other_address = "faizanahmad33.fa@gmail.com"

    try:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            logging.info("Starting SMTP libraries as server {} using IP {}".format(server, 587))
            server.starttls()
            server.login(sender_address, sender_pass)
            logging.info("Started server using address {}".format(sender_address))
            message = 'Subject: {}\n\n{}'.format(sbj, msg)
            server.sendmail(sender_address, address, message)
            logging.info("Sent mail at address {}".format(address))
            server.quit()
            logging.info("Server closed")
            return True

        except Exception as exp:
            logging.error("While sending mail an error was raised, {}".format(exp))
            server = smtplib.SMTP('smtp.gmail.com', 587)
            logging.info("Starting SMTP libraries again as server {} using IP {}".format(server, 587))
            server.starttls()
            server.login(sender_address, sender_pass)
            logging.info("Started server using address {}".format(sender_address))
            server.sendmail(sender_address, other_address, str(address)+"\n"+str(msg))
            logging.info("Sent mail at address {}".format(other_address))
            server.quit()
            return "____INVALID-MAIL-ADDRESS____"
    except Exception as exp:
        logging.error("While sending mail an error was raised, {}".format(exp))
        return "____CONNECTION-TIMEDOUT_____"
