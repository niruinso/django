from django.db import models
from users.models import User
from django.core.files.storage import default_storage
import os


def user_avatar_path(instance, filename):
    # Формируем путь: media/avatars/user_<id>/<filename>
    return f'avatars/user_{instance.user.id}/{filename}'

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=20, unique=True)
    registration_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.unique_id} - {self.user.email}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(
        upload_to=user_avatar_path,
        null=True, 
        blank=True,
        storage=default_storage
    )

    def save(self, *args, **kwargs):
        # При сохранении убедимся, что это единственный аватар пользователя
        if self.avatar:
            # Получаем все профили пользователя (должен быть только один)
            profiles = Profile.objects.filter(user=self.user)
            for profile in profiles:
                if profile.id != self.id and profile.avatar:
                    # Удаляем аватар у других профилей (на случай дублирования)
                    profile.delete_avatar()
        super().save(*args, **kwargs)

    def delete_avatar(self):
        if self.avatar and default_storage.exists(self.avatar.path):
            default_storage.delete(self.avatar.path)
        self.avatar = None
        self.save()

    def delete(self, *args, **kwargs):
        if self.avatar:
            default_storage.delete(self.avatar.path)
        super().delete(*args, **kwargs)