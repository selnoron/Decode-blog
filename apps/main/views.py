from django.shortcuts import (
    render, 
    redirect,
    get_object_or_404
)
from django.views.generic import View
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.db.models.query import QuerySet
from main.models import (
    MyUser,
    Publication,
    Comment
)
from main.serializer import (
    MyUserSerializer,
    PublicationSerializer,
    CommentSerializer,
    RegistrationSerializer,
    LoginSerializer
)
from django.contrib.auth import login, logout, authenticate
from rest_framework.validators import ValidationError
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.http import HttpResponseForbidden


class MainView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if 'user' not in request.session.keys():
            return redirect('login')
        else:
            return redirect('blogs')
    
class BlogsView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if 'user' not in request.session.keys():
            return redirect('login')
        
        template_name: str = 'lentablogov.html'
        user: MyUser = MyUser.objects.get(pk=request.session['user'].get('id'))
        user = MyUserSerializer(instance=user)
        
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '')

        blog_query = Publication.objects.all()

        if search_query:
            blog_query = blog_query.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )

        if sort_by:
            blog_query = blog_query.filter(p_type=sort_by)

        blogs = []
        for i in range(len(blog_query) - 1, -1, -1):
            dat = PublicationSerializer(instance=blog_query[i]).data
            blogs.append(dat)
        
        return render(
            request=request,
            template_name=template_name,
            context={
                'user': user,
                'blogs': blogs,
                'search_query': search_query,
                'sort_by': sort_by
            }
        )
    

class ProfileView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        if 'user' not in request.session.keys():
            return redirect('login')
        
        template_name: str = 'profile.html'
        user: MyUser = MyUser.objects.get(pk=request.session['user'].get('id'))
        user = MyUserSerializer(instance=user)
        print(user.instance.posts.all(), 1111)
        blog_query = user.instance.posts.all()  
        blogs = []
        search_query = request.GET.get('search', '')
        sort_by = request.GET.get('sort_by', '')
        
        if search_query:
            blog_query = blog_query.filter(
                Q(title__icontains=search_query) | Q(text__icontains=search_query)
            )

        if sort_by:
            blog_query = blog_query.filter(p_type=sort_by)

        for i in range(len(blog_query) - 1, -1, -1):
            dat = PublicationSerializer(instance=blog_query[i]).data
            blogs.append(dat)
        
        
        return render(
            request=request,
            template_name=template_name,
            context={
                'user': user.data,
                'blogs': blogs
            }
        )
    

class CreateBlogView(View):
    def get(self, request):
        if 'user' not in request.session.keys():
            return redirect('login')
        return render(request, 'newblog.html')
    
    def post(self, request):
        if 'user' not in request.session.keys():
            return redirect('login')
        
        user = MyUser.objects.get(pk=request.session['user'].get('id'))

        title = request.POST.get('title')
        p_type = request.POST.get('p_type')
        text = request.POST.get('text')
        file = request.FILES.get('file')
        
        # Создаем новый пост
        new_blog = Publication(
            title=title,
            p_type=p_type,
            text=text,
            author=user,
            file=file
        )
        new_blog.save()
        
        return redirect('profile')
    

class DeleteBlogView(View):
    def get(self, request, id):
        if 'user' not in request.session.keys():
            return redirect('login')
        
        user = MyUser.objects.get(pk=request.session['user'].get('id'))
        
        blog = get_object_or_404(Publication, id=id)
        
        # Проверяем, является ли пользователь автором блога
        if blog.author != user:
            return HttpResponseForbidden("You do not have permission to delete this blog.")
        
        # Удаляем блог
        blog.delete()
        
        # Перенаправляем на страницу профиля
        return redirect('profile')
    

class UpdateBlogView(View):
    def get(self, request, id):
        if 'user' not in request.session.keys():
            return redirect('login')
        user = MyUser.objects.get(pk=request.session['user'].get('id'))
        
        blog = get_object_or_404(Publication, id=id)

        if blog.author != user:
            return HttpResponseForbidden("You do not have permission to delete this blog.")

        return render(request, 'updateblog.html')

    def post(self, request, id):
        if 'user' not in request.session.keys():
            return redirect('login')
        
        user = MyUser.objects.get(pk=request.session['user'].get('id'))
        
        if not id:
            return HttpResponseForbidden("Blog ID is required.")
        
        blog = get_object_or_404(Publication, id=id)
        
        if blog.author != user:    
            return HttpResponseForbidden("You do not have permission to update this blog.")
        
        data = request.POST

        if data['title'] != '':
            blog.title = request.POST['title']
        if data['p_type'] != '':
            blog.p_type = request.POST['p_type']
        if data['text'] != '':
            blog.text = request.POST['text']
        if data['file'] != '':
            blog.file = request.FILES['file']
        
        blog.save()
        
        return redirect('profile')
    

class UpdateProfileView(View):
    def get(self, request):
        if 'user' not in request.session.keys():
            return redirect('login')
        user = MyUser.objects.get(pk=request.session['user'].get('id'))

        if 'user' not in request.session.keys():
            return redirect('login')
        return render(request, 'updateprofile.html')

    def post(self, request):
        if 'user' not in request.session.keys():
            return redirect('login')
        
        user = get_object_or_404(MyUser, id=request.session['user'].get('id'))
        

        
        data = request.POST

        if data['username'] != '':
            user.username = request.POST['username']
        if data['avatar'] != '':
            user.p_type = request.POST['avatar']
        if data['description'] != '':
            user.text = request.POST['description']
        
        user.save()
        
        return redirect('profile')
    

class PublicationCommentsView(View):
    def get(self, request, id):
        publication = get_object_or_404(Publication, id=id)
        comments = Comment.objects.filter(publication=publication).order_by('-id')
        comms = []
        for i in range(len(comments) - 1, -1, -1):
            dat = CommentSerializer(instance=comments[i]).data
            print(dat, 11111111111111111111111111111111111)
            comms.append(dat)
        return render(
            request, 
            'comments.html', 
            {
                'publication': publication, 
                'comments': comms
            })

    def post(self, request, id):
        publication = get_object_or_404(Publication, id=id)
        text = request.POST.get('text', '').strip()
        user = MyUser.objects.get(pk=request.session['user'].get('id'))
        if text:
            Comment.objects.create(
                author=user,  
                publication=publication,
                text=text
            )

        return redirect('comments', id=id) 


class RegistrationView(View):
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):
        email = request.POST.get('email')
        username = request.POST.get('username')
        avatar = request.FILES.get('avatar')
        password = request.POST.get('password')

        try:
            user = MyUser.objects.create_user(
                email=email,
                username=username,
                password=password,
                avatar=avatar
            )
            login(request, user)  
            return redirect('main') 
        except Exception as e:
            return HttpResponse(f"Ошибка: {str(e)}", status=400)


class LoginView(APIView):
    querylist: MyUser = MyUser.objects.all()
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        try:
            user: MyUser = self.querylist.get(email=request.POST.get("email"))
            serializer = MyUserSerializer(
                instance=user
            )
            user = serializer.data
            request.session["user"] = {
                    "id": user.get("id"),
                    "email": user.get("email"),
                    "username": user.get("username"),
                    "avatar": user.get("avatar")
                }
            request.session.modified = True
            return redirect('blogs')
        except MyUser.DoesNotExist:
            raise ValidationError('Object Does NOT exists', code=404)


class LogoutView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        del request.session['user']
        return redirect('main')
