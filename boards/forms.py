from django import forms
from .models import Topic


class NewTopicForm(forms.ModelForm):
    message = forms.CharField(max_length=100, strip=True, widget=forms.Textarea(attrs={'rows': 5, 'id': 'message', 'name': 'message'}), help_text="The max length of the text is 100")

    class Meta:
        model = Topic
        fields = ['subject', 'message']
        help_texts = {'subject': 'The max length of the subject is 50'}
