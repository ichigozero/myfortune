import smtplib
import ssl
import datetime
from email.header import Header
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, smtp_config):
        self._smtp_username = smtp_config['username']
        self._stmp_password = smtp_config['password']
        self._encryption = smtp_config['encryption']
        self._smtp_address = smtp_config['smtp_address']
        self._smtp_port = smtp_config['port']
        self._smtp_server = None

    def send_mail(self, recipients):
        try:
            self._connect_to_smtp_server()

            for recipient in recipients:
                self._smtp_server.sendmail(
                    from_addr=self._smtp_username,
                    to_addrs=recipient['email'],
                    msg=self._compose_mail(
                        sender_address=self._smtp_username,
                        recipient_address=recipient['email'],
                        mail_subject=recipient['subject'],
                        mail_body=recipient['message']
                    )
                )

            self._disconnect_from_smtp_server()
        except (AttributeError, smtplib.SMTPException):
            pass

    def _connect_to_smtp_server(self):
        try:
            context = ssl.create_default_context()

            if self._encryption == 'SSL':
                self._smtp_server = smtplib.SMTP_SSL(
                    self._smtp_address,
                    self._smtp_port,
                    context=context
                )
            else:
                self._smtp_server = smtplib.SMTP(
                    self._smtp_address,
                    self._smtp_port
                )
                self._smtp_server.starttls(context=context)

            self._smtp_server.login(
                user=self._smtp_username,
                password=self._stmp_password
            )
        except smtplib.SMTPException:
            pass

    def _compose_mail(
            self,
            sender_address,
            recipient_address,
            mail_subject,
            mail_body
    ):
        composed_mail = MIMEText(
            _text=mail_body.encode('utf-8'),
            _subtype='plain',
            _charset='utf-8'
        )

        composed_mail['From'] = sender_address
        composed_mail['To'] = recipient_address
        composed_mail['Subject'] = Header(
            s='{}・{}'.format(
                mail_subject,
                datetime.datetime.today().strftime('%Y/%m/%d')
            ),
            charset='utf-8'
        )
        composed_mail['MIME-Version'] = '1.0'
        composed_mail['Content-type'] = 'text/plain; charset="utf-8"'
        composed_mail['Content-Transfer-Encoding'] = 'Base64'

        return composed_mail.as_string()

    def _disconnect_from_smtp_server(self):
        try:
            self._smtp_server.quit()
            self._smtp_server = None
        except (AttributeError, smtplib.SMTPException):
            pass
