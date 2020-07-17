import smtplib
import ssl
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText


class Mailer:
    def __init__(self, smtp_config):
        self._smtp_username = smtp_config.get('login')
        self._stmp_password = smtp_config.get('password')
        self._encryption = smtp_config.get('encryption')
        self._smtp_address = smtp_config.get('smtp')
        self._smtp_port = smtp_config.get('port')
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

    def _compose_mail(self, sender_address, mail_body):
        def _generate_mail_subject():
            return '占い・{}'.format(datetime.today().strftime("%Y/%m/%d"))

        composed_mail = MIMEText(mail_body.encode('utf-8'), 'plain', 'utf-8')

        composed_mail['From'] = sender_address
        composed_mail['Subject'] = Header(_generate_mail_subject(), 'utf-8')
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
