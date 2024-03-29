from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed

from main.models import Post

class ExtendedRSSFeed(Rss201rev2Feed):
    def add_item_elements(self, handler, item):
        super(ExtendedRSSFeed,self).add_item_elements(handler,item)
        handler.addQuickElement('content',item['content'])

class LatestPostFeed(Feed):
    feed_type = ExtendedRSSFeed
    title = "Blog System"
    link="/rss/"
    description="This is the blog system"

    def items(self):
        return Post.objects.filter(status=Post.STATUS_NORMAL)[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.desc

    def item_link(self, item):
        return reverse('post_detail',args=[item.pk,])

    def item_extra_kwargs(self, item):
        return {'content':item.content}