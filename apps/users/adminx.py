import xadmin
from .models import BannerInfo,EmailVerifyCode
from xadmin import views

class BaseXadminSetting(object):
    enable_themes = True
    use_bootswatch = True

class CommXadminSetting(object):
    site_title = '星海教育后台管理系统'
    site_footer = '星海公司'
    menu_style = 'accordion'


class BannerInfoXadmin(object):
    list_display = ['image','url','add_time']
    model_icon = 'fa fa-picture-o'

class EmailVerifyCodeXadmin(object):
    list_display = ['code', 'email', 'send_type','add_time']
    model_icon = 'fa fa-envelope'

xadmin.site.register(BannerInfo,BannerInfoXadmin)
xadmin.site.register(EmailVerifyCode,EmailVerifyCodeXadmin)
#注册xadmin的主题
xadmin.site.register(views.BaseAdminView,BaseXadminSetting)
#注册xadmin的标题和底部公司名称
xadmin.site.register(views.CommAdminView,CommXadminSetting)
