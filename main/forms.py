from django import forms

class AnswerForm(forms.Form):
    answer = forms.CharField(label='Type your answer', max_length=200, required=False, widget=forms.HiddenInput())