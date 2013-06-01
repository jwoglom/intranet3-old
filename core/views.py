# Create your views here.
from django.shortcuts import render_to_response
def disp_homepage(request):
    d = {'title': 'Intranet'}
    return render_to_response('homepage.html', d)
def disp_welcome(request):
    d = {
    	'title': 'Welcome, user',
    	'header-title': 'Welcome, user'
    }
    return render_to_response('welcome.html', d)

def blank_template(request):
    return render_to_response('blank.html', {})
def login_template(request):
	return render_to_response('loginnew.html', {})