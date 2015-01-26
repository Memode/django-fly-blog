from django.contrib import admin
from django.core import urlresolvers
from models import Post
from models import Category
from models import Page
from models import Widget
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Widget)