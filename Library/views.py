from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from .models import Books, Profile
from .forms import BooksForm, UserRegisterForm, UserLoginForm, EmailChangeForm, FirstNameChangeForm
from django.views.generic import UpdateView, DeleteView, CreateView, View
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from shopping_cart.models import Order
import json
from django.http import JsonResponse
from validate_email import validate_email
from password_validator import PasswordValidator
from .filters import ListingFilter


class UsernameValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if User.objects.filter(username = username).exists():
            return JsonResponse({'username_error': 'Пользователь с таким никнеймом уже существует'}, status = 409)
        return JsonResponse({'username_valid': True})


class EmailValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email не действителен'}, status=409)
        if User.objects.filter(email = email).exists():
            return JsonResponse({'email_error': 'Пользователь с таким email уже существует'}, status = 409)
        return JsonResponse({'email_valid': True})


class PasswordValidationView(View):
    def post(self, request):
        data = json.loads(request.body)
        password = data['password1']
        shema = PasswordValidator()
        shema.min(8)
        shema.max(20)
        shema.has().digits()
        shema.has().no().spaces()
        shema.has().symbols()
        if not shema.validate(password):
            return JsonResponse({'password1_error': 'Пароль не корректен'}, status=409)
        return JsonResponse({'password1_valid': True})


def userAccount(request):
    userName = request.user.username
    userEmail = request.user.email
    userFirstName = request.user.first_name
    return render(request, 'Library/user_account.html', {'userName': userName, 'userEmail': userEmail, 'userFirstName': userFirstName})


def listOfBooks(request):
    list = Books.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=list)
    context = {'list': list, 'listing_filter': listing_filter}
    return render(request, 'Library/homePage.html', context)


class CustomSuccessMessageMixin:   #Вывод сообщений об успешном завершении чего-либо
    @property
    def success_msg(self):
        return False

    def form_valid(self, form):
        messages.success(self.request, self.success_msg)
        return super().form_valid(form)


class AddBook(LoginRequiredMixin, CustomSuccessMessageMixin, CreateView): #LoginRequiredMixin обязательно должен быть в крайнем левом положении при наследовании
    login_url = 'library:login'   #Для LoginRequiredMixin, куда перенаправлять не авторизированного пользователя
    redirect_field_name = 'library:login'   #Для LoginRequiredMixin, та же хрень
    model = Books
    template_name = 'Library/addBook.html'
    form_class = BooksForm
    success_msg = 'Запись создана'
    success_url = reverse_lazy('library:home')

    def form_valid(self, form):  #Нужно для автоматического сохранения автора записи
        self.object = form.save(commit=False)  #Этой строчкой сохраняем экземпляр объекта, но ещё метод сохранения не вызван, то есть в БД не записано, это как раз благодаря commit=False
        self.object.user = self.request.user   #Добавление дополнительного параметра автора записи для self.object
        self.object.save()   #Сохранение в БД
        return super().form_valid(form)


#def addBook(request):
#    if request.method == 'POST': #проверка на метод
#        form = BooksForm(request.POST) #тут будут храниться данные, которые получили от user'а при вводе их в форму
#        if form.is_valid(): #проверка правильно ли заполнены формы user'ом
#            form.save() #сохранение введённых данных user'ом
#            messages.success(request, 'Книга успешно добавлена')
#            return redirect('home') #перенаправление на главную страницу после корректного ввода всех данных
#        else:
#            messages.error(request, 'Ошибка добавления книги')
#    form = BooksForm()
#    data = {
#        'form': form
#    }
#    return render(request, 'Library/addBook.html', data)


class BooksUpdateView(LoginRequiredMixin, CustomSuccessMessageMixin, UpdateView):
    login_url = 'library:login'
    redirect_field_name = 'library:login'
    model = Books
    template_name = 'Library/update.html'
    success_msg = 'Запись отредактирована'
    form_class = BooksForm

    def get_form_kwargs(self):   #Ограничение на изменение записи не администратором
        kwargs = super().get_form_kwargs()
        if not self.request.user.is_superuser:
            return self.handle_no_permission()   #Будет выдавать 403 Forbidden
        return kwargs


