def test_send_mail(monkeypatch, mocker, mailer):
    import smtplib

    smtplib_mock = mocker.MagicMock()
    smtplib_mock.SMTP_SSL = mocker.Mock()
    mocker.patch.object(smtplib, 'SMTP_SSL', smtplib_mock)
    mailer._smtp_server = smtplib.SMTP_SSL()

    spy_smtp_connect = mocker.patch.object(mailer, '_connect_to_smtp_server')
    spy_smtp_send_mail = mocker.spy(mailer._smtp_server, 'sendmail')
    spy_smtp_disconnect = mocker.patch.object(
        mailer,
        '_disconnect_from_smtp_server'
    )

    recipients = [{
        'email': 'foo@localhost',
        'subject': '占い',
        'message': 'Hello World!'
    }]
    mailer.send_mail(recipients)

    spy_smtp_connect.assert_called_once()
    spy_smtp_send_mail.assert_called_once_with(
        from_addr=mailer._smtp_username,
        to_addrs='foo@localhost',
        msg=mailer._compose_mail(
            sender_address=mailer._smtp_username,
            mail_subject='占い',
            mail_body='Hello World!'
        )
    )
    spy_smtp_disconnect.assert_called_once()


def test_compose_mail(monkeypatch, fake_datetime, mailer):
    class MockDatetime:
        def today(*args, **kwargs):
            return fake_datetime

    import datetime

    monkeypatch.setattr(datetime, 'datetime', MockDatetime)

    output = mailer._compose_mail(
        sender_address='john.doe@localhost',
        mail_subject='占い',
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
