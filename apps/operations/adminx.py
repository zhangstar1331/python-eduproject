import xadmin
from .models import UserAsk,UserLove,UserCourse,UserComment,UserMessage
# Create your models here.
class UserAskXadmin(object):
    list_display = ['name','phone','course','add_time']
    model_icon = 'fa fa-server'

class UserLoveXadmin(object):
    list_display = ['love_man','love_id','love_type','love_status','add_time']
    model_icon = 'fa fa-star'

class UserCourseXadmin(object):
    list_display = ['study_man','study_course','add_time']
    model_icon = 'fa fa-map'

class UserCommentXadmin(object):
    list_display = ['comment_man','comment_course','comment_content','add_time']
    model_icon = 'fa fa-pencil-square-o'

class UserMessageXadmin(object):
    list_display = ['message_man','message_content','message_status','add_time']
    model_icon = 'fa fa-envelope-o'

xadmin.site.register(UserAsk,UserAskXadmin)
xadmin.site.register(UserLove,UserLoveXadmin)
xadmin.site.register(UserCourse,UserCourseXadmin)
xadmin.site.register(UserComment,UserCommentXadmin)
xadmin.site.register(UserMessage,UserMessageXadmin)