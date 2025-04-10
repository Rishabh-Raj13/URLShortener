import string
import random
import hashlib
from urllib.parse import urlparse
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from url.forms import Url
from url.models import UrlData
from django.urls import reverse

# Base62 encoding characters
BASE62_ALPHABET = string.ascii_letters + string.digits

def base62_encode(num):
    """Convert an integer to a Base62 string."""
    if num == 0:
        return BASE62_ALPHABET[0]
    encoded = []
    base = len(BASE62_ALPHABET)
    while num:
        num, rem = divmod(num, base)
        encoded.append(BASE62_ALPHABET[rem])
    return ''.join(reversed(encoded))

def generate_short_slug(url):
    """Generate a unique short slug using a hash-based approach."""
    hash_digest = hashlib.md5(url.encode()).hexdigest()  # Generate hash of the URL
    num = int(hash_digest, 16)  # Convert hash to an integer
    return base62_encode(num)[:8]  # Convert to Base62 and take the first 8 chars

def urlShort(request):
    if request.method == 'POST':
        form = Url(request.POST)
        if form.is_valid():
            url = form.cleaned_data["url"]
            
            # Check if the URL already exists in the database
            existing_url = UrlData.objects.filter(url=url).first()
            if existing_url:
                return HttpResponse(f"URL already exists with short link: /{existing_url.slug}", status=400)

            # Generate a short slug
            slug = generate_short_slug(url)

            # Ensure uniqueness in case of collisions
            while UrlData.objects.filter(slug=slug).exists():
                slug = generate_short_slug(url + str(random.randint(0, 1000)))

            # Save new short URL entry
            new_url = UrlData(url=url, slug=slug)
            new_url.save()

            return redirect("http://127.0.0.1:8000/urlShort")

    else:
        form = Url()
    
    data = UrlData.objects.all()
    context = {'form': form, 'data': data}
    return render(request, 'index.html', context)

def urlRedirect(request, slugs):
    """Redirect to the original URL based on slug."""
    try:
        data = UrlData.objects.get(slug=slugs)
        originalUrl = data.url

        # Ensure correct URL format
        parsed_url = urlparse(originalUrl)
        if not parsed_url.scheme:  
            originalUrl = "http://" + originalUrl

        return redirect(originalUrl)

    except UrlData.DoesNotExist:
        return HttpResponse("URL not found", status=404)

def delete_url(request, slug):
    url = get_object_or_404(UrlData, slug=slug)
    url.delete()
    return redirect("http://127.0.0.1:8000/urlShort")