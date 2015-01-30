# coding:utf-8
from django.views.generic import ListView, DetailView
from models import Post, Category, Page, Widget
from django.core.paginator import Paginator
from flyblog import settings
from django.db.models import Q, F
from django.shortcuts import render

# 公共的context内容


class BaseMixin(object):

    def add_context_data(self, **kwargs):
        # 这里重载了ListView的get_context_data方法
        context = super(BaseMixin, self).get_context_data(**kwargs)
        try:
            context['categories'] = Category.available_list()
            context['widgets'] = Widget.available_list()
            context['recently_posts'] = Post.get_recently_posts(
                settings.RECENTLY_NUM)
            context['hot_posts'] = Post.get_hots_posts(settings.HOT_NUM)
            context['pages'] = Page.objects.filter(status=0)
            if not context.has_key('title'):
                context['title'] = ''
            context['title'] += 'Younfor'
            context['desc'] = 'python,c,c++,java,linux,生活感悟，工作笔记，心情驿站'
            context['keywords'] = 'python,c,c++,java,linux,生活感悟，工作笔记，心情驿站'
            context['author'] = 'younfor'
            context['sitename'] = 'Younfor\'s BLOG'
            context['blogdesc'] = '悄悄是别离的笙箫，所谓爱情，所谓人生，所谓。'
        except Exception as e:
            print e
        return context

# 首页的view


class IndexView(BaseMixin, ListView):
    query = None
    template_name = 'blog/index.html'

    def get(self, request, *args, **kwargs):
        # 这里专门获取get提交的分页参数
        try:
            self.cur_page = int(request.GET.get('page', 1))
        except TypeError:
            self.cur_page = 1

        if self.cur_page < 1:
            self.cur_page = 1

        return super(IndexView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        # 获取文章搜索字段
        self.query = self.request.GET.get('s')
        if self.query:
            qset = (
                Q(title__icontains=self.query) |
                Q(content__icontains=self.query)
            )
            posts = Post.objects.defer('content', 'content_html')\
                .filter(qset, status=0)
            for post in posts:
                post.title = post.title.replace(
                    self.query, '<span class="hightline">%s</span>' % self.query)
        else:
            posts = Post.objects.defer('content', 'content_html')\
                .filter(status=0)
        return posts

    def get_context_data(self, **kwargs):
        # print 'get_context_data'
        paginator = Paginator(self.object_list, settings.PAGE_NUM)
        kwargs['posts'] = paginator.page(self.cur_page)
        kwargs['query'] = self.query
        return super(IndexView, self).add_context_data(**kwargs)

# 文章详情的view


class PostDetailView(BaseMixin, DetailView):
    object = None
    template_name = 'blog/detail.html'
    queryset = Post.objects.filter(status=0)
    slug_field = 'alias'

    def get(self, request, *args, **kwargs):
        # slug是urls文件的正则匹配
        alias = self.kwargs.get('slug')
        try:
            self.object = self.queryset.get(alias=alias)
        except Post.DoesNotExist:
            print 'page not 2find!'
            context = super(PostDetailView, self).get_context_data(**kwargs)
            return render(request, 'blog/404.html', context)
        # 访问量＋１
        Post.objects.filter(id=self.object.id).update(
            view_times=F('view_times') + 1)
        return super(PostDetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs['related_posts'] = self.object.related_posts
        tags = []
        for post in self.queryset:
            tags += post.tags.split(',')
        kwargs['tags'] = tags
        return super(PostDetailView, self).add_context_data(**kwargs)


class PageDetailView(BaseMixin, DetailView):
    template_name = "blog/page.html"
    queryset = Page.objects.filter(status=0)
    slug_field = 'alias'

    def get(self, request, *args, **kwargs):
        alias = self.kwargs.get('slug')
        try:
            self.object = self.queryset.get(alias=alias)
            context = self.get_context_data(object=self.object)
        except Page.DoesNotExist:
            context = super(PostDetailView, self).get_context_data(**kwargs)
            return render(request, 'blog/404.html', context)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        return super(PageDetailView, self).add_context_data(**kwargs)


class CategoryListView(IndexView):

    def get_queryset(self):
        alias = self.kwargs.get('alias')

        try:
            self.category = Category.objects.get(alias=alias)
        except Category.DoesNotExist:
            return []

        posts = self.category.post_set.defer(
            'content', 'content_html').filter(status=0)
        return posts

    def get_context_data(self, **kwargs):
        if hasattr(self, 'category'):
            kwargs['title'] = self.category.name + ' | '
        return super(CategoryListView, self).get_context_data(**kwargs)


class TagsListView(IndexView):

    def get_queryset(self):
        self.tag = self.kwargs.get('tag')
        posts = Post.objects.defer('content', 'content_html')\
            .filter(tags__icontains=self.tag, status=0)
        return posts

    def get_context_data(self, **kwargs):
        kwargs['title'] = self.tag + ' | '
        return super(TagsListView, self).get_context_data(**kwargs)
