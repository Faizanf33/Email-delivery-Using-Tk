import os
import logging
import smtplib

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

class Mail:
    ip = 587
    server_status = False

    def __init__(self, user_id, user_pass):
        self.start_service = self.start_service()
        if self.start_service:
            try:
                server = smtplib.SMTP('smtp.gmail.com', self.ip)
                logging.info("Starting SMTP libraries as server {} using ip {}".format(server, self.ip))
                server.starttls()
                server.login(user_id, user_pass)
                logging.info("Started server using address {}".format(user_id))
                self.server_status = True
                self.server = server
                self.user_id = user_id

            except Exception as exp:
                logging.error("____INVALID-ID/PASS____")

        else:
            logging.warn("Unable to start services...")

    @staticmethod
    def start_service():
        try:
            ip = 587
            logging.debug("Testing SMTP libraries as server '{}' using ip '{}'".format("smtp.gmail.com", ip))
            server = smtplib.SMTP('smtp.gmail.com', ip)
            server.starttls()
            return True

        except Exception as exp:
            logging.error("While starting server an error was raised => {}".format(exp))
            return False


    def sendmail(self, address, sbj, msg, files):
        logging.info("Creating an instance of MIMEMultipart as 'mail'")
        mail = MIMEMultipart()

        try:
            logging.info("Adding subject, text and attachments to mail")
            mail['From'] = self.user_id
            mail['To'] = address
            mail['Subject'] = sbj
            mail.attach(MIMEText(msg, 'plain'))

            for path in files:
                attachment = open(path, "rb")
                part = MIMEBase('application', 'octet-stream')
                part.set_payload((attachment).read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', "attachment; filename= {}".format(os.path.split(path)[-1]))
                mail.attach(part)

            message = mail.as_string()

            self.server.sendmail(self.user_id, address, message)
            logging.info("Sent mail at address {}".format(address))
            return (True, "Sent")

        except Exception as exp:
            logging.error("While sending mail error was raised again => {}".format(exp))
            self.server_status = False
            self.server.quit()
            logging.info("Server closed")
            return (False, "____CONNECTION-TIMEDOUT_____")
