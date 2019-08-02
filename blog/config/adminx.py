from django.contrib import admin

import xadmin

from .models import Link,SiderBar
from blog.site import main_site
from blog.base_admin import BaseOwnerModelAdmin


# @admin.register(Link,site=main_site)
class LinkAdmin(BaseOwnerModelAdmin):
    list_display=('title','status','owner','created_time')

    fields = (
        'title',
        'status',
        'href',
        'weight',
    )

    list_filter = ['status','created_time']

    def save_model(self, request, obj, form, change):
        obj.owner=request.user
        return super(LinkAdmin,self).save_model(request,obj,form,change)


@xadmin.sites.register(SiderBar)
class SiderBarAdmin(BaseOwnerModelAdmin):
    list_display=['title','status','owner','created_time']

    fields = [
        'title',
        'status',
        'display_type',
        'content',
    ]


    list_filter = ['display_type','created_time']

    @property
    def media(self):
        media=super().media
        media.add_js(['js/sidebar.js',])
        return media



