from PIL import Image, ImageDraw, ImageFont


def fill_event_form(input_path, output_path, data):

    image = Image.open(input_path).convert("RGB")
    draw = ImageDraw.Draw(image)

    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial.ttf",
            14
        )
    except:
        font = ImageFont.load_default()

    # ==================================================
    # PARTICIPANT INFORMATION
    # ==================================================

    # Full Name box: x=33-401, y=307-341
    draw.text(
        (38, 315),
        data.get("full_name", ""),
        fill="black",
        font=font
    )

    # DOB box: x=420-618, y=307-341
    # Cover the placeholder first
    draw.rectangle(
        (423, 309, 580, 338),
        fill="white"
    )

    draw.text(
        (430, 315),
        data.get("dob", ""),
        fill="black",
        font=font
    )

    # Phone box: x=204-401, y=379-414
    draw.text(
        (210, 388),
        data.get("phone", ""),
        fill="black",
        font=font
    )

    # Email box: x=420-618, y=384-419
    draw.text(
        (426, 393),
        data.get("email", ""),
        fill="black",
        font=font
    )

    # ==================================================
    # GENDER
    # ==================================================

    gender = data.get("gender", "").lower()

    # Radio button centers:
    # Male   = (39, 390)
    # Female = (39, 418)

    if gender == "male":
        draw.text(
            (32, 382),
            "●",
            fill="black",
            font=font
        )

    elif gender == "female":
        draw.text(
            (32, 410),
            "●",
            fill="black",
            font=font
        )

    # ==================================================
    # WHERE DID YOU HEAR ABOUT THIS EVENT?
    # ==================================================

    source = data.get("source", "").lower()

    # Radio button centers
    source_positions = {
        "facebook": (32, 474),
        "youtube": (128, 474),
        "instagram": (214, 474),
        "twitter": (311, 474),
        "other": (388, 474)
    }

    if source in source_positions:

        x, y = source_positions[source]

        draw.text(
            (x, y),
            "●",
            fill="black",
            font=font
        )

    # If "Other" was selected, put the text inside its box
    if source == "other":

        draw.text(
            (455, 474),
            data.get("other_source", ""),
            fill="black",
            font=font
        )

    # ==================================================
    # NUMBER OF TICKETS
    # ==================================================

    draw.text(
        (38, 601),
        data.get("tickets", ""),
        fill="black",
        font=font
    )

    # ==================================================
    # PAYMENT METHOD
    # ==================================================

    payment = data.get("payment", "").lower()

    payment_positions = {
        "credit card": (255, 593),
        "debit card": (358, 593),
        "cash": (457, 593),
        "check": (527, 593)
    }

    if payment in payment_positions:

        x, y = payment_positions[payment]

        draw.text(
            (x, y),
            "●",
            fill="black",
            font=font
        )

    # ==================================================
    # AGREEMENT
    # ==================================================

    if data.get("agreement") == "yes":

        draw.text(
            (32, 719),
            "●",
            fill="black",
            font=font
        )

    # ==================================================
    # DATE SIGNED
    # ==================================================

    # Cover the existing mm/dd/yyyy placeholder
    draw.rectangle(
        (414, 712, 580, 742),
        fill="white"
    )

    draw.text(
        (420, 718),
        data.get("date_signed", ""),
        fill="black",
        font=font
    )

    # ==================================================
    # SIGNATURE
    # ==================================================
    # Intentionally left blank.
    # We should capture the user's real signature separately.

    # ==================================================
    # SAVE
    # ==================================================

    image.save(output_path)

    return output_path