from django.shortcuts import render
from django.views import View
from .models import About as a
from .models import Blog

#Import Pagination Stuff
from django.core.paginator import Paginator

def home(request):
    return render(request, "index.html")


class About(View):
    def get(self, request):
        about = a.objects.get(is_active=True)
        data = {
            'about': about
        }
        return render(request, "about.html", data)


class ContactUs(View):
    def get(self, request):
        return render(request, "contact.html")

    def post(self, request):
        pass


class ServiceList(View):
    def get(self, request):
        return render(request, "service.html")


class ServiceDetails(View):
    def get(self, request, service_id):
        return render(request, "service-detail.html")


class BlogList(View):
    def get(self, request):

        #Set up Pagination
        p = Paginator(Blog.objects.all(),2)
        page = request.GET.get('page')
        blogs = p.get_page(page)
        data = {
            'blogs': blogs
        }
        return render(request, "blog.html",data)


def post(self, request):
    pass


class BlogDetails(View):
    def get(self, request, blog_id):
        return render(request, "blog.html")
