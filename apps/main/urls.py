from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from main.views import (
    MainView,
    BlogsView,
    CreateBlogView,
    DeleteBlogView,
    UpdateBlogView,
    ProfileView,
    PublicationCommentsView,
    UpdateProfileView,
    LoginView,
    LogoutView,
    RegistrationView
)



urlpatterns = [
    path('', MainView.as_view(), name='main'),
    path('blogs/', BlogsView.as_view(), name='blogs'),
    path('blogs/comments/<int:id>', PublicationCommentsView.as_view(), name='comments'),
    path('blogs/profile', ProfileView.as_view(), name='profile'),
    path('blogs/profile/new', CreateBlogView.as_view(), name='create'),
    path('blogs/profile/update', UpdateProfileView.as_view(), name='update_p'),
    path('blogs/delete/<int:id>', DeleteBlogView.as_view(), name='delete'),
    path('blogs/update/<int:id>', UpdateBlogView.as_view(), name='update'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]

urlpatterns += static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
)
urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT
)