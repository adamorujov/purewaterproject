from django.urls import path
from mainpage.api import views

urlpatterns = [
    path("settings-list/", views.SettingsListAPIView.as_view(), name="settings-list"),
    path("socialmedia-list/", views.SocialMediaListAPIView.as_view(), name="socialmedia-list"),
    path("service-list/", views.ServiceListAPIView.as_view(), name="service-list"),
    path("category-list/", views.CategoryListAPIView.as_view(), name="category-list"),
    path("category-ourproduct-list/<int:id>/", views.CategoryOurProductListAPIView.as_view(), name="category-ourproduct-list"),
    path("ourproduct-retrieve/<int:id>/", views.OurProductRetrieveAPIView.as_view(), name="ourproduct-retrieve"),
    path("testimonial-list/", views.TestimonialListAPIView.as_view(), name="testimonial-list"),
]