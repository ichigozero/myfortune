def test_compose_mail(mailer):
    output = mailer._compose_mail(
        sender_address='john.doe@localhost',
        mail_body='Hello World!'
    )
    assert output == (
        'Content-Type: text/plain; charset="utf-8"\n'
        'MIME-Version: 1.0\n'
        'Content-Transfer-Encoding: base64\n'
        'From: john.doe@localhost\n'
        'Subject: =?utf-8?b?5Y2g44GE44O7MjAyMC8wNy8xNw==?=\n'
        'MIME-Version: 1.0\n'
        'Content-type: text/plain; charset="utf-8"\n'
        'Content-Transfer-Encoding: Base64\n'
        '\n'
        'SGVsbG8gV29ybGQh\n'
    )
