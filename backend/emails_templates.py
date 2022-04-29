import smtplib, ssl
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import os


class Email():
    def __init__(self, smtp_server, sender, password):
        self.smtp_server = smtp_server
        self.port = 587
        self.sender = sender
        self.password = password

    #context = ssl.create_default_context()
    def format_list_emails_to_string(self, list_emails):
        string_emails = list_emails.__repr__()[1:-1].replace("'", '').replace('"', '')
        return string_emails

    def attach(self, message, path_file):
        with open(path_file, 'rb') as file:
            part = MIMEApplication(file.read(), Name=os.path.basename(path_file))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(path_file)}"'
        message.attach(part)
        return

    def create_message(self, receivers, subject, body, path_files=[], assinatura=None, html=True):
        message = MIMEMultipart()
        # HEADER
        message["From"] = self.sender
        receivers.append(self.sender)
        message["To"] = ', '.join(receivers)
        message["Subject"] = subject
        # message["Bcc"] = self.receiver #Com cópia oculta
        # BODY
        if html == True:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))
        for path_file in path_files:
            self.attach(message, path_file)

        if assinatura !=None:
            with open(assinatura, 'rb') as img:
                assinatura = MIMEImage(img.read())
            message.attach(assinatura)
        else:
            pass
        return message

    def send_email(self, message):

        context = ssl._create_unverified_context()
        #context = ssl.create_default_context()
        with smtplib.SMTP(self.smtp_server, self.port) as server:
            server.starttls(context=context)
            #server.ehlo('Thiago Martins')
            server.login(self.sender, self.password)
            server.sendmail(message['From'], message['To'].split(), message.as_string())
        return

def TEST_confirming_email(receivers):
    sender = 'devloot2@gmail.com'
    password = 'jw8mEBTM4ZuJ9gv'

    smtp_server = 'smtp.gmail.com'
    subject = 'E-mail Subject test'
    body = """
<html>
<body>
<h2>Prezado cliente,</h2><br>
<br>
<p>Segue código de verificação 456789</p><br>
<p>email n°123</p><br>
<br>
Atenciosamente,<br>
</body>
</html>
"""
    e_mail = Email(smtp_server=smtp_server, sender=sender, password=password)
    message = e_mail.create_message(receivers, subject, body)
    e_mail.send_email(message)
