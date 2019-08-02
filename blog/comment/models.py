from django.db import models

from main.models import Post
# Create your models here.

class Comment(models.Model):
    STATUS_NORMAL=1
    STATUST_DELETE=0
    STATUS_ITEM=[
        (STATUS_NORMAL,"正常"),
        (STATUST_DELETE,"删除"),
    ]
    target=models.ForeignKey(Post,verbose_name="评论文章")
    content=models.CharField(max_length=2000,verbose_name="内容")
    nickname=models.CharField(max_length=50,verbose_name="昵称")
    # website=models.URLField(verbose_name="网站")
    # email=models.EmailField(verbose_name="邮箱")
    status=models.PositiveIntegerField(choices=STATUS_ITEM,default=STATUS_NORMAL,verbose_name="状态")
    created_time=models.DateTimeField(auto_now_add=True,verbose_name="创建时间")


    @classmethod
    def get_by_target_id(cls,target_id):
        return cls.objects.filter(target_id=target_id,status=cls.STATUS_NORMAL)

    class Meta:
        verbose_name=verbose_name_plural="评论"