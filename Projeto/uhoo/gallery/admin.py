# -*- coding: utf-8
try:
    import Image
except ImportError:
    from PIL import Image
import os

from models import album, photo
#from sorl.thumbnail.admin import AdminImageMixin
from django.contrib import admin
from django.template import Library

register = Library()

admin.site.register(album)
admin.site.register(photo)


