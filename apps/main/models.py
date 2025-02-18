from django.db import models
import datetime
from django.utils import timezone 
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError


class MyUserManager(BaseUserManager):
    """ClientManager."""

    def create_user(
        self,
        email: str,
        username: str,
        avatar: str,
        password: str
    ) -> 'MyUser':

        if not email:
            raise ValidationError('email required')
        if not username:
            raise ValidationError('nickname required')

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            username=username,
            avatar=avatar,
            password=password
        )
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return custom_user

    def create_superuser(
        self,
        email: str,
        password: str
    ) -> 'MyUser':

        custom_user: 'MyUser' = self.model(
            email=self.normalize_email(email),
            password=password
        )
        custom_user.is_superuser = True
        custom_user.is_active = True
        custom_user.is_staff = True
        custom_user.set_password(password)
        custom_user.save(using=self._db)
        return
    

class MyUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(
        verbose_name='почта/логин',
        unique=True,
        max_length=200
    )
    username = models.CharField(
        verbose_name='ник',
        max_length=20
    )
    avatar = models.ImageField(
        verbose_name="изображение",
        upload_to='avatars/',
        default='avatars/unknown.png'
    )
    description = models.CharField(
        verbose_name='описание',
        max_length=100,
        default=""
    )
    is_staff = models.BooleanField(
        verbose_name='staff',
        default=False
    )
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='myuser_groups',  # Уникальное имя для обратной связи
        related_query_name='myuser'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='myuser_permissions',  # Уникальное имя для обратной связи
        related_query_name='myuser'
    )
    
    objects = MyUserManager()

    REQUIRED_FIELDS = []
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Publication(models.Model):
    class Categories(models.TextChoices):
        GAME = 'game'
        LIFE = 'life'

    title = models.CharField(
        verbose_name='титульник',
        max_length=50
    )
    p_type = models.CharField(
        verbose_name='категория',
        max_length=6,
        choices=Categories.choices,
        default=Categories.LIFE
    )
    author = models.ForeignKey(
        verbose_name='автор поста',
        related_name='posts',
        to=MyUser,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name='текст',
        max_length=1000,
        null=True
    )
    file = models.ImageField(
        verbose_name="пост",
        upload_to='img/',
        default='img/unknown.png'
    )


class Comment(models.Model):
    author = models.ForeignKey(
        verbose_name='автор комента',
        related_name='comments',
        to=MyUser,
        on_delete=models.CASCADE
    )
    publication = models.ForeignKey(
        verbose_name='пост',
        related_name='cpost',
        to=Publication,
        on_delete=models.CASCADE
    )
    text = models.CharField(
        verbose_name='камент',
        max_length=150
    )
