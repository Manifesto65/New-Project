from django.urls import path
from .views import home, About, ContactUsView, ServiceList, BlogList,BlogDetails,ServiceDetails

app_name= "website"
urlpatterns = [
    path('', home, name="homepage"),
    path('about/', About.as_view(), name="about"),
    path('contact/', ContactUsView.as_view(), name="contact"),
    path('blog/', BlogList.as_view(), name="blog_list"),
    path('service/', ServiceList.as_view(), name="service_list"),
    path('blog/<int:blog_id>', BlogDetails.as_view(), name="blog_detail"),
    path('service/<int:service_id>', ServiceDetails.as_view(), name="service_detail"),



]
