import os
import smtplib
import logging

from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders

logging.basicConfig(format="%(levelname)s:%(message)s", level=logging.DEBUG)

def send_mail(fromaddr, password, toaddr, filename, path, sbj="Confirmation mail", msg="TEXT YOU WANT TO SEND"):
	try:
		logging.info("Starting server : smtp.gmail.com")
		server = smtplib.SMTP('smtp.gmail.com', 587)
		server.starttls()

	except Exception as exp:
		logging.warn("While starting server an error occurred!")
		logging.error(exp, "Check your internet connection!")
		return
	
	logging.debug("Server started using port : 587")
	try:
		logging.info("Login using id {} and pass".format(fromaddr))
		server.login(fromaddr, password)
	except:
		logging.error("Incorrect Email-Id/Password")
		return
		
	logging.info("Creating an instance of MIMEMultipart as 'mail'")
	mail = MIMEMultipart()
	
	try:
		logging.info("Adding subject, text and attachments to mail")
		mail['From'] = fromaddr
		mail['To'] = toaddr
		mail['Subject'] = sbj
		 	 
		mail.attach(MIMEText(msg, 'plain'))
		 
		attachment = open(path, "rb")
		 
		part = MIMEBase('application', 'octet-stream')
		part.set_payload((attachment).read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
		 
		mail.attach(part)
		 
		text = mail.as_string()
	
	except Exception as exp:
		logging.warn("While setting up mail error occured")
		logging.error(exp)
		server.sendmail(fromaddr, fromaddr, text="Error: {}".format(exp))
		server.quit()
		return
	
	try:
		logging.info("Sending mail to '{}'".format(toaddr))
		server.sendmail(fromaddr, toaddr, text)
		server.quit()
	except:
		logging.error("While sending mail an error occured!")
		server.quit()
		return

	logging.info("Mail was sent successfully")
	return

logging.info("Searcing for file with '.zip' extention in path : {}".format(os.getcwd()))
for file in os.listdir(os.getcwd()):
	if file.endswith('.zip'):
		filename = file
		logging.info("file '{}' found".format(filename))
		break

	else:
		filename = ""
		continue

if filename != "":
	path = os.path.join(os.getcwd(), filename)
	logging.debug("path to file : {}".format(path))
	
	send_mail("EMAIL_ID", "PASSWORD", "SENDER ADDRESS", filename, path, sbj="Confirmation mail", msg="TEXT YOU WANT TO SEND")

else:
	logging.warn("file not found!\nNo further proceedings.")
