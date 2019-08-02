from django.shortcuts import render,get_object_or_404
from django.views.generic import DetailView,ListView
from django.db.models import Q,F
from django.core.cache import cache

from .models import Category,Tag,Post
from config.models import SiderBar
from comment.models import Comment


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 2  # 每一页的数量
    context_object_name = 'post_list'
    template_name = 'main/list.html'

class CommonViewMixin():
    def get_context_data(self,**kwargs):
        context=super(CommonViewMixin, self).get_context_data(**kwargs)
        context.update({
            'sidebars':SiderBar.get_all(),
        })
        context.update(Category.get_nav())
        return context

class IndexView(CommonViewMixin,ListView):
    model = Post
    paginate_by = 6
    template_name = 'main/list.html'
    context_object_name = 'post_list'
    queryset = Post.latest_posts()


class CategoryView(IndexView):
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        category_id=self.kwargs.get('category_id')
        # category=Category.objects.filter(id=category_id)
        category=get_object_or_404(Category,pk=category_id)
        context.update({
            'category':category,
        })
        return context

    def get_queryset(self):
        qs=super().get_queryset()
        category_id=self.kwargs.get('category_id')
        return qs.filter(id=category_id)


class TagView(IndexView):
    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        tag_id=self.kwargs.get('tag_id')
        tag=get_object_or_404(Tag,pk=tag_id)
        context.update({
            'tag':tag,
        })
        return context

    def get_queryset(self):
        qs=super().get_queryset()
        tag_id=self.kwargs.get('tag_id')
        return qs.filter(id=tag_id)

class PostDetailView(CommonViewMixin,DetailView):
    queryset = Post.latest_posts()
    context_object_name = 'post'
    template_name = 'main/detail.html'
    pk_url_kwarg = 'post_id'

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        context.update({
            # 'comment_list':Comment.get_by_target(self.request.path)
            'comment_list':Comment.get_by_target_id(self.kwargs.get(self.pk_url_kwarg)),
        })
        return context

    def get(self,request,*args,**kwargs):
        response=super().get(request,*args,*kwargs)
        self.handle_visited()
        return response

    def handle_visited(self):
        increase_pv=False
        uid=self.request.uid
        pv_uid='{}:{}'.format(uid,self.request.path)
        print(pv_uid)
        if not cache.get(pv_uid):
            increase_pv=True
            cache.set(pv_uid,1,10*60)

        if increase_pv:
            Post.objects.filter(id=self.object.id).update(pv=F('pv')+1)

class SearchView(IndexView):
    def get_context_data(self,**kwargs):
        keyword=self.request.GET.get('keyword','')
        context=super().get_context_data(**kwargs)
        context.update({
            'keyword':keyword,
        })
        return context

    def get_queryset(self):
        keyword=self.request.GET.get('keyword')
        qs=super().get_queryset()
        if keyword:
            return qs.filter(Q(title__icontains=keyword) |
                             Q(desc__icontains=keyword) |
                             Q(owner__icontains=keyword))
        return qs


class AuthorView(IndexView):
    def get_queryset(self):
        qs=super().get_queryset()
        auther_id=self.kwargs.get('author_id')
        if not auther_id:
            return qs
        return qs.filter(owner_id=auther_id)
