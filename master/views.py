# Homepage view
from django.shortcuts import render

def home(request):
    return render(request, 'pages/index.html',{'page':'home'})


# Mentions legal view
def mentions(request):
    title = "Mentions légales"
    return render(request, 'pages/mentions_legal.html', {'title':title})


# Contact view
def contact(request):
    title = "Contact"
    return render(request, 'pages/contact.html', {'title':title})


