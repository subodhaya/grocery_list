from django.contrib import admin
from django.urls import path ,include 
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('submit/<int:list_id>/', views.submit_list, name='submit_list'),
     path("add_item/", views.add_item, name='add_item'),
    path('list/create/', views.grocery_list, name='grocery_list'),
    path('list/<int:list_id>/', views.grocery_list, name='grocery_list'),
    path('list/create1/', views.create_list, name='create_list'),  # New URL pattern
    path('list/<int:list_id>/add_item/', views.add_item, name='add_item'),
    path('log_lists/', views.log_lists, name='log_lists'),
    path('get_list_names/', views.get_list_names, name='get_list_names'),
    path('update_task_status/<int:list_id>/', views.update_task_status, name='update_task_status'),
    path('display_all_lists/', views.display_all_lists, name='display_all_lists'),
    path('get_finished_lists/', views.get_finished_lists, name='get_finished_lists'),
    path('update_list_status/<int:list_id>/', views.update_list_status, name='update_list_status'),
    path('get_saved_lists/', views.get_saved_lists, name='get_saved_lists'),
    path('get_items/<int:list_id>/', views.get_items, name='get_items'),
    path('shopnow/<int:list_id>/', views.shopnow_view, name='shopnow_view'),
    path('edit_list/<int:list_id>/', views.edit_list, name='edit_list'),
    path('delete_list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('shopnow/<int:list_id>/update_item/<int:item_id>/', views.update_item, name='update_item'),
    path('get_finished_lists/delete_list/<int:list_id>/', views.delete_list, name='delete_list'),
    path('log_Edit_lists/', views.log_Edit_lists, name='log_Edit_lists'),
    path('delete_item/<int:item_id>/', views.delete_item, name='delete_item'),
    path('share_list/<int:list_id>/', views.share_list, name='share_list')
     
]
    

