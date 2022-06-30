from django.views import generic
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import About as a
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import UserForm

# Import Pagination Stuff
from django.core.paginator import Paginator


def home(request):
    about = a.objects.get(is_active=True)
    banners = Banner.objects.filter(is_active=True)
    print(banners)
    services = Services.objects.all()
    blogs = Blog.objects.all()
    data = {
        'about': about,
        'services': services,
        'blogs': blogs,
        'banners': banners

    }

    return render(request, "index.html", data)


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
        data = {
            'contact': contact
        }

        return render(request, "contact.html", data)

    def post(self, request):
        postData = request.POST
        fname = postData.get('fname')
        lname = postData.get('lname')
        email = postData.get('email')
        subject = postData.get('subject')
        message = postData.get('message')

        value = {
            'fname': fname,
            'lname': lname,
            'email': email,
            'subject': subject,
            'message': message
        }

        def validateContact(contact):
            error_message = None
            if not contact.first_name:
                error_message = 'First name is required'

            return error_message

        error_message = None
        show_msg = None

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

        data = {
            'error': error_message,
            'show_message': show_msg,
            'value': value
        }

        return render(request, "contact.html", data)


class ServiceList(View):
    def get(self, request):
        p = Paginator(Services.objects.all(), 1)
        page = request.GET.get('page')
        services = p.get_page(page)
        data = {
            'services': services
        }

        return render(request, "service.html", data)


class ServiceDetails(View):
    def get(self, request, service_id):
        service = Services.objects.get(id=service_id)
        service_list = Services.objects.all()
        data = {
            'service': service,
            'service_list': service_list
        }
        return render(request, "service_detail.html", data)


class BlogList(View):
    def get(self, request):

        # Set up Pagination

        p = Paginator(Blog.objects.all(), 1)
        page = request.GET.get('page')
        blogs = p.get_page(page)
        data = {
            'blogs': blogs
        }
        return render(request, "blog.html", data)


class BlogDetails(View):
    def get(self, request, blog_id):
        query = request.GET.get('query')
        if query:
            return redirect(reverse('website:search') + '?query=' + query)

        blog = Blog.objects.get(id=blog_id)
        total_comment = Comment.objects.filter(blog=blog).count()
        comments = Comment.objects.filter(blog=blog)
        blog_list = Blog.objects.all()
        print(blog)
        data = {
            'blog': blog,
            'blog_list': blog_list,
            'total_comment': total_comment,
            'comments': comments
        }
        return render(request, "blog_detail.html", data)

    def post(self, request, blog_id):
        postData = request.POST
        content = postData.get("comment")
        blog = Blog.objects.get(id=blog_id)
        try:
            user = User.objects.get(username=request.session['username'])
        except:
            user = None
        if user:
            comment = Comment(content=content,
                              blog=blog,
                              user=user)
            comment.save()
            return redirect("website:blog_detail", blog_id=blog_id)
        else:
            return redirect("website:account")


class Account(View):
    def get(self, request):
        return render(request, 'account/account.html')

    def post(self, request):
        postData = request.POST
        choice = postData.get("choice")
        if choice == "login":
            username = postData.get('user')
            password = postData.get('pass')
            print(username)
            value = {
                'user': username
            }
            try:
                user = User.objects.get(username=username)
            except:
                user = None
            error_message = None
            print(username)
            if user:
                flag = check_password(password, user.password)
                if flag:
                    request.session['user_id'] = user.id
                    request.session['username'] = user.username
                    return redirect('website:homepage')
                else:
                    error_message = 'Username or password is invalid'
            else:
                error_message = 'Username or password is invalid'

            return render(request, 'account/account.html', {'error': error_message, 'value': value})

        if choice == "signup":
            username = postData.get('user')
            email = postData.get('email')
            password = postData.get('pass')
            value = {
                'user': username,
                'email': email
            }

            def validateUser(user):
                error_message = None
                if not user.username:
                    error_message = 'User name is required'
                elif len(user.username) < 3:
                    error_message = 'User name should be more than 2 letters'
                elif len(user.email) < 5:
                    error_message = 'email should be more than 5 letters'
                elif len(user.password) < 4:
                    error_message = 'password should be more than 2 letters'
                elif user.isuserExist():
                    error_message = 'Username  already exists'
                return error_message

            error_message = None

            user = User(username=username, email=email, password=password)
            error_message = validateUser(user)

            if not error_message:
                # saving
                user.password = make_password(user.password)
                user.save()
                return redirect('website:account')

        return render(request, 'account/account.html', {'error': error_message, 'value': value})


def logout(request):
    request.session.clear()
    return redirect('website:account')


def userprofile(request, user_id):
    user = User.objects.get(id=user_id)
    print(user)
    data = {
        'user': user
    }
    return render(request, "account/userprofile.html", data)


class UserUpdateView(generic.UpdateView):
    template_name = "account/update_profile.html"
    queryset = User.objects.all()
    form_class = UserForm

    def get_success_url(self, **kwargs):
        user = self.request.session['user_id']
        return reverse("website:profile", kwargs={'user_id': user})


class Search(View):
    def get(self, request):
        query = request.GET.get('query')
        print(query)
        query_result = Blog.objects.filter(blog_title__icontains=query)
        p = Paginator(query_result, 2)
        page = request.GET.get('page')
        blogs = p.get_page(page)
        print(query_result)
        data = {
            'blogs': blogs
        }

        print(data)
        return render(request, "search.html", data)
