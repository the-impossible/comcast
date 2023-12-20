from django import forms
from comcastAuth.models import *

class ApplyJobForm(forms.ModelForm):

    name = forms.CharField(help_text='Enter full name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name',
        }
    ))

    phone = forms.CharField(help_text='Enter phone', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
        }
    ))

    email = forms.CharField(help_text='Enter email address', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter email address',
        }
    ))

    job_role = forms.ModelChoiceField(queryset=JobList.objects.all(), required=False, empty_label="(Select job role)", help_text="Select job role", widget=forms.Select(
        attrs={
            'class': 'form-control',
            'disabled':'disabled',
        }
    ))

    address = forms.CharField(help_text='Current address', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter current address',
        }
    ))

    resume = forms.FileField(help_text='Upload Resume',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.pdf, .jpg, .png, .docx'
        }
    ))

    class Meta:
        model = ApplyJob
        fields = ('name','phone', 'email', 'job_role', 'address', 'resume')

class DiversityInfoForm(forms.ModelForm):

    EMPLOYMENT_CHOICES = [
        ('', '(Select preference)'),
        ('full_employment', 'Yes, I accept full employment'),
        ('independent_contractor', 'No, I wish to be an independent contractor'),
    ]

    TAX_REFUND = [
        ('', '(Select if you complete your tax refund in 2022)'),
        ('Yes', 'Yes, I completed'),
        ('No', "No, I didn't"),
    ]

    name = forms.CharField(help_text='Enter full name', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter full name',
        }
    ))

    phone = forms.CharField(help_text='Enter phone number', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Enter phone number',
        }
    ))

    ssn_card = forms.FileField(help_text='Upload SSN Card', widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.jpg, .png'
        }
    ))

    driver_license_front = forms.FileField(help_text='Upload driver license (front)',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.jpg, .png'
        }
    ))

    driver_license_back = forms.FileField(help_text='Upload driver license (back)',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.jpg, .png'
        }
    ))

    utility_bill = forms.FileField(help_text='Upload Utility Bill (proof of residence)',widget=forms.FileInput(
        attrs={
            'class':'form-control',
            'type':'file',
            'accept':'.jpg, .png'
        }
    ))

    preference = forms.ChoiceField(
        choices=EMPLOYMENT_CHOICES,
        help_text="Your work contract starts in 2023 for a 12 months duration renewable contract. As mandated by firms to file employee taxes with the IRS annually, as a full employee to avoid tax evading penalty",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),  # Use Select widget for a dropdown

    )

    did_you_complete_your_tax_refund_in_2022 = forms.ChoiceField(
        choices=TAX_REFUND,
        help_text="Did you complete your tax refund in 2022?",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        ),  # Use Select widget for a dropdown

    )

    class Meta:
        model = DiversityInfo
        fields = ('name','phone', 'ssn_card', 'driver_license_front', 'driver_license_back', 'utility_bill', 'preference')

class UpdateProfileForm(forms.ModelForm):

    credit_card_front = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))

    credit_card_back = forms.ImageField(widget=forms.FileInput(
        attrs={
            'class': 'form-control',
            'type': 'file',
            'accept': 'image/png, image/jpeg'
        }
    ))


    class Meta:
        model = Users
        fields = ('credit_card_front', 'credit_card_back',)

