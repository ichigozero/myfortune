import smtplib
from datetime import datetime
from email.header import Header
from email.mime.text import MIMEText


class Mailer:
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
