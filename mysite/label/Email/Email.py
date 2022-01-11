from django.core.mail import EmailMessage

login = "rafal.kornat@besolux.com"
password ="WeronikaSlawek9*"


class Mail(EmailMessage):
    to = [""]
    cc = ["rafal.trachta@besolux.com","rafal.kornat@besolux.com"]
    bcc = [""]
    message_subject = "Etykiety"
    port = 465 
    smtp_server = "smtp.gmail.com"

    def __init__(self,variant="Labels",text=""):
        if variant == "IT":
            message_subject = "Problems with label3"
            message_text = text
        elif variant == "Labels":
            pass
        message_adress = "From: %s\r\n" % login + "CC: %s\r\n" % ",".join(self.cc)
        message = message_adress + "Subject: %s\r\n" % message_subject+ "\r\n" + message_text


        toaddrs = self.to + self.cc + self.bcc
        