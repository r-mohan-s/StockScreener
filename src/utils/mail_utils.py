from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import smtplib
from datetime import date


def send_mail_with_attachment(file_name="blank.csv"):
    today = date.today()

    message = MIMEMultipart()
    message["from"] = "Mohan Subramani"
    message["to"] = "rsmohan.0812@gmail.com"
    message["subject"] = "Buy list for "+str(today)

    # open the file to be sent
    attachment = open(file_name, "rb")

    # instance of MIMEBase and named as p
    p = MIMEBase('application', 'octet-stream')

    # To change the payload into encoded form
    p.set_payload((attachment).read())

    # encode into base64
    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % file_name)

    # attach the instance 'p' to instance 'msg'
    message.attach(p)

    with smtplib.SMTP(host="smtp.gmail.com", port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login("mohancando123@gmail.com", "5102921851")
        smtp.send_message(message)
        print("Mail sent")
