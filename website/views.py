from django.shortcuts import render
from django.views import View
from .models import About as a
from .models import *

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



class ContactUsView(View):
    def get(self, request):
        contact = Contact.objects.get(status=True)
        data={
            'contact':contact
        }

        return render(request, "contact.html",data)

    def post(self, request):
        postData = request.POST
        fname = postData.get('fname')
        lname = postData.get('lname')
        email = postData.get('email')
        subject = postData.get('subject')
        message = postData.get('message')

        value ={
            'fname':fname,
            'lname': lname,
            'email':email,
            'subject' : subject,
            'message':message
        }

        def validateContact(contact):
            error_message = None
            if not contact.first_name:
                error_message = 'First name is required'

            return error_message

        error_message = None
        show_msg =None

        contact = ContactUs(first_name=fname,
                            last_name=lname,
                            email=email,
                            subject=subject,
                            message=message
                            )

        error_message = validateContact(contact)
        

        if not error_message:
            contact.save()
            show_msg = "Thank You for contacting us"
            value = {}
            
           

        data={
            'error': error_message,
            'show_message': show_msg,
            'value' :value
        }

        return render(request, "contact.html",data )


class ServiceList(View):
    def get(self, request):
        return render(request, "service.html")


class ServiceDetails(View):
    def get(self, request, service_id):
        return render(request, "service-detail.html")


class BlogList(View):
    def get(self, request):

        #Set up Pagination
        p = Paginator(Blog.objects.all(),1)
        page = request.GET.get('page')
        blogs = p.get_page(page)
        data = {
            'blogs': blogs
        }
        return render(request, "blog.html",data)





class BlogDetails(View):
    def get(self, request,blog_id):
        print(blog_id)
        blog = Blog.objects.get(id=blog_id)
        blog_list = Blog.objects.all()
        print(blog)
        data= {
            'blog':blog,
            'blog_list':blog_list
        }
        return render(request, "blog_detail.html",data)
