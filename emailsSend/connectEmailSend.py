import os, dotenv, smtplib, ssl
from email.message import EmailMessage

dotenv.load_dotenv()

def connectEmailSend(user, body):
    EMIAL_ADDRESS = os.getenv("EMAIL")
    EMIAL_PASSWORD = os.getenv("SENHA")

    #Criar e-mail
    msg=EmailMessage()
    msg['Subject'] = body["title"]
    msg['From'] = EMIAL_ADDRESS
    msg['To'] = user.email
    msg.set_content(body["mensagem"])

    context = ssl.create_default_context()

    # Enviar Emial
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(EMIAL_ADDRESS, EMIAL_PASSWORD)
        smtp.send_message(msg)
