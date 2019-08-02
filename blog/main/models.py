from django.db import models
from django.contrib.auth.models import User

import mistune
# Create your models here.

class Category(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEM=[
        (STATUS_NORMAL,"正常"),
        (STATUS_DELETE,"删除"),
    ]
    name=models.CharField(max_length=50,verbose_name="名称")
    status=models.PositiveIntegerField(choices=STATUS_ITEM,default=STATUS_NORMAL,verbose_name="状态")
    is_nav=models.BooleanField(default=False,verbose_name="是否为导航")
    owner=models.ForeignKey(User,verbose_name="作者")
    created_time=models.DateTimeField(auto_created=True,verbose_name="创建时间")

    @classmethod
    def get_nav(cls):
        categories=Category.objects.filter(status=Category.STATUS_NORMAL)
        nav_categories=[]
        normal_categories=[]
        for category in categories:
            if category.is_nav:
                nav_categories.append(category)
            else:
                normal_categories.append(category)
        return {
            'navs':nav_categories,
            'categories':normal_categories,
        }

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=verbose_name_plural='分类'


class Tag(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_ITEM=[
        (STATUS_NORMAL,"正常"),
        (STATUS_DELETE,"删除"),
    ]
    name=models.CharField(max_length=10,verbose_name="标签")
    status=models.PositiveIntegerField(choices=STATUS_ITEM,verbose_name="状态",default=STATUS_NORMAL)
    owner=models.ForeignKey(User,verbose_name="作者")
    created_time=models.DateTimeField(auto_created=True,verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name=verbose_name_plural="标签"


class Post(models.Model):
    STATUS_NORMAL=1
    STATUS_DELETE=0
    STATUS_DRAFT=2
    STATUS_ITEM=[
        (STATUS_NORMAL,"正常"),
        (STATUS_DELETE,"删除"),
        (STATUS_DRAFT,"草稿"),
    ]
    title=models.CharField(max_length=255,verbose_name="标题")
    desc=models.CharField(max_length=1024,verbose_name="摘要")
    content=models.TextField(verbose_name="正文")
    content_html=models.TextField(verbose_name="正文html代码",blank=True,editable=False)
    status=models.PositiveIntegerField(choices=STATUS_ITEM,default=STATUS_NORMAL,verbose_name="状态")
    category=models.ForeignKey(Category,verbose_name="分类")
    tag=models.ManyToManyField(Tag,verbose_name="标签",blank=True)
    owner=models.ForeignKey(User,verbose_name="作者")
    created_time=models.DateTimeField(auto_created=True,verbose_name="创建时间")

    pv=models.PositiveIntegerField(default=1)

    is_md=models.BooleanField(verbose_name="是否使用Markdown格式",default=False)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.is_md:
            self.content_html=mistune.markdown(self.content)
        else:
            self.content_html=self.content

        super().save(force_insert,force_update,using,update_fields)

    def __str__(self):
        return self.title

    @classmethod
    def hot_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by('-pv')

    @staticmethod
    def get_by_tag(tag_id):
        try:
            tag=Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            tag=None
            post_list=[]
        else:
            post_list=tag.post_set.filter(status=Tag.STATUS_NORMAL)\
            .select_related('owner','category')

        return post_list,tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category=Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category=None
            post_list=[]
        else:
            post_list=category.post_set.filter(status=Post.STATUS_NORMAL)\
            .select_related('owner','category')
        return post_list,category

    @classmethod
    def latest_posts(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)



    class Meta:
        verbose_name=verbose_name_plural="文章"
        ordering=['-id']  # 根据id进行倒叙排列
