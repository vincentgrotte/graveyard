from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .models import *
from .forms import *
import subprocess

def index(request):
	template = loader.get_template('drawsig/index.html')

	if request.method == 'POST' :
		form = InputForm(request.POST)
		if form.is_valid():
			intent = request.POST.get('intent', "")
			shape = request.POST.get('shape', "")
			sigil = Sigil(intent=intent, shape=shape)
			sigil.save()
			return HttpResponseRedirect('')
	else:
		form = InputForm()

	sigils = Sigil.objects.all()
	context = {
		"sigils" : sigils,
		"form"	: form
	}

	return HttpResponse(template.render(context, request))

