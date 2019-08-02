import mistune

from django.http import JsonResponse
from django.views import View

from comment.models import  Comment
from main.models import Post

class CommentView(View):

    def post(self,request,*args,**kwargs):
        target_id=request.POST.get('post_id')
        target=Post.objects.filter(id=target_id)[0]
        content=request.POST.get('content')

        # content=mistune.markdown(raw_content)

        nickname=request.user.username
        comment=Comment()
        success=True
        msg=''
        if nickname:
            comment.nickname=nickname
        else:
            msg="必须登陆才能评论！"
            success=False

        if success:
            comment.content=content
            comment.target=target
            comment.save()

        return JsonResponse(data={'success':success,'msg':msg})



