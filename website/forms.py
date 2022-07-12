from django import forms
from .models import User, Comment
from mptt.forms import TreeNodeChoiceField


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'phoneno']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['phoneno'].label = "Phone Number"


class NewCommentForm(forms.ModelForm):
    parent = TreeNodeChoiceField(queryset=Comment.objects.all())

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['parent'].widget.attrs.update(
            {'class': 'd-none'})
        self.fields['parent'].label = ''
        self.fields['parent'].required = False

    class Meta:
        model = Comment
        fields = ('blog', 'parent', 'content')

        widgets = {
            'content': forms.Textarea(attrs={'class': 'ml-3 mb-3 form-control border-0 comment-add rounded-0', 'rows': '1', 'placeholder': 'Add a public comment'}),
        }

    def save(self, *args, **kwargs):
        Comment.objects.rebuild()
        return super(NewCommentForm, self).save(*args, **kwargs)
