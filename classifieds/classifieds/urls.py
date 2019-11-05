"""classifieds URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from weekly_classifieds.views import index, admin_index, handle_img, search_results

# index for evryone, admin index for me to fill out form, handle_img for form to submit to that url, use ajax for request otherwise may get timeout error from heroku


urlpatterns = [
    path('hack_free_admin/', admin.site.urls),
    
    path('', index, name='index'),
    path('admin_index', admin_index, name='admin_index'),
    # path('handle_img', handle_img, name='handle_img'),
    path('search_results', search_results, name='search_results'),
]
