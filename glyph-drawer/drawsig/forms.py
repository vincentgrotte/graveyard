from django import forms

class InputForm(forms.Form):
	intent = forms.CharField(widget=forms.Textarea, max_length=250)
	shape = forms.CharField(label='shape', max_length=4)