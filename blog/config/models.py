from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string
# Create your models here.

class Link(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEM=[
        (STATUS_NORMAL,"正常"),
        (STATUS_DELETE,"删除"),
    ]
    title=models.CharField(max_length=50,verbose_name="标题")
    href=models.URLField(verbose_name="链接")
    status=models.PositiveIntegerField(choices=STATUS_ITEM,verbose_name="状态")
    weight=models.PositiveIntegerField(default=1,choices=zip(range(1,6),range(1,6)),verbose_name="权重",
                                       help_text="权重越高,排名越靠前")
    owner=models.ForeignKey(User,verbose_name="作者")
    created_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name=verbose_name_plural="友链"

class SiderBar(models.Model):
    STATUS_SHOW=1
    STATUS_HIDE=0
    STATUS_ITEM=[
        (STATUS_SHOW,"展示"),
        (STATUS_HIDE,"隐藏"),
    ]

    DISPLAY_HTML=1
    DISPLAY_LATEST=2
    DISPLAY_HOT=3
    DISPLAY_COMMENT=4
    SIDE_TYPE=[
        (DISPLAY_HTML,"HTML"),
        (DISPLAY_LATEST,"最新文章"),
        (DISPLAY_HOT,"最热文章"),
        (DISPLAY_COMMENT,"最近评论"),
    ]
    title=models.CharField(max_length=50,verbose_name="标题",blank=True)
    display_type=models.PositiveIntegerField(default=1,choices=SIDE_TYPE,verbose_name="展示类型")
    content=models.CharField(max_length=500,blank=True,verbose_name="内容")
    status=models.PositiveIntegerField(choices=STATUS_ITEM,verbose_name="状态",default=STATUS_SHOW)
    owner=models.ForeignKey(User,verbose_name="作者")
    created_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")

    @property
    def content_html(self):
        """直接渲染模板"""
        from main.models import Post  # 避免循环引用
        from comment.models import Comment

        result=''
        show_items_num=5
        if self.display_type==self.DISPLAY_HTML:
            result=self.content
        elif self.display_type==self.DISPLAY_LATEST:
            context={
                'posts':Post.latest_posts()[:show_items_num]
            }
            tes=render_to_string('config/blocks/sidebar_posts.html',context=context)
            result=render_to_string('config/blocks/sidebar_posts.html',context=context)
        elif self.display_type==self.DISPLAY_HOT:
            context={
                'posts': Post.hot_posts()[:show_items_num],
            }
            result=render_to_string('config/blocks/sidebar_posts.html',context=context)
        elif self.display_type==self.DISPLAY_COMMENT:
            context={
                'comments': Comment.objects.filter(status=Comment.STATUS_NORMAL)[:show_items_num]
            }
            result=render_to_string('config/blocks/sidebar_comments.html',context=context)

        return result

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    class Meta:
        verbose_name=verbose_name_plural="侧栏"
