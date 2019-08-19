import xadmin
from .models import CityInfo,OrgInfo,TeacherInfo
class CityInfoXadmin(object):
    list_display = ['name','add_time']
    model_icon = 'fa fa-thumb-tack'

class OrgInfoXadmin(object):
    list_display = ['image', 'name','course_num','study_num','address','desc','detail','love_num','click_num','category','cityinfo','add_time']
    search_fields = ['name']
    list_filter = ['name']
    model_icon = 'fa fa-university'
    style_fields = {'detail':'ueditor'}

class TeacherInfoXadmin(object):
    list_display = ['image','name','work_year','work_position','work_style','work_company','age','gender','love_num','click_num','add_time']
    model_icon = 'fa fa-user-circle-o'

xadmin.site.register(CityInfo,CityInfoXadmin)
xadmin.site.register(OrgInfo,OrgInfoXadmin)
xadmin.site.register(TeacherInfo,TeacherInfoXadmin)