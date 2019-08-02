from django import forms
from dal import autocomplete
from ckeditor_uploader.widgets import CKEditorUploadingWidget

from main.models import Tag,Category,Post

class PostAdminForm(forms.ModelForm):
    # content=forms.CharField(widget=CKEditorUploadingWidget(),label='正文',required=True)
    desc=forms.CharField(widget=forms.Textarea,label="摘要",required=False)
    category=forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=autocomplete.ModelSelect2(url='category-autocomplete'),
        label='分类'
    )

    tag=forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=autocomplete.ModelSelect2Multiple(url='tag-autocomplete'),
        label='标签'
    )

    content_ck=forms.CharField(widget=CKEditorUploadingWidget(),label="正文",required=False)

    content_md=forms.CharField(widget=forms.Textarea,label="正文",required=False)

    content=forms.CharField(widget=forms.HiddenInput(),required=False)

    class Meta:
        model=Post
        fields=('category','tag','title','desc','content','status')


    def __init__(self,instance=None,initial=None,**kwargs):
        initial=initial or {}
        if instance:
            if instance.is_md:
                initial['content_md']=instance.content
            else:
                initial['content_ck']=instance.content

        super().__init__(instance=instance,initial=initial,**kwargs)


    def clean(self):
        is_md=self.cleaned_data.get('is_md')
        if is_md:
            content_key='content_md'
        else:
            content_key='content_ck'

        content=self.cleaned_data[content_key]
        if not content:
            self.add_error(content_key,'内容不能为空！')
            return
        self.cleaned_data['content']=content

    class Media:
        js=('js/post_editor.js',)
