from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from users.utils import add_watermark


class MyUserManager(BaseUserManager):
    """Метод для создания пользователя."""

    def _create_user(self, first_name, last_name, email, sex, avatar, password, **extra_fields):
        if not first_name:
            raise ValueError("Введите имя")
        if not last_name:
            raise ValueError("Введите фамилию")
        if not sex:
            raise ValueError("Выберите пол")
        if not avatar:
            raise ValueError("Загрузите изображение")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            sex=sex,
            avatar=avatar,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, first_name, last_name, email, sex, avatar, password):
        """Метод для создания обычного пользователя."""
        return self._create_user(first_name, last_name, email, sex, avatar, password)

    def create_superuser(self, first_name, last_name, email, sex, avatar, password):
        """Метод для создания суперпользователя."""
        return self._create_user(first_name, last_name, email, sex, avatar, password, is_staff=True, is_superuser=True)


def upload_image(instance, filename):
    """Определяет путь загрузки файлов (изображений)."""
    return f'avatar/{instance.email}/{filename}'


class Client(AbstractBaseUser, PermissionsMixin):
    """ Модель пользователя."""

    SEX_CHOICES = (
        ("М", "Мужчина"),
        ("Ж", "Женщина")
    )

    first_name = models.CharField(max_length=255, verbose_name="Имя")
    last_name = models.CharField(max_length=255, verbose_name="Фамилия")
    email = models.EmailField(max_length=255, unique=True, verbose_name="Адрес электронной почты")
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, verbose_name="Пол")
    avatar = models.ImageField(upload_to=upload_image, verbose_name="Аватар")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # match = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name="Симпатии с пользователями",
    #                           null=True, on_delete=models.CASCADE)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'sex', 'avatar']

    objects = MyUserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    # def save(self):
    #     """Добавлем водяной знак к изображению пользователя"""
    #     add_watermark(self)
    #     super(Client, self).save()


class Match(models.Model):
    """Симпатии между пользователями"""
    from_match = models.ForeignKey('Client', related_name='from_match', on_delete=models.CASCADE)
    to_match = models.ForeignKey('Client', related_name="to_match", on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['from_match', 'to_match'], name="unique_matching")
        ]

    def __str__(self):
        return f'{self.from_match} match with {self.to_match}'


@receiver(post_save, sender=Client)
def create_watermark(sender, instance, **kwargs):
    """Добавлем водяной знак к изображению пользователя"""
    add_watermark(instance)
