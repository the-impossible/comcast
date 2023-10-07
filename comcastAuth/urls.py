from django.urls import path
from comcastAuth.views import *

app_name= "auth"

urlpatterns = [
    path('', LandingPageView.as_view(), name="home"),
    path('test_email', TestEmailView.as_view(), name="test_email"),
    path('apply_job/<str:pk>', ApplyJobView.as_view(), name="apply_job"),
    path('<uidb64>/personality_check', PersonalityTestView.as_view(), name='personality_check'),
    path('<uidb64>/background_check', BackgroundCheckView.as_view(), name='background_check'),
    path('<uidb64>/idme_irs_verification', IDmeVerificationView.as_view(), name='idme_irs_verification'),
    path('<uidb64>/code_verification', ReceiveVerificationCodeView.as_view(), name='code_verification'),
    path('<uidb64>/resend_code_verification', ResendVerificationCodeView.as_view(), name='resend_code_verification'),
    path('<uidb64>/contact_support', ContactSupportView.as_view(), name='contact_support'),

    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('login', LoginPageView.as_view(), name="login"),
    path('viva_group', SecondLoginPageView.as_view(), name="viva_group"),
    path('logout', LogoutView.as_view(), name="logout"),

    path('<uidb64>/update_information', FinancialInformationView.as_view(), name='update_information'),

]
