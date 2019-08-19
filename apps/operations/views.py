from django.shortcuts import render,HttpResponse,redirect
from .forms import UserAskForm, UserCommentForm
from django.http import JsonResponse
from .models import UserLove, UserComment
from apps.courses.models import CourseInfo
from apps.orgs.models import OrgInfo,TeacherInfo
#用户咨询
def user_ask(request):
    user_ask_form = UserAskForm(request.POST)
    if user_ask_form.is_valid():
        #form实例可以直接保存提交，不需要单独写，保存form就相当于保存model
        user_ask_form.save(commit=True)
        return JsonResponse({'status':'ok','msg':'请求成功'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '请求失败'})
#用户搜藏
def user_love(request):
    love_id = request.GET.get('love_id','')
    love_type = request.GET.get('love_type','')
    love_man = request.user
    if love_id and love_type:
        obj = None
        if int(love_type) == 1:
            obj = OrgInfo.objects.filter(id=int(love_id))[0]
        if int(love_type) == 2:
            obj = CourseInfo.objects.filter(id=int(love_id))[0]
        if int(love_type) == 3:
            obj = TeacherInfo.objects.filter(id=int(love_id))[0]
        #表里查看是否有当前搜藏的信息
        love = UserLove.objects.filter(love_id=int(love_id),love_type=int(love_type),love_man=love_man)
        if love:
            #根据表里查到的搜藏状态去进行处理
            if love[0].love_status:
                # 取消搜藏
                love[0].love_status = False
                love[0].save()
                obj.love_num -= 1
                obj.save()
                return JsonResponse({'status':'ok','msg':'收藏'})
            else:
                # 搜藏
                love[0].love_status = True
                love[0].save()
                obj.love_num += 1
                obj.save()
                return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
        else:
            a = UserLove()
            a.love_id = int(love_id)
            a.love_type = int(love_type)
            a.love_status = True
            a.love_man = love_man
            a.save()
            obj.love_num += 1
            obj.save()
            return JsonResponse({'status': 'ok', 'msg': '取消收藏'})
    else:
        return JsonResponse({'status': 'fail', 'msg': '请求失败'})

#用户评论
def user_comment(request):
    user_comment_form = UserCommentForm(request.POST)
    if user_comment_form.is_valid():
        a = UserComment()
        a.comment_content = user_comment_form.cleaned_data['comment_content']
        a.comment_course_id = user_comment_form.cleaned_data['comment_course_id']
        a.comment_man_id = request.user.id
        a.save()
        return JsonResponse({'status':'ok','msg':'评论成功'})
    else:
        return JsonResponse({'status': 'ok', 'msg': '评论失败'})