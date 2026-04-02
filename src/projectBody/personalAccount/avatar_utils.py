import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile

def handle_avatar_upload(user, uploaded_file):
    """
    Сохраняет аватар пользователя и возвращает путь к файлу.
    Удаляет все предыдущие аватары пользователя.
    """
    try:
        profile = user.profile
        
        # Удаляем все существующие аватары пользователя
        if profile.avatar:
            if default_storage.exists(profile.avatar.name):
                default_storage.delete(profile.avatar.name)
        
        # Генерируем путь и имя файла
        file_ext = os.path.splitext(uploaded_file.name)[1].lower()
        avatar_dir = f"avatars/user_{user.id}/"
        filename = f"{avatar_dir}avatar{file_ext}"
        
        # Создаем папку, если её нет
        if not default_storage.exists(avatar_dir):
            os.makedirs(os.path.join(default_storage.location, avatar_dir), exist_ok=True)
        
        # Удаляем все файлы в папке пользователя перед сохранением нового
        if default_storage.exists(avatar_dir):
            for old_file in default_storage.listdir(avatar_dir)[1]:
                default_storage.delete(os.path.join(avatar_dir, old_file))
        
        # Сохраняем новый файл
        file_content = ContentFile(uploaded_file.read())
        saved_path = default_storage.save(filename, file_content)
        return saved_path
    except Exception as e:
        raise Exception(f"Ошибка при сохранении аватара: {str(e)}")