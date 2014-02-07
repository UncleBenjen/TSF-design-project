from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext
from django.shortcuts import render_to_response

def index(request):
	context = RequestContext(request)
	
	context_dict = {'boldmessage': "This is C-Map context"}
	
	return render_to_response('curriculum/index.html', context_dict, context)

def about(request):
	context = RequestContext(request)
	return render_to_response('curriculum/about.html', context)
