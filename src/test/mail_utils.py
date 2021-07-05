import emails

def send_mail_with_attachment(file_name="blank.csv", data=""):
    message = emails.html(
        html="<h1>My message</h1><strong>I've got something to tell you!</strong>",
        subject="A very important message",
        mail_from="referral.0812@gmail.com",
    )
    message.attach(data=open(file_name),filename=data)

    # Send the email
    r = message.send(
        to="referral.0812@gmail.com",
        smtp={
            "host": "email-smtp.us-east-2.amazonaws.com",
            "port": 587,
            "timeout": 5,
            "user": "AKIA5LPHNNMH6R3GSH7G",
            "password": "BB2mZNvY1vucnTKt62iZGDNQJSlWsjC1G2e3kIv1lCnJ",
            "tls": True,
        },
    )

    # Check if the email was properly sent
    assert r.status_code == 250