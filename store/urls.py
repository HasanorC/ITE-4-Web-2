from django.urls import path
from . import views
urlpatterns = [
   path('', views.food_list, name='product_list'),
    path('product_list/add/', views.add_food, name='add_product'),
    path('admin_products/', views.admin_food_list, name='admin_products'),
    path('product_list/edit/<int:pk>/', views.edit_food, name='edit_product'),
    path('admin_products/delete/<int:pk>/', views.delete_food, name='delete_product'),
    path('products/<int:pk>/', views.food_description, name='product_detail'),

    path('categories/', views.admin_food_categories, name='admin_categories'),
    path('categories/add/', views.add_food_category, name='add_category'),
    path('categories/edit/<int:pk>/', views.edit_food_category, name='edit_category'),
    path('categories/delete/<int:pk>/', views.delete_food_category, name='delete_category'),

    path('signup/', views.signupUser, name='signup'),
    path('login/', views.user, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('about/', views.aboutStore, name='about'),
]
