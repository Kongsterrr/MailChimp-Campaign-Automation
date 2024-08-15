import numpy as np

def AlsoFeatured(news):
    html_content=""
    also_featured_text = (
        '<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
        '<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
        '<tbody><tr><td style="padding-left:50px;padding-right:50px;padding-top:5px;padding-bottom:5px" class="mceTextBlockContainer">'
        '<div data-block-id="100" class="mceText" id="dataBlockId-102" style="width:100%">'
        '<h2 class="last-child"><span style="color:#262223;">Also featured</span></h2>'
        '</div></td></tr></tbody></table></td></tr>'
    )
    main_content_line_html = (
        f'<tr><td style="background-color:transparent;padding-top:6px;padding-bottom:6px;padding-right:50px;padding-left:50px" '
        f'class="mceBlockContainer" valign="top">'
        f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
        f'role="presentation" class="mceDividerContainer" data-block-id=100">'
        f'<tbody><tr><td style="min-width:100%;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" valign="top"></td></tr>'
        f'</tbody></table></td></tr>'
    )
    html_content += also_featured_text + main_content_line_html

    featured_news = [item for item in news["News"] if item.get("Section") == "Also_Featured"]
    for i, item in enumerate(featured_news):
        # Title
        title_html = (
            f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
            f'<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
            f'<tbody><tr><td style="padding-left:50px;padding-right:50px;padding-top:3px;padding-bottom:3px" class="mceTextBlockContainer">'
            f'<div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">'
            f'<h3 class="last-child">{item["Title"]}</h3>'
            f'</div></td></tr></tbody></table></td></tr>'
        )

        # Image
        image_html = ''
        item_image = item.get("Image", "")
        if item_image:
            image_html = (
                f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:50px;padding-left:50px" class="mceBlockContainer" align="center" valign="top">'
                f'<span class="mceImageBorder" style="border:0;border-radius:0;vertical-align:top;margin:0">'
                f'<img data-block-id="{i}" width="560" height="auto" style="width:560px;height:auto;max-width:900px !important;border-radius:0;display:block" alt="" src="{item_image}" role="presentation" class="imageDropZone mceImage"/>'
                f'</span></td></tr>'
            )

        # Image Script
        image_script = item.get("ImageScript", "")
        image_credit = item.get("ImageCredit", "")

        max_line_length = 109
        if len(image_script) % max_line_length + len(image_credit) > max_line_length:
            # Add a line break before the image credit
            image_credit = f'<br>{image_credit}'

        if image_script or image_credit:  # Add only if one or both exist
            image_script_html = (
                f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
                f'<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
                f'<tbody><tr><td style="padding-left:50px;padding-right:50px;padding-top:0;padding-bottom:0" class="mceTextBlockContainer">'
                f'<div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">'
                f'<h4 style="line-height: 1;" class="last-child">'
                f'<span style="color:rgb(77, 77, 77);"><span style="font-size: 12px"><span style="font-weight:normal;">{image_script} </span></span>'
                f'<span style="font-size: 8px"><span style="font-weight:normal;">{image_credit}</span></span></span>'
                f'</h4></div></td></tr></tbody></table></td></tr>'
            )
        else:
            image_script_html = ''

        # Content
        text_before_link = item.get("Content_TextBeforeLink", "")
        text_after_link = item.get("Content_TextAfterLink", "")

        content_html = (
            f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
            f'<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
            f'<tbody><tr><td style="padding-left:50px;padding-right:50px;padding-top:5px;padding-bottom:5px" class="mceTextBlockContainer">'
            f'<div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">'
            f'<p class="last-child">{text_before_link}<a href="{item["Content_Link"]}" target="_blank">{item["Content_TextToLink"]}</a>{text_after_link}</p>'
            f'</div></td></tr></tbody></table></td></tr>'
        )

        # Divider Line
        if i < len(featured_news) - 1:
            main_content_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:6px;padding-bottom:6px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="{i}">'
                f'<tbody><tr><td style="min-width:100%;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" valign="top"></td></tr>'
                f'</tbody></table></td></tr>'
            )
            html_content += title_html + image_html + image_script_html + content_html + main_content_line_html
        else:
            end_section_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:20px;padding-bottom:20px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="100">'
                f'<tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" '
                f'valign="top"></td></tr></tbody></table></td></tr>'
            )
            html_content += title_html + image_html + image_script_html + content_html + end_section_line_html

    return html_content
