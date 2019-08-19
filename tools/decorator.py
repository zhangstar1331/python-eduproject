from django.shortcuts import redirect,reverse
def decorator_login(func):
    def inner(request,*args,**kwargs):
        #用户如果登录了，就走之前的逻辑
        if request.user.is_authenticated:
            return func(request,*args,**kwargs)
        else:
            #保存当前url地址，使得登录之后跳转到当前页面
            url = request.get_full_path()
            ret = redirect(reverse('users:user_login'))
            ret.set_cookie('url',url)
            return ret
    return inner