from django import forms
from .models import Topic, Post
from django.utils.translation import ugettext_lazy as _


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(max_length=100, strip=True,
                              widget=forms.Textarea(attrs={'rows': 5, 'id': 'message', 'name': 'message'}),
                              help_text="The max length of the text is 100")

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        help_texts = {'subject': 'The max length of the subject is 50'}

    def __init__(self, *args, **kwargs):
        super(NewTopicForm, self).__init__(*args, **kwargs)
        self.fields['subject'].label = "Subject"
        self.fields['message'].label = "Message"
        self.fields['subject'].widget.attrs.update({'placeholder': 'Enter Your Subject'})
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter Your Message'})


class ReplyPostForm(forms.ModelForm):
    message = forms.CharField(max_length=500, strip=True, min_length=10,
                              widget=forms.Textarea(attrs={'rows': 5, 'id': 'message', 'name': 'message'}),
                              error_messages={'required': "Message is mandatory Argument "})

    def __init__(self, *args, **kwargs):
        super(ReplyPostForm, self).__init__(*args, **kwargs)
        self.fields['message'].label = "Message"
        self.fields['message'].widget.attrs.update({'placeholder': 'Enter Your Message'})

    class Meta:
        model = Post
        fields = ['message', ]
        error_messages = {
            'required': _("Please Enter the Message")
        }


class EditPostForm(ReplyPostForm):
    pass
