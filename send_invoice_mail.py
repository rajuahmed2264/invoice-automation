import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def send_email(receiver_email, receiver_name, from_date, to_date, pdf_name):
        
    # Email information
    sender_email = 'joyballav@heyremotekitchen.com'
    receiver_email = 'rajua6426@gmail.com'
    password = 'wkdABqXZqYgp4Usl'
    subject = 'Payment Invoice'

    pdf_attachment_path = f'invoices/{pdf_name}'
    
    with open("message_body.txt", "r") as file:
        message = file.read()

    message = message.replace("[Client name]", receiver_name)
    message = message.replace("[start-Date]", from_date)
    message = message.replace("[end-Date]", to_date)
    # Create a multipart message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add body to the email
    msg.attach(MIMEText(message, 'plain'))
    pdf_attachment_path = f'invoices/{pdf_name}'
    with open(pdf_attachment_path, 'rb') as pdf_attachment:
        pdf_part = MIMEApplication(pdf_attachment.read(), Name='file.pdf')
        pdf_part['Content-Disposition'] = f'attachment; filename="{pdf_attachment_path}"'
        msg.attach(pdf_part)
    # Create a secure SSL connection to the SMTP server
    smtp_server = 'smtp.larksuite.com'
    smtp_port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print('Email sent successfully!')

