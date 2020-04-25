from django.db import models
import uuid


# Create your models here.
def scramble_upload_video(instance, filename, subdiretory='mf_video'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


def scramble_upload_wallpapper(instance, filename, subdiretory='mf_wallpapper'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


def scramble_upload_screenshot(instance, filename, subdiretory='mf_screenshot'):
    ext = filename.split('.')[-1]
    return subdiretory+'/{}.{}'.format(uuid.uuid4(), ext)


class MFVideo(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField('mediafan', upload_to=scramble_upload_video)
    date = models.DateField(auto_now_add=True)


class MFWallpapper(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField('mediafan', scramble_upload_wallpapper)


class MFScreenshot(models.Model):
    title = models.CharField(max_length=200)
    picture = models.ImageField('mediafan', scramble_upload_screenshot)
    description = models.TextField(max_length=400)


