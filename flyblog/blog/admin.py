# coding:utf-8
from django.contrib import admin
from django.core import urlresolvers
from models import Post
from models import Category
from models import Page
from models import Widget
import hashlib
from tinymce.widgets import TinyMCE
from django import forms
from pagedown.widgets import AdminPagedownWidget
from ckeditor.widgets import CKEditorWidget
# 文章管理


class PostForm(forms.ModelForm):
    #content = forms.CharField(label=u'内容',widget=AdminPagedownWidget())

    '''tinymce
    content = forms.CharField(
        label=u'内容',
        widget=TinyMCE(
            attrs={'style': 'width:600px;height:500px;'},
        )
    )
    '''
    content = forms.CharField(
        label=u'内容',
        widget=CKEditorWidget()
    )
    summary = forms.CharField(label=u'摘要', required=False,
                              widget=forms.Textarea(attrs={'style': 'width:500px;height:100px;'}))

    class Meta:
        model = Post
        fields = ('title', 'alias', 'is_top', 'is_old', 'pub_time',  'tags', 'status',
                  'category', 'summary', 'content')


class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'alias')
    fields = ('title', 'alias', 'is_top', 'is_old', 'pub_time',  'tags', 'status',
              'category', 'summary', 'content')
    list_display = ('preview', 'title', 'category', 'is_top', 'pub_time')
    list_display_links = ('title', )

    ordering = ('-pub_time', )
    list_per_page = 15
    save_on_top = True
    form = PostForm
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


class CategoryAdmin(admin.ModelAdmin):
    search_fields = ('name', 'alias')
    list_display = ('name', 'rank', 'is_nav', 'status', 'create_time')


class PageAdmin(admin.ModelAdmin):
    search_fields = ('name', 'alias')
    fields = ('title', 'alias', 'link', 'content', 'is_html', 'status', 'rank')
    list_display = ('title', 'link', 'rank', 'status', 'is_html')

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.content_html = obj.content
        obj.save()


class WidgetAdmin(admin.ModelAdmin):
    search_fields = ('name', 'alias')
    fields = ('title', 'content', 'rank', 'hide')
    list_display = ('title', 'rank', 'hide')


# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Widget, WidgetAdmin)
