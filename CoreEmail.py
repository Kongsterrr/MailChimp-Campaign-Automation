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
    column_name = StringField('Column Name', validators=[DataRequired()])
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


# def send_email(smtp_server, smtp_port, smtp_username, smtp_password, recipient, subject, body, column_name, pdf_path=None, pdf_filename=None):
#     email = recipient.get('E-mail address') or recipient.get('Email') or recipient.get('email')
#     try:
#         # Set up the server (no encryption on port 25)
#         server = smtplib.SMTP(smtp_server, smtp_port)
#         server.starttls()
#         server.login(smtp_username, smtp_password)
#
#         # Create the email
#         msg = MIMEMultipart()
#         msg['From'] = 'candiceyu@chinadailyusa.com'
#         msg['To'] = email
#         msg['Subject'] = subject
#
#         # Attach the body to the email
#         name = recipient.get(column_name)
#         msg.attach(MIMEText(body.format(name=name), 'plain'))
#
#         # Attach the PDF file if provided
#         if pdf_path and pdf_filename:
#             with open(pdf_path, 'rb') as pdf_file:
#                 pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
#                 pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
#                 msg.attach(pdf_attachment)
#
#         # Send the email
#         server.sendmail('candiceyu@chinadailyusa.com', email, msg.as_string())
#         print(f"Email sent to {name} at {email}")
#
#         # Close the server connection
#         server.quit()
#
#     except Exception as e:
#         print(f"Failed to send email to {email}: {e}")

def send_email(smtp_server, smtp_port, sender_email, sender_password, recipient, subject, body, column_name, pdf_path=None, pdf_filename=None):
    email = recipient.get('E-mail address') or recipient.get('Email') or recipient.get('email')
    try:
        # Set up the server (no encryption on port 25)
        server = smtplib.SMTP(smtp_server, smtp_port)
        # server.starttls()
        server.login(sender_email, sender_password)

        # Create the email
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = email
        msg['Subject'] = subject

        # Attach the body to the email
        name = recipient.get(column_name)
        msg.attach(MIMEText(body.format(name=name), 'plain'))

        # Attach the PDF file if provided
        if pdf_path and pdf_filename:
            with open(pdf_path, 'rb') as pdf_file:
                pdf_attachment = MIMEApplication(pdf_file.read(), _subtype='pdf')
                pdf_attachment.add_header('Content-Disposition', 'attachment', filename=pdf_filename)
                msg.attach(pdf_attachment)

        # Send the email
        server.sendmail(sender_email, email, msg.as_string())
        print(f"Email sent to {name} at {email}")

        # Close the server connection
        server.quit()

    except Exception as e:
        print(f"Failed to send email to {email}: {e}")


def send_bulk_email(smtp_server, smtp_port, sender_email, sender_password, csv_file_path, subject, body_template, column_name, pdf_path=None, pdf_filename=None):
    """Send bulk emails to recipients listed in a CSV file."""
    recipients = read_recipients(csv_file_path)
    print(recipients[0].keys())

    for recipient in recipients:
        name = recipient.get(column_name)
        email = recipient.get('E-mail address') or recipient.get('Email') or recipient.get('email')
        try:
            send_email(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient=recipient,
                subject=subject,
                body=body_template,
                column_name=column_name,
                pdf_path=pdf_path,
                pdf_filename=pdf_filename
            )

            message = f"Email sent to {name} at {email}"
            yield f"data: {message}\n\n"
            time.sleep(2)
        except smtplib.SMTPException as e:
            message = f"Failed to send email to {email}: {e}"
            yield f"data: {message}\n\n"
            print(f"Retrying failed email for {email}...")
            time.sleep(5)  # Wait before retrying
            send_email(
                smtp_server=smtp_server,
                smtp_port=smtp_port,
                sender_email=sender_email,
                sender_password=sender_password,
                recipient=recipient,
                subject=subject,
                body=body_template,
                column_name=column_name,
                pdf_path=pdf_path,
                pdf_filename=pdf_filename
            )
            message = f"Email sent to {name} at {email}"
            yield f"data: {message}\n\n"

# def send_bulk_email(smtp_server, smtp_port, smtp_username, smtp_password, csv_file_path, subject, body_template, column_name, pdf_path=None, pdf_filename=None):
#     """Send bulk emails to recipients listed in a CSV file."""
#     recipients = read_recipients(csv_file_path)
#     print(recipients[0].keys())
#
#     for recipient in recipients:
#         name = recipient.get(column_name)
#         email = recipient.get('E-mail address') or recipient.get('Email') or recipient.get('email')
#         try:
#             send_email(
#                 smtp_server=smtp_server,
#                 smtp_port=smtp_port,
#                 smtp_username=smtp_username,
#                 smtp_password=smtp_password,
#                 recipient=recipient,
#                 subject=subject,
#                 body=body_template,
#                 column_name=column_name,
#                 pdf_path=pdf_path,
#                 pdf_filename=pdf_filename
#             )
#
#             message = f"Email sent to {name} at {email}"
#             yield f"data: {message}\n\n"
#             time.sleep(2)
#         except smtplib.SMTPException as e:
#             message = f"Failed to send email to {email}: {e}"
#             yield f"data: {message}\n\n"
#             print(f"Retrying failed email for {email}...")
#             time.sleep(5)  # Wait before retrying
#             send_email(
#                 smtp_server=smtp_server,
#                 smtp_port=smtp_port,
#                 smtp_username=smtp_username,
#                 smtp_password=smtp_password,
#                 recipient=recipient,
#                 subject=subject,
#                 body=body_template,
#                 column_name=column_name,
#                 pdf_path=pdf_path,
#                 pdf_filename=pdf_filename
#             )
#             message = f"Email sent to {name} at {email}"
#             yield f"data: {message}\n\n"