from django import forms
from django.utils.translation import ugettext_lazy as _
from django_summernote.widgets import SummernoteInplaceWidget
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import Speaker, Program


class EmailLoginForm(forms.Form):
    email = forms.EmailField(
        max_length=255,
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Email address',
            'class': 'form-control',
        })
    )

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data


class SpeakerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpeakerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Speaker
        fields = ('desc', 'info', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }
        labels = {
            'desc': _('Profile'),
            'info': _('Additional information'),
        }


class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', _('Submit')))

    class Meta:
        model = Program
        fields = ('slide_url', 'video_url', 'is_recordable', 'desc', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }
        labels = {
            'slide_url': _('Slide URL'),
            'video_url': _('Video URL'),
            'is_recordable': _('Photography and recording is allowed'),
            'desc': _('Description'),
        }
