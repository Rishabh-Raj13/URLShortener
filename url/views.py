import random
import string
from urllib.parse import urlparse
from django.shortcuts import redirect, render

from url.forms import Url
from url.models import UrlData
from django.http import HttpResponse
# Create your views here.

# def index(request):
#     return HttpResponse("hello world")

def urlShort(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            slug=''.join(random.choice(string.ascii_letters) for x in range(10))
            url = form.cleaned_data["url"]
            new_url = UrlData(url=url,slug=slug)
            new_url.save()
            # request.user.urlshort.add(new_url)
            return redirect('/urlShort')
    else:
        form = Url()
    data = UrlData.objects.all()
    context = {
        'form':form,
        'data':data
    }
    return render(request, 'index.html', context)
    
def urlRedirect(request, slugs):
    try:
        # Look up the URL data based on the slug
        data = UrlData.objects.get(slug=slugs) 
        originalUrl=data.url
        originalUrl = originalUrl.replace("http://127.0.0.1:8000/urlShort/","")
        print(originalUrl)
        parsed_url = urlparse(originalUrl)
        if not parsed_url.scheme:  # If scheme (http/https) is missing
            originalUrl = "http://" + originalUrl
        return redirect(originalUrl)  # Redirect to the original URL
    except UrlData.DoesNotExist:
        return HttpResponse("URL not found", status=404)  # If slug doesn't exist, return a 404 response

    