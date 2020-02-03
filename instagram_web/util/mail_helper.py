import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from models.user import User



def mail(user):
    message = Mail(
        from_email='Nextagram_support@gmail.com',
        to_emails=user.email,
        subject='Endorsement Thank you note',
        html_content='<h1>Hello and thank you for supporting this guy!!!</h1>')
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))