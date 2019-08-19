from apps.users.models import EmailVerifyCode
from random import randrange,choice
from django.core.mail import send_mail
from eduproject.settings import EMAIL_HOST_USER
#获取随机验证码
def get_random_code(code_length):
    #code源
    code_source = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKKLZXCVBNM'
    code = ''
    for i in range(code_length):
        #两种获得随机数的方法
        #rand_code = choice(code_source)
        rand_code = code_source[randrange(0,len(code_source)-1)]
        code += rand_code
    return code
#验证码存库及发送邮件
def send_email_code(email,send_type):
    #第一步：创建邮箱验证码对象，保存验证码，用于做后续的校验
    code = get_random_code(8)
    a = EmailVerifyCode()
    a.email = email
    a.send_type = send_type
    a.code = code
    a.save()
    #第二步：向指定邮箱发送邮件
    send_title = ''
    send_content = ''
    if send_type == 1:
        send_title = '欢迎注册星海教育网站'
        send_content = '请点击下面的链接激活您的账号。\n http://127.0.0.1:8000/users/user_active/'+code
    if send_type == 2:
        send_title = '星海教育重置密码'
        send_content = '请点击下面的链接重置您的密码。\n http://127.0.0.1:8000/users/user_reset/'+code
    if send_type == 3:
        send_title = '星海教育修改邮箱'
        send_content = '下面为您的修改邮箱验证码'+code
    send_mail(send_title,send_content,EMAIL_HOST_USER,[email])