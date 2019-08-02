from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from main.models import Post

class PostSitemap(Sitemap):
    changefre='always'
    property=1.0
    protocol = 'https'

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)

    def lastmod(self,obj):
        return obj.created_time

    def location(self, obj):
        return reverse('post_detail',args=[obj.pk,])