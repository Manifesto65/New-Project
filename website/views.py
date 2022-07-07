from django.views import generic
from django.urls import reverse
from django.shortcuts import render, redirect
from .forms import NewCommentForm
from django.contrib.auth.hashers import make_password, check_password
from django.views import View
from .models import About as a
from .models import *
from django.contrib.auth.decorators import login_required
from .forms import UserForm
from django.http import JsonResponse

# Import Pagination Stuff
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def home(request):
    about = a.objects.filter(is_active=True)
    teams = Team.objects.all()
    testimonials = Testimonial.objects.all()
    banners = Banner.objects.filter(is_active=True)
    print(testimonials)
    services = Services.objects.all()
    blogs = Blog.objects.all()
    data = {
        'about': about,
        'services': services,
        'blogs': blogs,
        'teams': teams,
        'banners': banners,
        'testimonials': testimonials

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


class ProjectList(View):
    def get(self, request):
        p = Paginator(Project.objects.all(), 1)
        page = request.GET.get('page')
        projects = p.get_page(page)
        data = {
            'projects': projects
        }

        return render(request, "project.html", data)


class ServiceDetails(View):
    def get(self, request, service_id):
        service = Services.objects.get(id=service_id)
        service_list = Services.objects.all()
        data = {
            'service': service,
            'service_list': service_list
        }
        return render(request, "service_detail.html", data)


class ProjectDetails(View):
    def get(self, request, project_id):
        project = Project.objects.get(id=project_id)
        project_list = Project.objects.all()
        data = {
            'project': project,
            'project_list': project_list
        }
        return render(request, "project_detail.html", data)


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


class BlogDetails(View):
    def get(self, request, blog_id):
        query = request.GET.get('query')
        if query:
            return redirect(reverse('website:search') + '?query=' + query)

        blog = Blog.objects.get(id=blog_id)
        total_comment = Comment.objects.filter(blog=blog).count()
        allcomments = blog.comments.filter(status=True)
        page = request.GET.get('page', 1)

        blog_list = Blog.objects.all()
        comment_form = NewCommentForm()
        # paginator = Paginator(allcomments, 10)
        # try:
        #     comments = paginator.page(page)
        # except PageNotAnInteger:
        #     comments = paginator.page(1)
        # except EmptyPage:
        #     comments = paginator.page(paginator.num_pages)
        # user_comment = None
        print(blog)
        data = {
            'blog': blog,
            'blog_list': blog_list,
            'total_comment': total_comment,
            'comment_form': comment_form,
            'allcomments': allcomments
        }
        return render(request, "blog_detail.html", data)

    def post(self, request, *args, **kwargs):
        return self.addcomment(request)

    def addcomment(self, request):
        if request.POST.get('action') == 'delete':
            id = request.POST.get('nodeid')
            print(id)
            c = Comment.objects.get(id=id)
            c.delete()
            return JsonResponse({'remove': id})

        comment_form = NewCommentForm(request.POST)
        print(comment_form)
        if comment_form.is_valid():
            user_comment = comment_form.save(commit=False)
            user_comment.user = request.user
            user_comment.save()
            blog = comment_form.cleaned_data.get('blog')
            print(blog)
            user = request.user.username
            return redirect("website:blog_detail", blog_id=blog.id)
