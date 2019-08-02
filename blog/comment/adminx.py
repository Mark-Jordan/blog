from django.contrib import admin
from django.contrib.admin.filters import SimpleListFilter
import xadmin

from .models import Comment
from blog.site import main_site
from django.contrib.admin import ModelAdmin

from .forms import CommentForm

@xadmin.sites.register(Comment)
class CommentAdmin():
    # form=CommentForm
    list_display = [
        'target',
        'nickname',
        # 'website',
        'status',
        'created_time'
    ]

    # amdin 过滤器的使用方法
    # class PostFilter(SimpleListFilter):
    #     title = "文章"
    #     parameter_name = "post"
    #
    #     def lookups(self, request, model_admin):
    #         return Post.objects.filter(owner=request.user).values_list('id','title')
    #
    #     def queryset(self, request, queryset):
    #         if self.value():
    #             print(self.value())
    #             print(queryset)
    #             return queryset.filter(target_id=self.value())

    list_filter = ['created_time','status']


    fields = ['target','nickname','content','status']

    def get_list_queryset(self):
        request=self.request
        qs=super().get_list_queryset()
        return qs.filter(target__owner=request.user)
