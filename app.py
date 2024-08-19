from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from ParseWord import parse_word_document
from main import scrape_image_and_caption
from News_Template.MainContent import MainSection
from News_Template.AlsoFeatured import AlsoFeatured
from News_Template.BeforeContent import before_content_html
from News_Template.AfterContent import after_content_html
from main import campaign_content, create_preview_text, create_campaign, send_test_email
from dotenv import load_dotenv

from dotenv import load_dotenv

from flask import flash
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

UPLOAD_FOLDER = '/Users/Jack/Desktop/Newsletter/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/', methods=['GET', 'POST'])
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
def success():
    return render_template('success.html')


if __name__ == "__main__":
    app.run(debug=True)
