from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt

app_name = 'library'

urlpatterns = [
    path('', views.listOfBooks, name='home'),
    path('listing/', views.listing, name='listing'),
    path('addbook/', views.AddBook.as_view(), name='addBook'),
    path('<int:pk>/update', views.BooksUpdateView.as_view(), name='books_update'),
    path('<int:pk>/delete', views.BooksDeleteView.as_view(), name='books_delete'),
    path('register/', views.UserRegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
    path('account/', views.userAccount, name='account'),
    #path('password_change/', auth_views.PasswordChangeView.as_view(template_name='Library/password_change.html', success_url=reverse_lazy('account')), name='password_change')
    path('password_change/', views.ChangePasswordView.as_view(), name='password_change'),
    path('email_change/', views.emailChange, name='email_change'),
    path('firstname_change/', views.firstNameChange, name='firstname_change'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('validate-password1/', csrf_exempt(views.PasswordValidationView.as_view()), name='validate-password1')
]