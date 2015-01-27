# coding:utf-8
from django.views.generic import ListView, DetailView
from models import Post, Category, Page, Widget
from django.core.paginator import Paginator
from flyblog import settings
from django.db.models import Q

#公共的context内容
class BaseMixin(object):

    def add_context_data(self, **kwargs):
        try:
            #这里重载了ListView的get_context_data方法
            context = super(IndexView, self).get_context_data(**kwargs)
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(settings.RECENTLY_NUM)
            context['hot_posts'] = Post.get_hots_posts(settings.HOT_NUM)
            context['pages'] = Page.objects.filter(status=0)
            context['title'] = 'Younfor'
            context['desc'] = 'python,c,c++,java,linux,生活感悟，工作笔记，心情驿站'
            context['keywords'] = 'python,c,c++,java,linux,生活感悟，工作笔记，心情驿站'
            context['author'] = 'younfor'
            context['sitename'] = 'Younfor\'s blog'
            context['blogdesc'] = '悄悄是别离的笙箫，所谓爱情，所谓人生，所谓。'
        except Exception as e:
            print e
        return context

#首页的view
class IndexView(BaseMixin, ListView):
    query = None
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        #这里专门获取get提交的分页参数
        try:
            self.cur_page = int(request.GET.get('page', 1))
        except TypeError:
            self.cur_page = 1

        if self.cur_page < 1:
            self.cur_page = 1

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        #print 'get_context_data'
        paginator = Paginator(self.object_list, settings.PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        return super(IndexView, self).add_context_data(**kwargs)

    def get_queryset(self):
        #获取文章搜索字段
        self.query = self.request.GET.get('s')
        if self.query:
            qset = (
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query)
            )
            posts = Post.objects.defer('content', 'content_html')\
                .filter(qset, status=0)
            for post in posts:
                post.title = post.title.replace(self.query, '<span class="hightline">%s</span>' % self.query)
        else:
            posts = Post.objects.defer('content', 'content_html')\
                .filter(status=0)
        return posts
