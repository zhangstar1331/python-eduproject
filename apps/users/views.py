from django.shortcuts import render,HttpResponse,redirect,reverse
from .forms import UserRegisterForm,UserLoginForm,UserForgetForm,UserResetForm,UserChangeImageForm,UserChangeInfoForm,UserChangeEmailForm,UserResetEmailForm
from .models import UserProfile,EmailVerifyCode
from apps.courses.models import CourseInfo
from  apps.orgs.models import OrgInfo,TeacherInfo
from apps.operations.models import UserLove,UserMessage
from django.db.models import Q
from django.contrib.auth import authenticate,login,logout
from tools.send_email_tool import send_email_code
from django.http import JsonResponse
from datetime import datetime
from django.views.generic import View
def index(request):
    course_list = CourseInfo.objects.all()
    org_list = OrgInfo.objects.all()
    return render(request,'index.html',{
        'course_list':course_list,
        'org_list':org_list
    })
def register(request):
    if request.method == 'GET':
        user_register_form = UserRegisterForm()
        return render(request,'users/register.html',{
            'user_register_form':user_register_form
        })
    else:
        user_register_form = UserRegisterForm(request.POST)
        #验证通过
        if user_register_form.is_valid():
            email = user_register_form.cleaned_data['email']
            password = user_register_form.cleaned_data['password']

            #检查数据库里是否存在
            user_list = UserProfile.objects.filter(Q(username = email)|Q(email=email))
            if user_list:
                return render(request,'users/register.html',{
                    'msg':'用户已存在'
                })
            else:
                a = UserProfile()
                a.username = email
                a.set_password(password)
                a.email = email
                a.save()
                #发送邮箱验证码
                send_email_code(email,1)
                return HttpResponse('请尽快前往您的邮箱激活账户，否则无法登陆')
        else:
            return render(request,'users/register.html',{
                'user_register_form':user_register_form
            })
class LoginView(View):
    def get(self,request):
        return render(request, 'users/login.html')
    def post(self,request):
        user_login_form = UserLoginForm(request.POST)
        # 格式校验通过
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            # 数据验证
            user = authenticate(username=email, password=password)
            if user:
                user_list = UserProfile.objects.filter(username=email)
                if user_list[0].is_start:
                    login(request, user)
                    a = UserMessage()
                    a.message_content = '欢迎' + email + '登录'
                    a.message_man = user.id
                    a.save()
                    url = request.COOKIES.get('url', '/users/index')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
                else:
                    return HttpResponse('请尽快前往您的邮箱激活账户，否则无法登陆')
            else:
                return render(request, 'users/login.html', {
                    'msg': '邮箱或密码有误'
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form
            })
'''  
def user_login(request):
    if request.method == 'GET':
        return render(request,'users/login.html')
    else:
        user_login_form = UserLoginForm(request.POST)
        # 格式校验通过
        if user_login_form.is_valid():
            email = user_login_form.cleaned_data['email']
            password = user_login_form.cleaned_data['password']
            #数据验证
            user = authenticate(username = email,password = password)
            if user:
                user_list = UserProfile.objects.filter(username=email)
                if user_list[0].is_start:
                    login(request,user)
                    a = UserMessage()
                    a.message_content = '欢迎'+ email +'登录'
                    a.message_man = user.id
                    a.save()
                    url = request.COOKIES.get('url','/')
                    ret = redirect(url)
                    ret.delete_cookie('url')
                    return ret
                else:
                    return HttpResponse('请尽快前往您的邮箱激活账户，否则无法登陆')
            else:
                return render(request,'users/login.html',{
                    'msg':'邮箱或密码有误'
                })
        else:
            return render(request, 'users/login.html', {
                'user_login_form': user_login_form
            })
'''
def user_logout(request):
    logout(request)
    return redirect(reverse('users:index'))

def user_active(request,code):
    email_list = EmailVerifyCode.objects.filter(code=code)
    if email_list:
        email_ver = email_list[0].email
        user_list = UserProfile.objects.filter(username=email_ver)
        if user_list:
            user_list[0].is_start = True
            user_list[0].save()
            return redirect(reverse('users:user_login'))
        else:
            pass
    else:
        pass

def user_forget(request):
    if request.method == 'GET':
        user_forget_form = UserForgetForm()
        return render(request,'users/forgetpwd.html',{
            'user_forget_form':user_forget_form
        })
    else:
        user_forget_form = UserForgetForm(request.POST)
        if user_forget_form.is_valid():
            email = user_forget_form.cleaned_data['email']
            user_list = UserProfile.objects.filter(email=email)
            if user_list:
                send_email_code(email,2)
                return HttpResponse('请尽快到邮箱重置密码')
            else:
                return render(request, 'users/forgetpwd.html', {
                    'msg':'该用户不存在'
                })
        else:
            return render(request, 'users/forgetpwd.html', {
                'user_forget_form':user_forget_form
            })
def user_reset(request,code):
    if code:
        if request.method == 'GET':
            return render(request, 'users/password_reset.html', {
                'code':code
            })
        else:
            user_reset_form = UserResetForm(request.POST)
            if user_reset_form.is_valid():
                password = user_reset_form.cleaned_data['password']
                password1 = user_reset_form.cleaned_data['password1']
                if password == password1:
                    email_list = EmailVerifyCode.objects.filter(code=code)
                    if email_list:
                        email_ver = email_list[0].email
                        user_list = UserProfile.objects.filter(username=email_ver)
                        if user_list:
                            user_list[0].set_password(password)
                            user_list[0].save()
                            return redirect(reverse('users:user_login'))
                        else:
                            pass
                    else:
                        pass
                else:
                    return render(request, 'users/password_reset.html', {
                        'msg':'两次密码输入不一致',
                        'code':code
                    })
            else:
                return render(request, 'users/password_reset.html', {
                    'user_reset_form':user_reset_form,
                    'code':code
                })

