from django.shortcuts import render,HttpResponse,redirect
from .models import OrgInfo,CityInfo,TeacherInfo
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from apps.operations.models import UserLove
from django.db.models import Q
#机构列表
def org_list(request):
    all_orgs = OrgInfo.objects.all()
    all_city = CityInfo.objects.all()
    orgs_sort = all_orgs.order_by('-love_num')
    #点击机构类别进行筛选
    cate = request.GET.get('cate', '')
    if cate:
        all_orgs = all_orgs.filter(category=cate)
    #关键字全局搜索
    keyword = request.GET.get('keyword','')
    if keyword:
        all_orgs = all_orgs.filter(Q(name__icontains=keyword)|Q(detail__icontains=keyword)|Q(desc__icontains=keyword))
    #点击城市进行筛选
    cityid = request.GET.get('cityid','')
    if cityid:
        all_orgs = all_orgs.filter(cityinfo_id=int(cityid))
    #按照学习人数和课程数进行排序
    sort = request.GET.get('sort','')
    if sort:
        all_orgs = all_orgs.order_by('-'+sort)
    #实现分页功能
    pagenum = request.GET.get('pagenum','')
    pa = Paginator(all_orgs,3)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)

    return render(request,'orgs/org-list.html',{
        'all_orgs':all_orgs,
        'pages':pages,
        'all_city':all_city,
        'orgs_sort':orgs_sort,
        'cate':cate,
        'cityid':cityid,
        'sort':sort,
        'keyword':keyword,
    })
#机构详情
def org_detail(request,org_id):
    #收藏状态展示判断
    love_status = False
    # 先判断用户登录
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_id=org_id,love_man=request.user,love_status=1)
        if love:
            love_status = True
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]
        return render(request,'orgs/org-detail-homepage.html',{
            'org':org,
            'love_status':love_status
        })

def org_detail_course(request,org_id):
    # 收藏状态展示判断
    love_status = False
    # 先判断用户登录
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_id=org_id, love_man=request.user, love_status=1)
        if love:
            love_status = True
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]
        all_course = org.courseinfo_set.all()
        org.click_num += 1
        org.save()
        # 实现分页功能
        pagenum = request.GET.get('pagenum', '')
        pa = Paginator(all_course, 1)
        try:
            pages = pa.page(pagenum)
        except PageNotAnInteger:
            pages = pa.page(1)
        except EmptyPage:
            pages = pa.page(pa.num_pages)
        return render(request,'orgs/org-detail-course.html',{
            'org':org,
            'pages':pages,
            'act': 'kc',
            'love_status': love_status
        })

def org_detail_desc(request,org_id):
    # 收藏状态展示判断
    love_status = False
    # 先判断用户登录
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_id=org_id, love_man=request.user, love_status=1)
        if love:
            love_status = True
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]
        return render(request,'orgs/org-detail-desc.html',{
            'org':org,
            'act': 'js',
            'love_status': love_status
        })

def org_detail_teacher(request,org_id):
    # 收藏状态展示判断
    love_status = False
    # 先判断用户登录
    if request.user.is_authenticated:
        love = UserLove.objects.filter(love_id=org_id, love_man=request.user, love_status=1)
        if love:
            love_status = True
    if org_id:
        org = OrgInfo.objects.filter(id = int(org_id))[0]
        return render(request,'orgs/org-detail-teachers.html',{
            'org':org,
            'act': 'th',
            'love_status': love_status
        })

#讲师列表
def teacher_list(request):
    teachers = TeacherInfo.objects.all()
    teachers_sort = teachers.order_by('-love_num')
    clickNum = request.GET.get('clickNum','')
    if clickNum:
        teachers = teachers.order_by('-'+clickNum)
    #全局搜索
    keyword = request.GET.get('keyword','')
    if keyword:
        teachers = teachers.filter(Q(name__icontains=keyword))
    # 实现分页功能
    pagenum = request.GET.get('pagenum', '')
    pa = Paginator(teachers, 2)
    try:
        pages = pa.page(pagenum)
    except PageNotAnInteger:
        pages = pa.page(1)
    except EmptyPage:
        pages = pa.page(pa.num_pages)
    return render(request,'teachers/teachers-list.html',{
        'teachers':teachers,
        'pages':pages,
        'renqi':clickNum,
        'teachers_sort':teachers_sort,
        'keyword':keyword,
    })

#讲师详情
def teacher_detail(request,teacher_id):
    if teacher_id:
        teacher = TeacherInfo.objects.filter(id=teacher_id)[0]
        teachers_sort = TeacherInfo.objects.order_by('-love_num')
        teacher.click_num += 1
        teacher.save()
        if request.user.is_authenticated:
            love = UserLove.objects.filter(love_id=int(teacher_id),love_man=request.user,love_type=3,love_status=1)
            love_status1 = False
            if love:
                love_status1 = True
            love = UserLove.objects.filter(love_id=teacher.work_company_id,love_man=request.user, love_type=1, love_status=1)
            love_status2 = False
            if love:
                love_status2 = True
            return render(request,'teachers/teacher-detail.html',{
                'teacher':teacher,
                'teachers_sort':teachers_sort,
                'love_status1':love_status1,
                'love_status2': love_status2
            })