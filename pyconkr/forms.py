from django import forms
from django.conf import settings
from django.core.files.images import get_image_dimensions
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

    def __init__(self, *args, **kwargs):
        super(EmailLoginForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Login')))

    def clean(self):
        cleaned_data = super(EmailLoginForm, self).clean()
        return cleaned_data


class SpeakerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SpeakerForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', _('Submit')))
        self.fields['image'].help_text += _('Maximum size is %d MB') \
            % settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB
        self.fields['image'].help_text += ' / ' + _('Minimum dimension is %d x %d') \
            % settings.SPEAKER_IMAGE_MINIMUM_DIMENSION

    class Meta:
        model = Speaker
        fields = ('image', 'desc', 'info', )
        widgets = {
            'desc': SummernoteInplaceWidget(),
        }
        labels = {
            'image': _('Photo'),
            'desc': _('Profile'),
            'info': _('Additional information'),
        }

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            if image._size > settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB * 1024 * 1024:
                raise forms.ValidationError(
                    _('Maximum size is %d MB')
                    % settings.SPEAKER_IMAGE_MAXIMUM_FILESIZE_IN_MB
                )
            w, h = get_image_dimensions(image)
            if w < settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[0] \
                    or h < settings.SPEAKER_IMAGE_MINIMUM_DIMENSION[1]:
                raise forms.ValidationError(
                    _('Minimum dimension is %d x %d')
                    % settings.SPEAKER_IMAGE_MINIMUM_DIMENSION
                )

        return image


class ProgramForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProgramForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
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
