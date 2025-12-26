# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# from environs import Env

# env = Env()
# env.read_env()

# SMTP_HOST = env("SMTP_HOST")
# SMTP_PORT = env("SMTP_PORT")
# SMTP_USER = env("SMTP_USER")
# SMTP_PASSWORD = env("SMTP_PASSWORD")


def send_email(to: str, title: str, message: str):
    print(f'to = {to}')
    print(f'title = {title}')
    print(f'message = {message}')


    # msg = MIMEMultipart()
    # msg["From"] = SMTP_USER
    # msg["To"] = to
    # msg["Subject"] = subject

    # msg.attach(MIMEText(message, "plain"))

    # with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
    #     smtp.starttls()
    #     smtp.login(SMTP_USER, SMTP_PASSWORD)
    #     smtp.send_message(msg)
