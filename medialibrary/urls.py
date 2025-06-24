from django.urls import path
from . import views
from .views import custom_login

urlpatterns = [
    # Public
    path('', views.home, name='home'),

    #login
    path('login/', custom_login, name='login'),

    #logout
    path('logout/', views.logout_view, name='logout'),

    # Member
    path('member/media/', views.member_media_list, name='member_media_list'),

    # Librarian
    path('librarian/', views.librarian_dashboard, name='librarian_dashboard'),
    path('librarian/members/', views.member_list, name='member_list'),
    path('librarian/members/create/', views.member_create, name='member_create'),
    path('librarian/members/<int:pk>/update/', views.member_update, name='member_update'),
    path('librarian/media/', views.media_list, name='media_list'),
    path('librarian/media/<str:media_type>/create/', views.media_create, name='media_create'),
    path('librarian/loans/', views.loan_list, name='loan_list'),
    path('librarian/loans/create/', views.loan_create, name='loan_create'),
    path('librarian/loans/<int:pk>/return/', views.loan_return, name='loan_return'),
]