# coding:utf-8
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from models import Post, Category, Page, Widget
from django.core.paginator import Paginator
from flyblog import settings
# Create your views here.
class BaseMixin(object):

    def get_context_data(self, *args, **kwargs):
        if 'object' in kwargs or 'query' in kwargs:
            context = super(BaseMixin, self).get_context_data(**kwargs)
        else:
            context = {}

        try:
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(RECENTLY_NUM)
            context['hot_posts'] = Post.get_hots_posts(HOT_NUM)
            context['pages'] = Page.objects.filter(status=0)
            context['online_num'] = len(cache.get('online_ips', []))
        except Exception as e:
            #logger.exception(u'加载基本信息出错[%s]！', e)
            print e
        return context


class IndexView(BaseMixin, ListView):
    query = None
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        try:
            self.cur_page = int(request.GET.get('page', 1))
        except TypeError:
            self.cur_page = 1

        if self.cur_page < 1:
            self.cur_page = 1

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        paginator = Paginator(self.object_list, settings.PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        return super(IndexView, self).get_context_data(**kwargs)

    def get_queryset(self):
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
                post.summary = post.summary.replace(self.query, '<span class="hightline">%s</span>' % self.query)
        else:
            posts = Post.objects.defer('content', 'content_html')\
                .filter(status=0)

        return posts
