import xadmin
from .models import CourseInfo,LessonInfo,VideoInfo,SourceInfo
# Create your models here.
class CourseInfoXadmin(object):
    list_display = ['image','name','study_time','study_num','level','love_num','click_num','desc','detail','category','course_notice','course_need','teacher_tell','add_time']
    model_icon = 'fa fa-tasks'

class LessonInfoXadmin(object):
    list_display = ['name', 'courseinfo', 'add_time']
    model_icon = 'fa fa-ticket'

class VideoInfoXadmin(object):
    list_display = ['name', 'study_time', 'url','lessoninfo','add_time']
    model_icon = 'fa fa-video-camera'

class SourceInfoXadmin(object):
    list_display = ['name', 'down_load', 'courseinfo', 'add_time']
    model_icon = 'fa fa-folder-open-o'

xadmin.site.register(CourseInfo,CourseInfoXadmin)
xadmin.site.register(LessonInfo,LessonInfoXadmin)
xadmin.site.register(VideoInfo,VideoInfoXadmin)
xadmin.site.register(SourceInfo,SourceInfoXadmin)