#用户中心
def user_info(request):
    return render(request,'users/usercenter-info.html')
def user_message(request):
    message_list = UserMessage.objects.filter(message_man=int(request.user.id))
    if message_list:
        return render(request,'users/usercenter-message.html',{
            'message_list':message_list
        })
#消息已阅读
def user_message_hasRead(request):
    id = request.GET.get('id','')
    message = UserMessage.objects.filter(id=id,message_status=False)
    if message:
        message[0].message_status=True
        message[0].save()
        return JsonResponse({'status':'ok'})
    else:
        pass
def user_course(request):
    usercourse_list = request.user.usercourse_set.all()
    course_list = [usercourse.study_course for usercourse in usercourse_list]
    return render(request,'users/usercenter-mycourse.html',{
        'course_list':course_list
    })
def user_fav_course(request):
    userlove_course_list = request.user.userlove_set.all().filter(love_type=2,love_status=True)
    userlove_course_id =[course.love_id for course in userlove_course_list]
    course_list = CourseInfo.objects.filter(id__in=userlove_course_id)
    return render(request,'users/usercenter-fav-course.html',{
        'course_list': course_list
    })
def user_fav_teacher(request):
    userlove_teacher_list = request.user.userlove_set.all().filter(love_type=3,love_status=True)
    userlove_teacher_id = [teacher.love_id for teacher in userlove_teacher_list]
    teacher_list = TeacherInfo.objects.filter(id__in=userlove_teacher_id)
    return render(request,'users/usercenter-fav-teacher.html',{
        'teacher_list':teacher_list
    })
def user_fav_org(request):
    userlove_org_list = request.user.userlove_set.all().filter(love_type=1,love_status=True)
    userlove_org_id = [org.love_id for org in userlove_org_list]
    org_list = OrgInfo.objects.filter(id__in=userlove_org_id)
    return render(request,'users/usercenter-fav-org.html',{
        'org_list':org_list
    })
#删除用户收藏
def user_fav_del(request):
    love_id = request.GET.get('love_id','')
    love_type = request.GET.get('love_type','')
    love_man = request.user
    love = UserLove.objects.filter(love_id=int(love_id),love_type=int(love_type),love_man=love_man,love_status=True)
    if love:
        love[0].love_status = False
        love[0].save()
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status': 'fail','msg':'取消失败'})

#修改头像
def user_change_image(request):
    #request.FILES为上传的文件
    #instance为需要改变的实例
    user_change_image_form = UserChangeImageForm(request.POST,request.FILES,instance=request.user)
    if user_change_image_form.is_valid():
        user_change_image_form.save(commit=True)
        return JsonResponse({'status':'ok'})
    else:
        return JsonResponse({'status': 'err'})
#修改用户信息
def user_change_info(request):
    user_change_info_form = UserChangeInfoForm(request.POST,instance=request.user)
    if user_change_info_form.is_valid():
        user_change_info_form.save(commit=True)
        return JsonResponse({'status': 'ok'})
    else:
        return JsonResponse({'status': 'err'})
#修改邮箱
def user_change_email(request):
    user_change_email_form = UserChangeEmailForm(request.POST)
    #校验邮箱是否正确
    if user_change_email_form.is_valid():
        email = user_change_email_form.cleaned_data['email']
        #邮箱在数据库中是否已经存在
        email_list = UserProfile.objects.filter(Q(email=email)|Q(username=email))
        if email_list:
            return JsonResponse({'status': 'err', 'msg': '该邮箱已存在'})
        else:
            email_code_list = EmailVerifyCode.objects.filter(email=email,send_type=3)
            if email_code_list:
                email_verify = email_code_list.order_by('-add_time')[0]
                if (datetime.now() - email_verify.add_time).seconds > 60:
                    email_verify.delete()
                    send_email_code(email, 3)
                    return JsonResponse({'status': 'ok', 'msg': '验证码发送成功，请前往邮箱查看'})
                else:
                    return JsonResponse({'status': 'ok', 'msg': '验证码已发送，1分钟之后再试'})
            else:
                send_email_code(email,3)
                return JsonResponse({'status': 'ok','msg':'验证码发送成功，请前往邮箱查看'})
    else:
        return JsonResponse({'status':'err','msg':'邮箱输入有误'})

#重置用户邮箱
def user_reset_email(request):
    user_reset_email_form = UserResetEmailForm(request.POST)
    if user_reset_email_form.is_valid():
        #判断邮箱验证码是否存在
        email = user_reset_email_form.cleaned_data['email']
        code = user_reset_email_form.cleaned_data['code']
        user_reset_email_list = EmailVerifyCode.objects.filter(email=email,code=code)
        if user_reset_email_list:
            email_verify = user_reset_email_list.order_by("-add_time")[0]
            #验证码过期校验
            if (datetime.now() - email_verify.add_time).seconds < 300:
                request.user.email = email
                request.user.username = email
                request.user.save()
                return JsonResponse({
                    'status':'ok'
                })
            else:
                return JsonResponse({
                    'status': 'err',
                    'msg':'验证码过期，请重新获取'
                })
        else:
            return JsonResponse({
                'status': 'err',
                'msg': '邮箱或验证码输入错误'
            })
    else:
        return JsonResponse({
            'status': 'err',
            'msg': '邮箱或验证码输入错误'
        })
def page_not_found(request, exception):
    return render(request,'handler_404.html')
def page_error(request):
    return render(request,'handler_500.html')