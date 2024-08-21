import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import csv
import time
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, FileField
from wtforms.validators import DataRequired


class EmailForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    body = TextAreaField('Body', validators=[DataRequired()])
    csv_file = FileField('CSV File', validators=[DataRequired()])
    pdf_file = FileField('PDF File (Optional)')
    pdf_filename = StringField('PDF Filename (Optional)')
    submit = SubmitField('Send Emails')

def read_recipients(csv_file_path):
    """Read recipients from a CSV file and return a list of dictionaries."""
    recipients = []
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            recipients.append(row)
    return recipients


def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient, subject, body, pdf_path=None, pdf_filename=None):
    try:
        # Set up the server (no encryption on port 25)
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.login(sender_email, sender_password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient['E-mail address']
        msg['Subject'] = subject

        # Attach the body to the email
        msg.attach(MIMEText(body.format(last_name=recipient['Last Name']), 'plain'))

        # Attach the PDF file if provided
        if pdf_path and pdf_filename:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                msg.attach(pdf_attachment)

        # Send the email
        server.sendmail(sender_email, recipient['E-mail address'], msg.as_string())
        print(f"Email sent to {recipient['Last Name']} at {recipient['E-mail address']}")

        # Close the server connection
        server.quit()

    except Exception as e:
        print(f"Failed to send email to {recipient['E-mail address']}: {e}")


def send_bulk_email(smtp_server, smtp_port, sender_email, sender_password, csv_file_path, subject, body_template, pdf_path=None, pdf_filename=None):
    """Send bulk emails to recipients listed in a CSV file."""
    recipients = read_recipients(csv_file_path)
    print(recipients[0].keys())

    for recipient in recipients:
        try:
            send_email(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient=recipient,
                subject=subject,
                body=body_template,
                pdf_path=pdf_path,
                pdf_filename=pdf_filename
            )
            time.sleep(2)
        except smtplib.SMTPException as e:
            print(f"Retrying failed email for {recipient['E-mail address']}...")
            time.sleep(5)  # Wait before retrying
            send_email(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient=recipient,
                subject=subject,
                body=body_template,
                pdf_path=pdf_path,
                pdf_filename=pdf_filename
            )





if __name__ == "__main__":
    # SMTP server configuration
    smtp_server = '103.253.239.168'
    smtp_port = 25  # Standard SMTP port for unencrypted email

    # Email credentials
    sender_email = 'candiceyu@chinadailyusa.com'
    sender_password = 'Yjn071022!'

    # Email content
    subject = 'Invitation to China Daily Vision China Forum on September 12, 2024'
    body_template = '''Dear Professor {last_name},

Commemorating the 45th anniversary of China and the US establishing diplomatic relations, China Daily will host a special Vision China Forum in New York on September 12, 2024. You are cordially invited to attend the Forum to be held at the Asia Society. 

This full-day event promises a wealth of insights and engaging discussions. For further details, please refer to the attached invitation letter. 

Kindly confirm your attendance by replying to this email by August 29, 2024. To help us better accommodate our guests, please indicate whether you will be attending the morning session, the afternoon session, or the entire day. 

We look forward to your participation in this meaningful event. 

Best regards, 

--
Jianing (Candice) Yu
Marketing Assistant
China Daily USA
617-407-7658 | candiceyu@chinadailyusa.com
1500 Broadway, Suite 2800, New York, NY 10036'''

    # CSV file path with recipient details
    csv_file_path = '/Users/Jack/desktop/ProfessorList.csv'

    # Path to the PDF file you want to attach
    pdf_path = '/Users/Jack/desktop/invitationletter.pdf'
    pdf_filename = 'Invitation Letter.pdf'  # The name you want the attachment to have in the email

    # Send bulk emails
    send_bulk_email(
        smtp_server=smtp_server,
        smtp_port=smtp_port,
        sender_email=sender_email,
        sender_password=sender_password,
        csv_file_path=csv_file_path,
        subject=subject,
        body_template=body_template,
        pdf_path=pdf_path,
        pdf_filename=pdf_filename
    )