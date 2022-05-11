import os
import smtplib


def send_email(message, recepientMail):

    EMAIL_ADDRESS = "manik071299@gmail.com"
    EMAIL_PASSWORD ="manikpassword"

    # Mail server to use, Port number to connect
    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        # Identifies ourself with the mail server
        smtp.ehlo()
        # Encrypt the traffic
        smtp.starttls()
        smtp.ehlo()

        # Login to the mail server
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

        subject = "Quiz Responses"
        body = str(message)

        msg = f"Subject : {subject}\n\n{body}"
        recipients = [recepientMail]

        # SENDER, RECEIVER, MESSAGE
        smtp.sendmail(EMAIL_ADDRESS, recipients, msg)

        return {"message" : "Email sent to recipient."}