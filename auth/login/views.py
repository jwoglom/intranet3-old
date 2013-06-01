# Create your views here.
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.context_processors import csrf
# This will fail because ldap stuff isnt installed
# from intranet.login.kerberos import *
default_login_msg = {
    'title': 'Login',
    'login_message': 'Please enter a username and password to log in:',
    'login_disclaimer': """
<p>Welcome to the Thomas Jefferson High School for Science and Technology Computer Systems Lab; if you have any problems please contact <a href='m&#97;&#105;&#108;&#116;&#111;&#58;&#115;y&#115;&#97;&#100;m&#105;&#110;&#115;&#64;&#108;&#105;&#115;&#116;&#115;.&#116;j&#104;&#115;&#115;&#116;&#46;&#101;&#100;u'>sysadmins@lists.tjhsst.edu</a>.</p>
<p>Unauthorized access will result in prosecution.  By proceeding, you CONSENT to having all activity monitored and logged.  If you do not agree to these terms, please disconnect immediately.</p>
    """,
}


def disp_login(request):

    default_login_msg.update(csrf(request))
    return render_to_response('login.html', default_login_msg)


def disp_auth(request):
    post = request.POST
    try:
        username = post['username']
        password = post['password']
    except Exception:
        default_login_msg.update(csrf(request))
        return render_to_response('login.html', default_login_msg)

    return render_to_response('login.html', {
        'login_message': 'Incorrect username or password.',
        'login_disclaimer': """
        Your POST Data:<br />
    Username: {}<br />
    Password: {}<br />
        """.format(username, password),
    })
