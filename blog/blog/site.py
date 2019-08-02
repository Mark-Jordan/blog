from django.contrib import admin


class MainAdminSite(admin.AdminSite):
    site_header = "Blog 管理后台"
    site_title = "blog"
    index_title = "首页"


class PermissionAdminSite(admin.AdminSite):
    site_title = '权限管理'
    site_header = "权限管理"
    index_title = "首页"


main_site=MainAdminSite(name="main_site")
# main_site=admin.site
# permission_site=PermissionAdminSite(name="main_site")
permission_site=admin.site
permission_site.site_header="权限管理"
permission_site.site_title="权限管理"
permission_site.index_title="首页"