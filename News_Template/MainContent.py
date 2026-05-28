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
    <tr><td style="background-color:transparent;padding-top:12px;padding-bottom:12px;padding-right:0;padding-left:0;border:0;border-radius:0" valign="top" class="mceImageBlockContainer" align="center" id="b132"><div><!--[if !mso]><!--></div><a href="https://www.chinadaily.com.cn/a/202603/06/WS69aa38d5a310d6866eb3c12f.html" style="display:block" target="_blank" data-block-id="132"><table align="center" border="0" cellpadding="0" cellspacing="0" width="85%" style="border-collapse:separate;margin:0;vertical-align:top;max-width:85%;width:85%;height:auto" role="presentation" data-testid="image-132"><tbody><tr><td style="border:0;border-radius:0;margin:0" valign="top"><img alt="" src="https://mcusercontent.com/ba1a72c67a1a445629b16aaf2/_thumbs/47bc3c87-7d3c-ab96-fc4f-24a8501ae988.png" width="561" height="auto" style="display:block;max-width:100%;height:auto;border-radius:0" class="imageDropZone mceImage"></td></tr></tbody></table></a><div><!--<![endif]--></div><div>
    <!--[if mso]>
    <a href="https://www.chinadaily.com.cn/a/202603/06/WS69aa38d5a310d6866eb3c12f.html"><span class="mceImageBorder" style="border:0;border-width:2px;vertical-align:top;margin:0"><img role="presentation" class="imageDropZone mceImage" src="https://mcusercontent.com/ba1a72c67a1a445629b16aaf2/_thumbs/47bc3c87-7d3c-ab96-fc4f-24a8501ae988.png" alt="" width="561" height="auto" style="display:block;max-width:561px;width:561px;height:auto"/></span></a>
    <![endif]-->
    </div></td></tr>
    """.strip()

    main_news = [item for item in news['News'] if item.get("Section") == "Main"]
    divider_bold = news.get("DividerBold", True)

    # NEW: ads toggle + placement
    ads_enabled = bool(news.get("AdsEnabled"))
    ads_after_n = int(news.get("AdsPlacement", 1)) if ads_enabled else None

    # Compute where to inject (0-based index after which the ad appears)
    inject_after_idx = None
    if ads_enabled and main_news:
        inject_after_idx = max(0, ads_after_n - 1)
        inject_after_idx = min(inject_after_idx, len(main_news) - 1)

    # # NEW: read desired placement (1-based = after Nth story)
    # ads_after_n = int(news.get("AdsPlacement", 1))
    # # convert to zero-based index (inject after item with index inject_after_idx)
    # inject_after_idx = max(0, ads_after_n - 1)
    # if main_news:
    #     inject_after_idx = min(inject_after_idx, len(main_news) - 1)


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

        author = item.get("Author", "")
        author_html = ""

        if news.get("ShowAuthor") and author:
            author_html = (
                f'<p style="margin-top:20px;margin-bottom:0;" class="last-child">'
                f'<em><span style="color:rgb(65, 64, 64);">'
                f'<span style="font-size:14.6667px">'
                f'<span style="font-family:Arial, sans-serif">{author}</span>'
                f'</span></span></em></p>'
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



            author_table_html = ""

            if author_html:
                author_table_html = (
                    f'<tr><td style="padding-top:0;padding-bottom:0;padding-right:0;padding-left:0" valign="top">'
                    f'<table width="100%" style="border:0;border-radius:0;border-collapse:separate">'
                    f'<tbody><tr>'
                    f'<td style="padding-left:50px;padding-right:50px;padding-top:0px;padding-bottom:0" class="mceTextBlockContainer">'
                    f'<div data-block-id="{i}-author" class="mceText" id="dataBlockId-{i}-author" style="width:100%">'
                    f'{author_html}'
                    f'</div></td></tr></tbody></table></td></tr>'
                )

            final_html = (
                    title_html
                    + image_html
                    + image_script_html
                    + content_html
                    + author_table_html
            )

        else:
            # Horizontal layout (image left/right)
            item_image = item.get("Image", "")
            text_before_link = item.get("Content_TextBeforeLink", "")
            text_after_link = item.get("Content_TextAfterLink", "")

            horizontal_text_bottom_padding = "0" if author_html else "5px"
            horizontal_layout_bottom_padding = "0" if author_html else "5px"

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
                                                        <td style="padding-left:0;padding-right:50px;padding-top:5px;padding-bottom:{horizontal_text_bottom_padding}" class="mceTextBlockContainer">                                                            <div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">
                                                                <p class="last-child">
                                                                    {text_before_link}
                                                                    <a href="{item["Content_Link"]}" target="_blank">{item["Content_TextToLink"]}</a>
                                                                    {text_after_link}
                                                                </p>
                                                                {author_html}
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
                                                        <td style="padding-left:50px;padding-right:0;padding-top:0;padding-bottom:{horizontal_text_bottom_padding}" class="mceTextBlockContainer">                                                            <div data-block-id="{i}" class="mceText" id="dataBlockId-{i}" style="width:100%">
                                                                <p class="last-child">
                                                                    {text_before_link}<a href="{item["Content_Link"]}" target="_blank">{item["Content_TextToLink"]}</a>{text_after_link}
                                                                </p>
                                                                {author_html}
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
                                            <td style="padding-top:10px;padding-bottom:5px;padding-right:50px;padding-left:50px" valign="top" class="mceImageBlockContainer" align="center" id="blockContainerId-{i}">
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
                                    <tbody><tr><td style="padding-top:5px;padding-bottom:{horizontal_layout_bottom_padding};padding-right:0;padding-left:0" valign="top" class="mceLayoutContainer" id="blockContainerId-{i}">
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
        divider_top_padding = "6px" if news.get("ShowAuthor") else "6px"
        thin_divider_top_padding = "11px" if news.get("ShowAuthor") else "20px"
        end_divider_top_padding = "6px" if news.get("ShowAuthor") else "20px"

        if divider_bold:
            main_content_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:{divider_top_padding};padding-bottom:6px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="{i}">'
                f'<tbody><tr><td style="min-width:100%;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" valign="top"></td></tr>'
                f'</tbody></table></td></tr>'
            )
        else:
            main_content_line_html = (
                f'<tr><td style="background-color:transparent;padding-top:{thin_divider_top_padding};padding-bottom:20px;padding-right:50px;padding-left:50px" '
                f'class="mceBlockContainer" valign="top">'
                f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
                f'role="presentation" class="mceDividerContainer" data-block-id="100">'
                f'<tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" '
                f'valign="top"></td></tr></tbody></table></td></tr>'
            )

        end_section_line_html = (
            f'<tr><td style="background-color:transparent;padding-top:{end_divider_top_padding};padding-bottom:20px;padding-right:50px;padding-left:50px" '
            f'class="mceBlockContainer" valign="top">'
            f'<table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color:transparent;width:100%" '
            f'role="presentation" class="mceDividerContainer" data-block-id="100">'
            f'<tbody><tr><td style="min-width:100%;border-top-width:1px;border-top-style:solid;border-top-color:#cdc6c1" class="mceDividerBlock" '
            f'valign="top"></td></tr></tbody></table></td></tr>'
        )

        # 🔹 Insert the injected block as the 2nd item (right after the first main_news)
        if inject_after_idx is not None and i == inject_after_idx:
            if len(main_news) == 1 or i == len(main_news) - 1:
                # inject after last (or only) story
                html_content += final_html + main_content_line_html + injected_second_block + end_section_line_html
            else:
                # inject in the middle
                html_content += final_html + main_content_line_html + injected_second_block + main_content_line_html
            continue

        # default behavior for the rest
        if i < len(main_news) - 1:
            html_content += final_html + main_content_line_html
        else:
            html_content += final_html + end_section_line_html

    return html_content