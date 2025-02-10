from django.urls import path
from productapp.api import views

urlpatterns = [
    path('city-list-create/', views.CityListCreateAPIView.as_view(), name="city-list-create"),
    path('city-retrieve-update-destroy/<int:id>/', views.CityRetrieveUpdateDestroyAPIView.as_view(), name="city-retrieve-update-destroy"),
    path('district-list-create/', views.DistrictListCreateAPIView.as_view(), name="district-list-create"),
    path('city-district-list/<int:id>/', views.CityDistrictListAPIView.as_view(), name="city-district-list"),
    path('district-retrieve-update-destroy/<int:id>/', views.DistrictRetrieveUpdateDestroyAPIView.as_view(), name="district-retrieve-update-destroy"),
    path('district-city-retrieve/<int:id>/', views.DistrictCityRetrieveAPIView.as_view(), name="district-city-retrieve"),
    path('village-list-create/', views.VillageListCreateAPIView.as_view(), name="village-list-create"),
    path('district-village-list/<int:id>/', views.DistrictVillageListAPIView.as_view(), name="district-village-list"),
    path('city-village-list/<int:id>/', views.CityVillageListAPIView.as_view(), name="city-village-list"),
    path('village-retrieve-update-destroy/<int:id>/', views.VillageRetrieveUpdateDestroyAPIView.as_view(), name="village-retrieve-update-destroy"),
    path('product-list-create/', views.ProductListCreateAPIView.as_view(), name="product-list-create"),
    path('product-retrieve-update-destroy/<int:id>/', views.ProductRetrieveUpdateDestroyAPIView.as_view(), name="product-retrieve-update-destroy"),
    path('gift-list-create/', views.GiftListCreateAPIView.as_view(), name="gift-list-create"),
    path('gift-retrieve-update-destroy/<int:id>/', views.GiftRetrieveUpdateDestroyAPIView.as_view(), name="product-retrieve-update-destroy"),
]