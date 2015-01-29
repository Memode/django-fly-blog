# coding:utf-8
from django.contrib import admin
from django.core import urlresolvers
from models import Post
from models import Category
from models import Page
from models import Widget
import hashlib
# 文章管理


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'alias')
    fields = ('content', 'summary', 'title', 'alias', 'tags', 'status',
              'category', 'is_top', 'is_old', 'pub_time')
    list_display = ('preview', 'title', 'category', 'is_top', 'pub_time')
    list_display_links = ('title', )

    ordering = ('-pub_time', )
    list_per_page = 15
    save_on_top = True
    # 显示字段

    def preview(self, obj):
        url_edit = urlresolvers.reverse(
            'admin:blog_post_change', args=(obj.id,))
        return u'''
                    <span><a href="/%s.html" target="_blank">预览</a></span>
                    <span><a href="%s" target="_blank">编辑</a></span>
                ''' % (obj.alias, url_edit)

    preview.short_description = u'操作'
    preview.allow_tags = True

    # add alias with md5, add user , cut the summary

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if not obj.alias:
            obj.alias = hashlib.md5(obj.title.encode('utf-8')).hexdigest()
        if not obj.summary:
            obj.summary = obj.content[0:min(len(obj.content), 200)]

        obj.content_html = obj.content
        obj.save()


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(Page)
admin.site.register(Widget)
