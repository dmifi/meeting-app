import os

from PIL import Image

from django.conf import settings
from django.core.files.storage import default_storage


def add_watermark(client_model):
    """Добаляет водяной знак"""

    watermark = Image.open(settings.MEDIA_ROOT + '/watermark.png')
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')

    avatar = Image.open(client_model.avatar)
    if avatar.mode != 'RGBA':
        avatar = avatar.convert('RGBA')

    if not os.path.exists(os.path.join(settings.MEDIA_ROOT, f'original/{client_model.email}')):
        os.makedirs(os.path.join(settings.MEDIA_ROOT, f'original/{client_model.email}'))

    img_name = str(client_model.avatar).split('/')[-1]

    wm_avatar = avatar.copy()
    wm_avatar.paste(watermark, (0, 0), watermark)
    wm_avatar.convert('RGB')

    path_original = f'{settings.MEDIA_ROOT}/original/{client_model.email}/{img_name}'
    path_avatar = f'{settings.MEDIA_ROOT}/avatar/{client_model.email}/{img_name}'
    with default_storage.open(path_avatar, 'wb') as wm_avatar_file:
        wm_avatar.save(wm_avatar_file, 'PNG', optimize=True, progressive=True)
    with default_storage.open(path_original, 'wb') as avatar_file:
        avatar.save(avatar_file, 'PNG', optimize=True, progressive=True)

