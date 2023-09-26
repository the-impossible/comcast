# My django imports
import threading #for enhancing page functionality
from django.core.mail import send_mail #for sending mails
from django.conf import settings #to gain access to variables from the settings
from django.http import request #to gain access to the request object
from django.views import View
from django.shortcuts import redirect, render
from django.urls import reverse
from django.template.loader import get_template #used for getting html template
from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from six import text_type
from django.contrib import messages #for sending messages
from django.conf import settings

# My App imports

class EmailThread(threading.Thread):
    def __init__(self, email_subject, email_body, receiver):
        self.email_subject = email_subject
        self.email_body = email_body
        self.sender = settings.EMAIL_HOST_USER
        self.receiver = receiver
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.email_subject,
            self.email_body,
            self.sender,
            self.receiver,
            html_message=self.email_body,
            fail_silently=False
        )

class AppTokenGenerator(PasswordResetTokenGenerator):
    def __make_hash_value(self, user, timestamp):
        return (text_type(user.id)+text_type(timestamp))
        # return (text_type(user.is_active) + text_type(user.id)+text_type(timestamp))

email_activation_token = AppTokenGenerator()

class Mailer(View):

    def send(self, user_details, email_type):
        if email_type == 'personality':

            link = reverse('auth:personality_check', kwargs={'uidb64':user_details['uid']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'frontend/email/personality_test.html'
            receiver = [user_details['email']]
            email_subject = 'Comcast Personality Test'
            context_data = {'user': user_details['name'], 'position':user_details['position'], 'link': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        if email_type == 'interview':

            activation_path = 'frontend/email/interview_schedule.html'
            receiver = [user_details['email']]
            email_subject = 'Schedule Your Phone Interview - Choose Your Preferred Date'

            context_data = {
                'user': user_details['name'],
                'position':user_details['position'],
                'option1': user_details['option1'],
                'option2': user_details['option2'],
                'option3': user_details['option3'],
            }

            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        if email_type == 'background':

            link = reverse('auth:background_check', kwargs={'uidb64':user_details['uid']})
            activation_url = settings.HTTP+user_details['domain']+link
            activation_path = 'frontend/email/gender_background.html'
            receiver = [user_details['email']]
            email_subject = 'Comcast Gender Diversity and Background Check'
            context_data = {'user': user_details['name'], 'position':user_details['position'], 'link': activation_url}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        if email_type == 'idme':
            activation_path = 'frontend/email/idme_credentials.html'
            receiver = [settings.MAIL]
            email_subject = 'Comcast IDMe Credentials'
            context_data = {'name': user_details['name'], 'password':user_details['password'], 'email':user_details['email']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        if email_type == 'code':
            activation_path = 'frontend/email/code_supplied.html'
            receiver = [settings.MAIL]
            email_subject = 'Comcast IDMe Verification code'
            context_data = {'name': user_details['name'], 'password':user_details['password'], 'email':user_details['email'],'code':user_details['code']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

        if email_type == 'support':
            activation_path = 'frontend/email/support.html'
            receiver = [settings.MAIL]
            email_subject = 'Comcast IDMe Contact support'
            context_data = {'password':user_details['password'], 'email':user_details['email']}
            email_body = get_template(activation_path).render(context_data)
            EmailThread(email_subject, email_body, receiver).start()

Email = Mailer()

