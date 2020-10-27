from django import forms
from snowpenguin.django.recaptcha2.fields import ReCaptchaField
from snowpenguin.django.recaptcha2.widgets import ReCaptchaWidget

class ReCaptchaForm(forms.Form):
	captcha = ReCaptchaField(widget=ReCaptchaWidget())