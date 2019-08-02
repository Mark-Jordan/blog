from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry

from xadmin.layout import Row,Fieldset,Container
import xadmin
from xadmin.filters import RelatedFieldListFilter,manager

from .models import Post,Category,Tag
from .adminForms import PostAdminForm
from  blog.site import main_site
from blog.base_admin import BaseOwnerModelAdmin


class PostInline:
    # xamdin 处理inline
    form_layout = (
        Container(
            Row('title', 'desc'),
        )
    )

    # admin的使用方法
    # fields = ('title', 'desc')
    extra = 1
    model = Post

@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerModelAdmin):
    list_display = ('name','status','owner','created_time','post_count')
    fields = ('name','status','is_nav','created_time')

    inlines = [PostInline, ]


    # admin用法
    # fieldsets = (
    #     ('分类',{
    #         'fields':(
    #             'name','status','is_nav','created_time'
    #         ),
    #         'description':'分类配置',
    #         'classes':('all',),
    #     }),
    # )


    def post_count(self,obj):
        return obj.post_set.count()

    post_count.short_description = "文章总数"

    list_filter = ['status','is_nav','created_time']


    # admin自定义静态资源引入
    class Media:
        css={
            'all':('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/css/',),
        }
        js=('https://cdn.bootcss.com/bootstrap/4.0.0-beta.2/js/bootstrap.bundle.js',)

@xadmin.sites.register(Tag,site=main_site)
class TagAdmin(BaseOwnerModelAdmin):
    list_display = ('name','status','owner','created_time')
    fields = ('name','status','created_time')

    list_filter = ['status','created_time']


@xadmin.sites.register(Post)
class PostAdmin(BaseOwnerModelAdmin):
    form = PostAdminForm

    list_display = ('title','status','category','owner','created_time','operator')
    list_display_links = []

    form_layout=(
        Fieldset(
            '基础信息',
            Row('title','category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content'
        )
    )

    # admin 过滤器
    # class PostOwnerFilter(SimpleListFilter):
    #     title = '分类'
    #     parameter_name = 'owner_category'
    #     def lookups(self, request, model_admin):
    #         return Category.objects.filter(owner=request.user).values_list('id','name')
    #
    #     def queryset(self, request, queryset):
    #         if self.value():
    #             return queryset.filter(category_id=self.value())
    #         return queryset

    # list_filter = [PostOwnerFilter,]

    # xadmin过滤器
    class CategoryOwnerFilter(RelatedFieldListFilter):
        @classmethod
        def test(cls, field, request, params, model, admin_view, field_path):
            return field.name == 'category'

        def __init__(self, field, request, params, model, mode_admin, field_path):
            super().__init__(field, request, params, model, mode_admin, field_path)
            self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')

    manager.register(CategoryOwnerFilter, take_priority=True)

    # xadmin的过滤字段的写法，此处只写过滤器过滤的字段名，而不是过滤器名
    list_filter=['category']

    search_fields = ['title','category__name']

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    fields = (
        'category', 'title',
        'desc', 'status', 'is_md','content',
        'tag', 'created_time',
    )

    # xadmin 的编写方法 和 admin中的fieldset 的区别
    form_layout=(
        Fieldset(
            '基础信息',
            Row('title','category'),
            'status',
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content',
        )
    )


    # 配置静态资源（兼容admin和xadmin）
    # @property
    # def media(self):
    #     media=super().media
    #     media.add_js(['the path of the js file',])
    #     media.add_css({'all':('the path of css file',)})
    #     return media

    # filter_horizontal = ('tag',)

    def operator(self,obj):
        if obj.id:
            return format_html(
                '<a href={}>编辑</a>',
                # 法一
                # reverse('xadmin:main_post_change',args=(obj.id,))
                # xadmin 中更友好的方法
                self.model_admin_url('change',obj.id)
            )
        return None
    operator.short_description = '操作'


# @admin.register(LogEntry,site=main_site)
class LogEntryAdmin(object):
    list_display = ['object_repr','object_id','action_flag','user','change_message']