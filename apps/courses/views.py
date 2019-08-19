from django.shortcuts import render,HttpResponse, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import CourseInfo, VideoInfo, LessonInfo
from apps.operations.models import UserLove, UserCourse, UserComment
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from tools.decorator import decorator_login
def course_list(request):
    course_all = CourseInfo.objects.all()
    recommend_course = course_all.order_by('-love_num')[:3]
    #最热门和参与人数排序
    sort = request.GET.get('sort','')
    if sort:
        course_all = course_all.order_by('-'+sort)
    #全局搜索
    keyword = request.GET.get('keyword','')
    if keyword:
        course_all = course_all.filter(Q(name__icontains=keyword)|Q(desc__icontains=keyword)|Q(detail__icontains=keyword))
    # 实现分页功能
    #获取当前页面的num值
    pagenum = request.GET.get('pagenum','')
    print(pagenum)
    #每页展示的条数
    pa = Paginator(course_all,3)
    # #获取对应页面的数据
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request,'courses/course-list.html',{
        'course_all':course_all,
        'recommend_course':recommend_course,
        'pages':pages,
        'sort':sort,
        'keyword':keyword
    })

def course_detail(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=int(course_id))[0]
        relate_course = CourseInfo.objects.filter(category=course.category).exclude(id=int(course_id))
        course.click_num += 1
        course.save()
        #用户收藏情况
        love_status = False
        love_org_status = False
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=course_id,love_status=1,love_man=request.user)
            if love:
                love_status = True
            love1 = UserLove.objects.filter(love_id=course.orginfo.id,love_status=1,love_man=request.user)
            if love1:
                love_org_status = True
        return render(request,'courses/course-detail.html',{
            'course':course,
            'relate_course':relate_course,
            'love_status':love_status,
            'love_org_status':love_org_status
        })
#@login_required(login_url="/users/user_login")
@decorator_login
def course_video(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=course_id)[0]
        # 判断用户之前是否已经学习过了这门课程，没有学过则添加记录，学过则不做处理
        userCourseList = UserCourse.objects.filter(study_man=request.user,study_course=course)
        if not userCourseList:
            a = UserCourse()
            a.study_man = request.user
            a.study_course = course
            a.save()
            #课程的学习人数加1
            course.study_num += 1
            course.save()
            #机构的学习人数加1
            #获取当前客户学习过的所有课程
            userCourseList = UserCourse.objects.filter(study_man=request.user)
            course_list =[userCourse.study_course for userCourse in userCourseList]
            #根据拿到的课程，找到每一个课程对应的机构
            org_list = list(set([orgs.orginfo for orgs in course_list]))
            if course.orginfo in org_list:
                course.orginfo.study_num += 1
                course.orginfo.save()

        #学过该课的同学还学过
        #1 获取学习过当前课程的列表信息
        userCourseList = UserCourse.objects.filter(study_course=course)
        #2 获取学习过当前课程的用户列表
        userList = [userCourse.study_man for userCourse in userCourseList]
        #3 获取这些用户学习得课程列表信息，并过滤掉当前课程
        userCourseList = UserCourse.objects.filter(study_man__in=userList).exclude(study_course = course)
        #4 获取到这些用户学习得课程
        courseList = list(set([userCourse.study_course for userCourse in userCourseList]))
        return render(request,'courses/course-video.html',{
            'course':course,
            "courseList":courseList
        })

def course_comment(request,course_id):
    if course_id:
        course = CourseInfo.objects.filter(id=course_id)[0]
        commentList = UserComment.objects.filter(comment_course_id=course_id)
        return render(request,'courses/course-comment.html',{
            'course':course,
            'commentList':commentList
        })

