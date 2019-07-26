# weekly_classifieds/views.py

from django.shortcuts import render, reverse
from .models import JobPosts, Date
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required # decorator for admin only access view
from django.views.decorators.http import require_POST

from django.core.paginator import Paginator # This is for pagination


# import for views
import requests
from PIL import Image
import pytesseract
import os

def del_last_week_posts():
    JobPosts.objects.all().delete()

def get_image(page_num):
    date = Date.objects.all()[0]
    BASEURL = f"https://issues.bpweekly.com/library/{date}/files/pages/tablet/"
    EXTENSION = ".jpg"

    url = BASEURL + page_num + EXTENSION
    return requests.get(url).content



def download_image(img_data):
    img_path = os.path.join(settings.STATIC_ROOT, 'job_post_page.jpg') # https://stackoverflow.com/a/13067314
    with open(img_path, 'wb') as handler:
        handler.write(img_data)


def extract_text():
    img_path = os.path.join(settings.STATIC_ROOT, 'job_post_page.jpg')
    content = pytesseract.image_to_string(Image.open(img_path))

    # Clean text and return list of job posts
    content = content.replace('+', '*') # Bullet points are some times a + and sometimes a *, so make them all a *
    #content = content.replace('  ', ' ') # replace double spaces with single. because ocr goes crazy from double space.
    content = content.split('*')

    return content


def store_job_posts(job_posts):
    # Skip first one because it looks like thisnes.) 13 AVAILABLE
    for job in job_posts[1:]:
        JobPosts(job_post=job).save()

def get_page_range(form_input):
        form_input = form_input.split(',')
        return list(range(int(form_input[0]), int(form_input[1]) + 1)) # get the values and cast to int. then convert them into a list 151, 152, 153...



# Get the date from the url to use in the BASE_URL and display on index page
def store_date_of_url(form_input):
        Date.objects.all().delete() # delete last weeks date
        date = form_input.split(',')[2] # input looks like this 152,156,07-17-20
        Date(week_date=date).save()




# Get the range of the classified ads
@staff_member_required
def handle_img(request):
    del_last_week_posts() # Since we are storing current weeks job posts we don't need/want last weeks

    store_date_of_url(request.POST.get('range')) 
    job_ad_range = get_page_range(request.POST.get('range'))
    for num in job_ad_range:
        img_data = get_image(str(num))
        download_image(img_data)
        job_posts = extract_text()
        store_job_posts(job_posts)
    return HttpResponseRedirect(reverse('index'))



# This index will have a form so that i can enter in the range of pages.
# it'll then call the functions to process this stuff
@staff_member_required # https://stackoverflow.com/a/42658756
def admin_index(request):
    return render(request, 'weekly_classifieds/admin_index.html', context=None)


def index(request):
    #del_last_week_posts()
    all_posts = JobPosts.objects.all()

    try:
        # Pagination
        paginator = Paginator(all_posts, 12)
        page = request.GET.get('page', 1)
        all_posts = paginator.page(page)
    except:
            pass
    context = {
        'all_posts': all_posts,
        'date': Date.objects.all()[0],
    }

    return render(request, 'weekly_classifieds/index.html', context=context)



# TODO: Send a text/email to user if their keyword comes up in a classified as


# Search results for job posts
def search_results(request):
    query = request.GET.get('q')

    if query:
        all_posts = JobPosts.objects.filter(job_post__icontains=query)
    try:
        # Pagination
        paginator = Paginator(all_posts, 12)
        page = request.GET.get('page', 1)
        all_posts = paginator.page(page)
    except:
            pass
            
    context = {
        'all_posts': all_posts,
        'query': query, # Needed for pagiantion, avoid 'local variable 'all_posts' referenced before assignment'
    }

    return render(request, 'weekly_classifieds/index.html', context)


# https://issues.bpweekly.com/library/07-17-2019/files/pages/tablet/251.jpg