import os
from dotenv import load_dotenv
from twilio.rest import Client
import smtplib

# Using a .env file to retrieve the phone numbers and tokens.

load_dotenv()

class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    def __init__(self):
        self.twilio_virtual_number = os.getenv('TWILIO_VIRTUAL_NUMBER')
        self.twilio_verified_number = os.environ["TWILIO_MY_NUMBER"]
        self.smtp_address = "smtp.gmail.com"
        self.email = os.environ["MY_EMAIL"]
        self.email_password = os.environ["MY_EMAIL_PASSWORD"]
        # Set up Twilio Client and SMTP connection
        self.client = Client(os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN"))
        self.connection = smtplib.SMTP(self.smtp_address)

    def send_emails(self, email_list, email_body):
        with self.connection as connection:
            connection.starttls()
            connection.login(user=self.email, password=self.email_password)
            for user_email in email_list:
                connection.sendmail(
                    from_addr=self.email,
                    to_addrs=user_email,
                    msg=f"Subject:New Low Price Flight!\n\n{email_body}".encode('utf-8')
                )

    def send_sms(self, message_body):
        """
        Sends an SMS message through the Twilio API.
        This function takes a message body as input and uses the Twilio API to send an SMS from
        a predefined virtual number (provided by Twilio) to your own "verified" number.
        It logs the unique SID (Session ID) of the message, which can be used to
        verify that the message was sent successfully.
        Parameters:
        message_body (str): The text content of the SMS message to be sent.
        Returns:
        None
        Notes:
        - Ensure that `TWILIO_VIRTUAL_NUMBER` and `TWILIO_VERIFIED_NUMBER` are correctly set up in
        your environment (.env file) and correspond with numbers registered and verified in your
        Twilio account.
        - The Twilio client (`self.client`) should be initialized and authenticated with your
        Twilio account credentials prior to using this function when the Notification Manager gets
        initialized.
        """
        #f"{os.getenv('TWILIO_VIRTUAL_NUMBER')}"
        message = self.client.messages.create(
            from_=self.twilio_virtual_number,
            to=self.twilio_verified_number,
            body=message_body

        )
        # Prints if successfully sent.
        print(message.sid)
