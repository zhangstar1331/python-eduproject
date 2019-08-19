from django import forms
from .models import UserAsk, UserComment
import re
class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk
        #使用字段较少的话可以单独列出来
        #fields = ['name','phone','course']
        #使用字段较多的话，可以将不需要的字段排除出去
        exclude = ['add_time']
        #如果用到了全部字段，可以用下面的方法
        #fields = '__all__'
    #添加自定义规则
    def clean_phone(self):
        #重新去cleaned_data中将需要的值给取出来
        phone = self.cleaned_data['phone']
        #建立正则对象
        com = re.compile('^(((13[0-9])|(14[579])|(15([0-3]|[5-9]))|(16[6])|(17[0135678])|(18[0-9])|(19[89]))\\d{8})$')
        #如果有返回值，则表示验证成功
        if com.match(phone):
            return phone
        else:
            #验证失败
            raise forms.ValidationError('手机号填写错误')

class UserCommentForm(forms.Form):
    comment_course_id = forms.IntegerField(required=True)
    comment_content = forms.CharField(required=True, min_length=1, max_length=300)
