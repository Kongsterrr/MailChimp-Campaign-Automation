def MainSection(news):

    html_content = ""
    date_html = (
        '<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
        '<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
        '<tbody><tr><td style="padding-left:40px;padding-right:40px;padding-top:0;padding-bottom:9px" class="mceTextBlockContainer">'
        '<div data-block-id="76" class="mceText" id="dataBlockId-76" style="width:100%">'
        f'<p style="text-align: center;" class="last-child">'
        f'<span style="color:rgb(38, 34, 35);"><span style="font-size: 12px"><span style="font-family: \'Times New Roman\', Times, Baskerville, Georgia, serif">{news["Date"]}</span></span></span>'
        '</p></div></td></tr></tbody></table></td></tr>'
    )
    html_content += date_html

    # 👉 the block you want to insert as the 2nd item
    injected_second_block = """
<tr><td style="background-color:transparent;padding-top:12px;padding-bottom:12px;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" class="mceImageBlockContainer" align="center" id="b132"><div><!--[if !mso]><!--></div><a href="https://www.barduschinamusic.org/events/us-china-music-forum-2025" style="display:block" target="_blank" data-block-id="132"><table align="center" border="0" cellpadding="0" cellspacing="0" width="85%" style="border-collapse:separate;margin:0;vertical-align:top;max-width:85%;width:85%;height:auto" role="presentation" data-testid="image-132"><tbody><tr><td style="border:0;border-radius:0;margin:0" valign="top"><img alt="" src="https://mcusercontent.com/ba1a72c67a1a445629b16aaf2/images/9eb37942-a29a-06df-7795-b8573de3e993.png" width="561" height="auto" style="display:block;max-width:100%;height:auto;border-radius:0" class="imageDropZone mceImage"></td></tr></tbody></table></a><div><!--<![endif]--></div><div>
<!--[if mso]>
<a href="https://www.barduschinamusic.org/events/us-china-music-forum-2025"><span class="mceImageBorder" style="border:0;border-width:2px;vertical-align:top;margin:0"><img role="presentation" class="imageDropZone mceImage" src="https://mcusercontent.com/ba1a72c67a1a445629b16aaf2/images/9eb37942-a29a-06df-7795-b8573de3e993.png" alt="" width="561" height="auto" style="display:block;max-width:561px;width:561px;height:auto"/></span></a>
<![endif]-->
</div></td></tr>
""".strip()

    main_news = [item for item in news['News'] if item.get("Section") == "Main"]
    divider_bold = news.get("DividerBold", True)

    for i, item in enumerate(main_news):
        layout = item.get("Layout", "vertical")
        image_placement = item.get("ImagePlacement", "left")

        # Title
        title_html = (
            f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
            f'<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
            f'<tbody><tr><td style="padding-left:50px;padding-right:50px;padding-top:5px;padding-bottom:5px" class="mceTextBlockContainer">'
            f'<div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">'
            f'<h1 style="line-height: 1.25;" class="last-child">'
            f'<span style="font-size: 25px"><span style="font-family: \'Times New Roman\', Times, Baskerville, Georgia, serif">{item["Title"]}</span></span>'
            f'</h1></div></td></tr></tbody></table></td></tr>'
        )

        # Image (vertical layout default)
        if layout == "vertical":
            image_html = ''
            item_image = item.get("Image", "")
            if item_image:
                image_html = (
                    f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:50px;padding-left:50px" class="mceBlockContainer" align="center" valign="top">'
                    f'<span class="mceImageBorder" style="border:0;border-radius:0;vertical-align:top;margin:0">'
                    f'<img data-block-id="{i}" width="560" height="auto" style="width:560px;height:auto;max-width:900px !important;border-radius:0;display:block" alt="" src="{item_image}" role="presentation" class="imageDropZone mceImage"/>'
                    f'</span></td></tr>'
                )

            image_script = item.get("ImageScript", "")
            image_credit = item.get("ImageCredit", "")
            max_line_length = 109
            if image_script and (len(image_script) % max_line_length + len(image_credit) > max_line_length):
                image_credit = f'<br>{image_credit}'

            if image_script or image_credit:
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

            final_html = title_html + image_html + image_script_html + content_html

        else:
            # Horizontal layout (image left/right)
            item_image = item.get("Image", "")
            text_before_link = item.get("Content_TextBeforeLink", "")
            text_after_link = item.get("Content_TextAfterLink", "")

            if image_placement == "left":
                left_content = f"""
                                <td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" data-block-id="{i}" colspan="6" width="50%">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody><tr>
                                            <td style="padding-top:5px;padding-bottom:5px;padding-right:50px;padding-left:50px" valign="top" class="mceImageBlockContainer" align="center" id="blockContainerId-{i}">
                                                <span class="mceImageBorder" style="border:0;border-radius:0;vertical-align:top;margin:0">
                                                    <img data-block-id="{i}" width="195.5" height="auto" style="width:195.5px;height:auto;max-width:195.5px !important;border-radius:0;display:block" alt="" src="{item_image}" role="presentation" class="imageDropZone mceImage">
                                                </span>
                                            </td>
                                        </tr></tbody>
                                    </table>
                                </td>
                            """
                right_content = f"""
                                <td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" data-block-id="{i}" colspan="6" width="50%">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody><tr>
                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" id="blockContainerId-{i}">
                                                <table width="100%" style="border:0;border-radius:0;border-collapse:separate">
                                                    <tbody><tr>
                                                        <td style="padding-left:0;padding-right:50px;padding-top:5px;padding-bottom:5px" class="mceTextBlockContainer">
                                                            <div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">
                                                                <p class="last-child">
                                                                    {text_before_link}
                                                                    <a href="{item["Content_Link"]}" target="_blank">{item["Content_TextToLink"]}</a>
                                                                    {text_after_link}
                                                                </p>
                                                            </div>
                                                        </td>
                                                    </tr></tbody>
                                                </table>
                                            </td>
                                        </tr></tbody>
                                    </table>
                                </td>
                            """
            else:
                left_content = f"""
                                <td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" data-block-id="{i}" colspan="6" width="50%">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody><tr>
                                            <td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top" id="blockContainerId-{i}">
                                                <table width="100%" style="border:0;border-radius:0;border-collapse:separate">
                                                    <tbody><tr>
                                                        <td style="padding-left:50px;padding-right:0;padding-top:5px;padding-bottom:5px" class="mceTextBlockContainer">
                                                            <div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">
                                                                <p class="last-child">
                                                                    {text_before_link}<a href="{item["Content_Link"]}" target="_blank">{item["Content_TextToLink"]}</a>{text_after_link}
                                                                </p>
                                                            </div>
                                                        </td>
                                                    </tr></tbody>
                                                </table>
                                            </td>
                                        </tr></tbody>
                                    </table>
                                </td>
                            """
                right_content = f"""
                                <td style="padding-top:0;padding-bottom:0" valign="top" class="mceColumn" data-block-id="{i}" colspan="6" width="50%">
                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                        <tbody><tr>
                                            <td style="padding-top:5px;padding-bottom:5px;padding-right:50px;padding-left:50px" valign="top" class="mceImageBlockContainer" align="center" id="blockContainerId-{i}">
                                                <span class="mceImageBorder" style="border:0;border-radius:0;vertical-align:top;margin:0">
                                                    <img data-block-id="{i}" width="195.5" height="auto" style="width:195.5px;height:auto;max-width:195.5px !important;border-radius:0;display:block" alt="" src="{item_image}" role="presentation" class="imageDropZone mceImage">
                                                </span>
                                            </td>
                                        </tr></tbody>
                                    </table>
                                </td>
                            """

            final_html = title_html + f"""
                            <tr><td valign="top" class="mceGutterContainer" id="gutterContainerId-{i}">
                                <table border="0" cellpadding="0" cellspacing="0" width="100%" style="border-collapse:separate" role="presentation">
                                    <tbody><tr><td style="padding-top:8px;padding-bottom:8px;padding-right:0;padding-left:0" valign="top" class="mceLayoutContainer" id="blockContainerId-{i}">
                                        <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation" data-block-id="{i}" id="section_{i}" class="mceLayout">
                                            <tbody><tr class="mceRow">
                                                <td style="background-position:center;background-repeat:no-repeat;background-size:cover" valign="top">
                                                    <table border="0" cellpadding="0" cellspacing="0" width="100%" role="presentation">
                                                        <tbody><tr>
                                                            <td valign="top" class="mceColumn" data-block-id="{i}" colspan="12" width="100%">
                                                                <table border="0" cellpadding="0" cellspacing="24" width="100%" style="table-layout:fixed" role="presentation">
                                                                    <colgroup>
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                        <col span="1" width="8.333333333333332%">
                                                                    </colgroup>
                                                                    <tbody><tr>
                                                                        {left_content}
                                                                        {right_content}
                                                                    </tr></tbody>
                                                                </table>
                                                            </td>
                                                        </tr></tbody>
                                                    </table>
                                                </td>
                                            </tr></tbody>
                                        </table>
                                    </td></tr></tbody>
                                </table>
                            </td></tr>
                        """

        # Build divider variants (bold vs thin)
        if divider_bold:
            main_content_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:6px;padding-bottom:6px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="{i}">'
                f'<tbody><tr><td style="min-width:100%;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" valign="top"></td></tr>'
                f'</tbody></table></td></tr>'
            )
        else:
            main_content_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:20px;padding-bottom:20px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="100">'
                f'<tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" '
                f'valign="top"></td></tr></tbody></table></td></tr>'
            )

        end_section_line_html = (
            f'<tr><td style="background-color:transparent;padding-top:20px;padding-bottom:20px;padding-right:50px;padding-left:50px" '
            f'class="mceBlockContainer" valign="top">'
            f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
            f'role="presentation" class="mceDividerContainer" data-block-id="100">'
            f'<tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" '
            f'valign="top"></td></tr></tbody></table></td></tr>'
        )

        # 🔹 Insert the injected block as the 2nd item (right after the first main_news)
        if i == 0:
            if len(main_news) > 1:
                # first article + divider, then injected block + divider (so the 2nd article follows cleanly)
                html_content += final_html + main_content_line_html + injected_second_block + main_content_line_html
            else:
                # only one main item: first article + divider, injected block, then end section line
                html_content += final_html + main_content_line_html + injected_second_block + end_section_line_html
            continue

        # default behavior for the rest
        if i < len(main_news) - 1:
            html_content += final_html + main_content_line_html
        else:
            html_content += final_html + end_section_line_html

    return html_content
