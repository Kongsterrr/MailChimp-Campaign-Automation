from flask import Flask, request, render_template, redirect, url_for, session, flash, current_app
from werkzeug.utils import secure_filename
import os
from ParseWord import parse_word_document
from mailchimp import scrape_image_and_caption
from News_Template.MainContent import MainSection
from News_Template.AlsoFeatured import AlsoFeatured
from News_Template.BeforeContent import before_content_html
from News_Template.AfterContent import after_content_html
from mailchimp import campaign_content, create_preview_text, create_campaign, send_test_email
from dotenv import load_dotenv
from CoreEmail import *
from flask import Response
import datetime
from login import *
from flask_jwt_extended import unset_jwt_cookies, get_jwt_identity, get_jwt, jwt_required
import jwt

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

UPLOAD_FOLDER = '/Users/Jack/Desktop/Newsletter/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')  # Change this!
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
app.config['JWT_TOKEN_LOCATION'] = ['cookies']
app.config['JWT_COOKIE_CSRF_PROTECT'] = False
JWT = JWTManager(app)

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)


@app.context_processor
def inject_user_status():
    user_logged_in = False
    jwt_token = request.cookies.get('access_token_cookie')  # The name of your cookie storing the JWT

    if jwt_token:
        try:
            # Decode the JWT using the secret key and verify its authenticity
            decoded = jwt.decode(jwt_token, current_app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            user_logged_in = decoded is not None
        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.DecodeError):
            user_logged_in = False

    return dict(user_logged_in=user_logged_in)

@app.route('/mailchimp', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Get the uploaded file
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            # Parse the uploaded document
            news = parse_word_document(filepath)

            # Get the date input
            date = request.form['date']
            news["Date"] = date

            # Save the news data temporarily (could use session or database)
            session['news_data'] = news

            return redirect(url_for('select_images'))

    return render_template('upload.html')


@app.route('/select_images', methods=['GET', 'POST'])
@login_required
def select_images():
    news = session.get('news_data')
    missing_images = session.pop('missing_images', False)
    if not news:
        return redirect(url_for('upload_file'))

    if request.method == 'POST':
        missing_images = False

        # Process the selected images and indexes
        for index, item in enumerate(news["News"]):
            img_index = request.form.get(f'image_index_{index}')
            if img_index:
                news["News"][index]["Image_Index"] = int(img_index)


        for item in news['News']:
            if 'Image_Index' in item:
                try:
                    img_index = int(float(item['Image_Index'])) - 1
                    img_src, img_script, img_credit = scrape_image_and_caption(item['Content_Link'], img_index)
                    item['Image'] = img_src
                    item['ImageScript'] = img_script
                    item['ImageCredit'] = img_credit

                    if not img_src:
                        missing_images = True

                except ValueError:
                    print(f"Invalid Image_Index for item: {item['Title']}, skipping image parsing.")
            else:
                continue

            # Save updated news with images
        session['news_data'] = news

        if missing_images:
            for reset_item in news['News']:
                if 'Image_Index' in reset_item:
                    del reset_item['Image_Index']
                    del reset_item['ImageScript']
                    del reset_item['ImageCredit']
            session['missing_images'] = True
            return redirect(url_for('select_images'))



        return redirect(url_for('review'))

    return render_template('select_images.html', news=news, enumerate=enumerate, missing_images=missing_images)


@app.route('/review', methods=['GET', 'POST'])
@login_required
def review():
    news = session.get('news_data')
    if request.method == 'POST':
        for index, item in enumerate(news['News']):
            # Handle updated image credit
            new_image_credit = request.form.get(f'image_credit_{index}')
            if new_image_credit:
                item['ImageCredit'] = new_image_credit

        main_section = MainSection(news)
        also_featured_section = AlsoFeatured(news)
        html_content = campaign_content(main_section, also_featured_section, before_content_html, after_content_html)

        # Store the generated HTML content into a file
        with open('test_campaign.html', 'w') as file:
            file.write(html_content)

        # Print message for testing purposes
        print("HTML content has been generated and saved to test_campaign.html")

        subject = news['Subject']
        title = news['Subject']
        preview_text = create_preview_text(news['News'][0])

        campaign_id = create_campaign(
            subject=subject,
            preview_text=preview_text,
            title=title,
            content=html_content
        )
        print(f"Campaign created with ID: {campaign_id}")

        # Send a test email
        test_emails = ['kongsterrr@gmail.com']
        send_test_email(campaign_id, test_emails)


        print(f"Test email sent to {', '.join(test_emails)}")

        return redirect(url_for('success'))

    return render_template('review.html', news=news, enumerate = enumerate)

@app.route('/success')
@login_required
def success():
    return render_template('success.html')


@app.route('/coremail', methods=['GET', 'POST'])
@login_required
def coremail():
    form = EmailForm()
    if form.validate_on_submit():
        csv_file = form.csv_file.data
        csv_filename = secure_filename(csv_file.filename)
        csv_filepath = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        csv_file.save(csv_filepath)

        pdf_file = form.pdf_file.data
        pdf_filepath = None
        if pdf_file:
            pdf_filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(pdf_file.filename))
            pdf_file.save(pdf_filepath)

        session['csv_file_path'] = csv_filepath
        session['pdf_file_path'] = pdf_filepath
        session['pdf_filename'] = form.pdf_filename.data.strip() or (pdf_file.filename if pdf_file else None)
        session['subject'] = form.subject.data
        session['body_template'] = form.body.data
        session['column_name'] = form.column_name.data

        return redirect(url_for('send_emails'))
    return render_template('coremail.html', form=form)


@app.route('/send_emails', methods=['GET'])
@login_required
def send_emails():
    csv_file_path = session.get('csv_file_path')
    pdf_file_path = session.get('pdf_file_path')
    pdf_filename = session.get('pdf_filename')

    # Start the email sending process in the background
    return render_template('sending.html')  # This will render the sending.html page

@app.route('/send_bulk_emails', methods=['GET'])
@login_required
def send_bulk_emails():
    csv_file_path = session.get('csv_file_path')
    pdf_file_path = session.get('pdf_file_path')
    pdf_filename = session.get('pdf_filename')
    column_name = session.get('column_name')

    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = os.getenv('SMTP_PORT')
    sender_email = os.getenv('SENDER_EMAIL')
    sender_password = os.getenv('SENDER_PASSWORD')

    return Response(
        send_bulk_email(
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            sender_email=sender_email,
            sender_password=sender_password,
            csv_file_path=csv_file_path,
            subject=session.get('subject'),
            body_template=session.get('body_template'),
            column_name=column_name,
            pdf_path=pdf_file_path,
            pdf_filename=pdf_filename
        ),
        mimetype='text/event-stream'
    )



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the credentials are correct
        secure_username = os.getenv('USERNAME')
        secure_password = os.getenv('PASSWORD')
        result = authenticate(username, password, secure_username, secure_password)
        if result:
            return result
        else:
            flash('Incorrect username or password. Please try again.', 'error')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    resp = make_response(redirect(url_for('login')))
    unset_jwt_cookies(resp)
    return resp

@app.route('/')
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
