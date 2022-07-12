from django.urls import path
from .views import (Search, home, About, ContactUsView, ServiceList, BlogList, BlogDetails,
                    ServiceDetails, Account, logout, userprofile, UserUpdateView, ProjectList, ProjectDetails)
app_name = "website"
urlpatterns = [
    path('', home, name="homepage"),
    path('about/', About.as_view(), name="about"),
    path('contact/', ContactUsView.as_view(), name="contact"),
    path('account/', Account.as_view(), name="account"),
    path('logout/', logout, name="logout"),
    path('blog/', BlogList.as_view(), name="blog_list"),
    path('service/', ServiceList.as_view(), name="service_list"),
    path('project/', ProjectList.as_view(), name="project_list"),

    path('search/', Search.as_view(), name="search"),
    path('service/<int:service_id>',
         ServiceDetails.as_view(), name="service_detail"),
    path('project/<int:project_id>',
         ProjectDetails.as_view(), name="project_detail"),
    path('userprofile/<int:user_id>', userprofile, name="profile"),
    path('update_user/<int:pk>', UserUpdateView.as_view(), name="update_user"),
    path('blog/<int:blog_id>', BlogDetails.as_view(), name="blog-detail"),



]