class BooksDeleteView(LoginRequiredMixin, CustomSuccessMessageMixin, DeleteView):
    login_url = 'library:login'
    redirect_field_name = 'library:login'
    model = Books
    template_name = 'Library/delete.html'
    success_msg = 'Запись удалена'
    success_url = '/'

    def get_form_kwargs(self):   #Ограничение на удаление записи не администратором
        kwargs = super().get_form_kwargs()
        if not self.request.user.is_superuser:
            return self.handle_no_permission()   #Будет выдавать 403 Forbidden
        return kwargs


def listing(request):
    objects = Books.objects.all()
    paginator = Paginator(objects, 5)
    page_number = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_number)
    context = {'page_obj': page_objects}
    return render(request, 'Library/listing.html', context)


class UserRegisterView(CustomSuccessMessageMixin, CreateView):
    template_name = 'Library/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('library:home')
    success_msg = 'Вы успешно зарегистрировались'

    def form_valid(self, form):    #Автоматическая авторизация после регистрации
        form_valid = super().form_valid(form)
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password1"]
        auth_user = authenticate(username=username, password=password)
        login(self.request, auth_user)
        return form_valid


#def register(request):
#    if request.method == 'POST':
#        form = UserRegisterForm(request.POST)
#        if form.is_valid():
#            user = form.save()
#           login(request, user)
#            messages.success(request, 'Вы успешно зарегистрировались')
#            return redirect('home')
#        else:
#            messages.error(request, 'Ошибка регистрации')
#    form = UserRegisterForm()
#    return render(request, 'Library/register.html', {'form': form})


class UserLoginView(CustomSuccessMessageMixin, LoginView):
    template_name = 'Library/login.html'
    form_class = UserLoginForm
    next_page = reverse_lazy('library:home')
    success_msg = 'Вы успешно авторизовались'

#def user_login(request):
#    if request.method == 'POST':
#        form = UserLoginForm(data=request.POST)
#        if form.is_valid():
#            user = form.get_user()
#            login(request, user)
#            messages.success(request, 'Вы успешно авторизовались')
#            return redirect('home')
#        else:
#            messages.error(request, 'Ошибка авторизации')
#    form = UserLoginForm()
#    return render(request, 'Library/login.html', {"form": form})


class UserLogoutView(CustomSuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('library:home')


#def user_logout(request):
#    logout(request)
#    messages.info(request, 'Вы вышли из учетной записи')
#    return redirect('home')

class ChangePasswordView(CustomSuccessMessageMixin, PasswordChangeView):
    template_name = 'Library/password_change.html'
    success_url = reverse_lazy('library:account')
    success_msg = 'Вы успешно изменили пароль'


def emailChange(request):
    if request.method == 'POST':
        emailChangeForm = EmailChangeForm(request.POST)
        if emailChangeForm.is_valid():
            request.user.email = emailChangeForm.cleaned_data['email']
            request.user.save()
            messages.success(request, F'Вы успешно изменили почту на {emailChangeForm.cleaned_data["email"]}')
            return redirect('library:account')
        else:
            messages.error(request, 'Ошибка изменения почты')
    else:
        emailChangeForm = EmailChangeForm()
    return render(request, 'Library/email_change.html', {'form': emailChangeForm})


def firstNameChange(request):
    if request.method == 'POST':
        firstNameChangeForm = FirstNameChangeForm(request.POST)
        if firstNameChangeForm.is_valid():
            request.user.first_name = firstNameChangeForm.cleaned_data['first_name']
            request.user.save()
            messages.success(request, F'Вы успешно изменили имя на {firstNameChangeForm.cleaned_data["first_name"]}')
            return redirect('library:account')
        else:
            messages.error(request, 'Ошибка изменения имени')
    else:
        firstNameChangeForm = FirstNameChangeForm()
    return render(request, 'Library/firstname_change.html', {'form': firstNameChangeForm})


