from News_Template.MainContent import MainSection
from News_Template.AlsoFeatured import AlsoFeatured
from News_Template.BeforeContent import before_content_html
from News_Template.AfterContent import after_content_html
import mailchimp_marketing as MailchimpMarketing
from mailchimp_marketing.api_client import ApiClientError
from bs4 import BeautifulSoup
import requests
import pytz
from ParseWord import parse_word_document
from dotenv import load_dotenv
import os


load_dotenv()

LIST_ID = os.getenv('MAILCHIMP_LIST_ID')
API_KEY = os.getenv('MAILCHIMP_API_KEY')
SERVER = os.getenv('MAILCHIMP_SERVER')

CLIENT = MailchimpMarketing.Client()
CLIENT.set_config({
    "api_key": API_KEY,
    "server": SERVER
})

def create_campaign(subject, preview_text, title, content):
    """Create a new campaign."""
    campaign_info = {
        "type": "regular",

        "recipients": {
            "list_id": LIST_ID,
            "segment_opts": {
                "match": "all",
                "conditions": [
                    {
                        "condition_type": "EmailAddress",
                        "op": "is",
                        "field": "merge0",
                        "value": "yjn0710@bu.edu"
                    }
                ]
            }
        },
        "settings": {
            "subject_line": subject,
            "preview_text": preview_text,
            "title": title,
            "from_name": "China Daily USA",
        },
    }

    campaign = CLIENT.campaigns.create(campaign_info)
    campaign_id = campaign['id']

    CLIENT.campaigns.set_content(campaign_id, {"html": content})

    return campaign_id


def campaign_content(mainsection, featuredsection, before_content_html, after_content_html):
    html_content = before_content_html + mainsection + featuredsection + after_content_html
    return html_content


def create_preview_text(news_item):
    preview_text = f"{news_item['Content_TextBeforeLink']}{news_item['Content_TextToLink']}{news_item['Content_TextAfterLink']}"

    if len(preview_text) > 150:
        truncated_text = preview_text[:146].rsplit(' ', 1)[0]
        preview_text = truncated_text + " ..."

    return preview_text


def send_test_email(campaign_id, test_emails):
    """Send a test email for the campaign."""
    CLIENT.campaigns.send_test_email(campaign_id, {'test_emails': test_emails, 'send_type': 'html'})

# def send_campaign(campaign_id):
#     response = CLIENT.campaigns.send(campaign_id)
#     return response


def schedule_campaign(campaign_id, send_time):
    # Define the EST timezone
    est = pytz.timezone('America/New_York')

    # Localize the send_time to EST
    localized_send_time = est.localize(send_time)

    # Convert the localized time to UTC
    utc_send_time = localized_send_time.astimezone(pytz.utc)

    # Format the UTC time in ISO 8601 format
    send_time_iso = utc_send_time.strftime('%Y-%m-%dT%H:%M:%S') + "+00:00"

    try:
        response = CLIENT.campaigns.schedule(campaign_id, {
            "schedule_time": send_time_iso
        })
        return response
    except ApiClientError as error:
        print(f"An error occurred while scheduling the campaign: {error.text}")
        return None


def scrape_image_and_caption(content_link, img_index):
    def get_image_and_caption(soup):
        content_div = soup.find('div', id='Content')
        if content_div:
            img_tags = content_div.find_all('img')

            if img_tags:
                img_tag = img_tags[0]
                img_src = img_tag['src']
                img_src = "https:" + img_src
            else:
                img_src = None
        else:
            img_src = None

        # Find the corresponding figcaption tag
        figcaption_tag = soup.find('figcaption')
        if figcaption_tag:
            img_script = figcaption_tag.get_text(strip=True)

            # Attempt to find the image credit within square brackets
            last_bracket_index = img_script.rfind(']')
            if last_bracket_index != -1:
                start_bracket_index = img_script.rfind('[', 0, last_bracket_index)
                if start_bracket_index != -1:
                    img_credit = img_script[start_bracket_index + 1:last_bracket_index].strip()
                    img_credit = img_credit.replace("/", " / ").replace("[", "").replace("]", "").upper()
                    # Remove the image credit part from the image script
                    img_script = img_script[:start_bracket_index].strip()
                else:
                    img_credit = None
            else:
                # Find the last period in the img_script
                last_period_index = img_script.rfind('.')
                if last_period_index != -1:
                    img_credit = img_script[last_period_index + 1:].strip()
                    img_credit = img_credit.replace("/", " / ").replace("[", "").replace("]", "").upper()
                    # Remove the image credit part from the image script
                    img_script = img_script[:last_period_index + 1].strip()
                else:
                    img_credit = None
        else:
            img_script = None
            img_credit = None

        return img_src, img_script, img_credit

    try:
        # Adjust the content link if img_index is greater than 1
        if img_index > 1:
            content_link = content_link.replace('.html', f'_{img_index}.html')

        # Send a GET request to the URL
        response = requests.get(content_link)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')

        # Attempt to get image and caption
        img_src, img_script, img_credit = get_image_and_caption(soup)

        return img_src, img_script, img_credit

    except requests.RequestException as e:
        print(f"Error while fetching the content from {content_link}: {e}")
        return None, None, None


def main():
    news = parse_word_document('/Users/Jack/desktop/newsletter1.docx')
    news["Date"] = "August 14, 2024"
    news["News"][0]["Image_Index"] = 1
    news["News"][2]["Image_Index"] = 1
    news["News"][4]["Image_Index"] = 4
    news["News"][6]["Image_Index"] = 1

    for item in news['News']:
        if 'Image_Index' in item:
            try:
                img_index = int(float(item['Image_Index']))
                img_src, img_script, img_credit = scrape_image_and_caption(item['Content_Link'], img_index)
                item['Image'] = img_src
                # print(item['Image'])
                item['ImageScript'] = img_script
                item['ImageCredit'] = img_credit
            except ValueError:
                print(f"Invalid Image_Index for item: {item['Title']}, skipping image parsing.")
        else:
            continue
    print(news)

    main_section = MainSection(news)
    also_featured_section = AlsoFeatured(news)
    html_content = campaign_content(main_section, also_featured_section, before_content_html, after_content_html)

    # Store the generated HTML content into a file
    with open('test_campaign.html', 'w') as file:
        file.write(html_content)

    # Print message for testing purposes
    print("HTML content has been generated and saved to test_campaign.html")

    # subject = news['Subject']
    # title = news['Subject']
    # preview_text = create_preview_text(news['News'][0])
    #
    # campaign_id = create_campaign(
    #     subject=subject,
    #     preview_text=preview_text,
    #     title=title,
    #     content=html_content
    # )
    # print(f"Campaign created with ID: {campaign_id}")
    #
    # # Send a test email
    # test_emails = ['kongsterrr@gmail.com']
    # send_test_email(campaign_id, test_emails)
    #
    #
    # print(f"Test email sent to {', '.join(test_emails)}")

    # Schedule Time
    # send_time_str = "08-13-2024 4:30 PM"
    # send_time = datetime.strptime(send_time_str, '%m-%d-%Y %I:%M %p')
    # print(send_time)
    # schedule_response = schedule_campaign(campaign_id, send_time)
    #
    # if schedule_response:
    #     print(f"Campaign scheduled for {send_time.strftime('%Y-%m-%d %H:%M:%S EST')}")
    # else:
    #     print("Failed to schedule the campaign.")


if __name__ == "__main__":
    main()