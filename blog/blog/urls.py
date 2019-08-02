"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib.sitemaps.views import sitemap
from django.conf import settings
from django.conf.urls.static import static

import xadmin
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls

from .autocomplete import CategoryAutocomplete,TagAutocomplete

from .site import main_site,permission_site
from main.views import AuthorView,SearchView,PostDetailView,IndexView,CategoryView,TagView
from config.views import LinkView
from comment.views import CommentView
from .rss import LatestPostFeed
from .sitemap import PostSitemap
from main.apis import post_list,PostList,PostViewSet,CategoryViewSet

router=DefaultRouter()
router.register(r'post',PostViewSet,base_name='api-post')
router.register(r'category',CategoryViewSet,base_name='api-category')

urlpatterns = [
    url(r'^$',IndexView.as_view(),name='index'),
    url(r'^author/(?P<author_id>\d+)',AuthorView.as_view(),name='author'),
    url(r'^search/$',SearchView.as_view(),name='search'),
    url(r'^comment/$',CommentView.as_view(),name="comment"),
    url(r'^category/(?P<category_id>\d+)$',CategoryView.as_view(),name='category_list'),
    url(r'^tag/(?P<tag_id>\d+)$',TagView.as_view(),name='tag_list'),
    url(r'^post/(?P<post_id>\d+).html$',PostDetailView.as_view(),name='post_detail'),
    url(r'^links$',LinkView.as_view(),name='links'),
    url(r'^rss/',LatestPostFeed(),name='rss'),
    url(r'^sitemap\.xml$',sitemap,{'sitemaps':{'posts':PostSitemap}},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^category-autocomplete/$',CategoryAutocomplete.as_view(),name='category-autocomplete'),
    url(r'^tag-autocomplete/$',TagAutocomplete.as_view(),name='tag-autocomplete'),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^admin/', xadmin.site.urls,name='main_admin'),
    url(r'^super_admin/', permission_site.urls,name='super_admin'),
    url(r'^api/post_list/',post_list,name='post-list'),
    url(r'^api/postList/',PostList.as_view(),name='PostList'),
    url(r'^api/',include(router.urls,namespace='api')),
    url(r'^api/docs/',include_docs_urls(title='blog api')),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

