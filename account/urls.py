from django.urls import path
from . import views
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),

    path('update_content/<str:pk>/', views.updateContent, name='update_content'),
    path('create_content/<slug:slug>/', views.createContent, name='create_content'),
    path('delete_content/<str:pk>/', views.deleteContent, name='delete_content'),

    path('brand/', views.brandPage, name='brand'),
    path('content/', views.contentPage, name='content'),
    path('single_brand/<slug:slug>/', views.single_brand, name='single_brand'),
    path('update_brand/<slug:slug>/', views.updateBrand, name='update_brand'),
    path('create_brand/', views.createBrand, name='create_brand'),
    path('delete_brand/<slug:slug>/', views.deleteBrand, name='delete_brand'),
    path('brand_chart/<brand_slug>/', views.UserChartView.as_view(), name='Brand-Detail'),
]