"""定义learning_logs的URL模式"""
# Django2版本用path取代了之前的url,此外path不支持正则表达式，需要引用re_path
from django.urls import path, re_path
# from django.conf.urls import url  # Django1版本
from . import views
app_name = 'learning_logs'

urlpatterns = [
    # 主页,views.index调用了要使用的视图，name指定这个URL模式的名称
    path('', views.index, name='index'),
    re_path(r'^topics/$', views.topics, name='topics'),
    # 特定主页的详细页面
    #
    # 正则表达式：r'^topics/(?P<topic_id>\d+)/$'
    # r让Django将这个字符串视为原始字符串，并指出正则表达式包含在引号内
    # /(?P<topic_id>\d+)/与包含在两个斜杠内的整数匹配，并将其存储在topic_id实参中
    # 表达式两边的括号捕获URL中的值，?P<topic_id>将匹配的值存储到topic_id中
    # 表达式\d+与包含在两个斜杠内的任何数字都匹配
    #
    # 当URL与这个模式匹配时，Django调用视图函数topic，并将topic_id中的值作为实参传递给他
    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),

    # 添加新主题的网页
    re_path(r'^new_topic/$', views.new_topic, name='new_topic'),
    # 删除主题
    re_path(r'^delete_topic/(?P<topic_id>\d+)/$', views.delete_topic,
            name='delete_topic'),
    # 添加新条目的页面
    re_path(r'^new_entry/(?P<topic_id>\d+)/$', views.new_entry,
            name='new_entry'),
    # 编辑条目的页面
    re_path(r'^edit_entry(?P<entry_id>\d+)/$', views.edit_entry,
            name='edit_entry'),
    # 删除条目
    re_path(r'^delete_entry(?P<entry_id>\d+)/$', views.delete_entry,
            name='delete_entry'),
    # 正则表达式被称为regex
    # 正则表达式r'^$'：
    # r让python将接下来的字符串视为原始字符串，引号告诉python正则表达式始于和终于何处
    # 脱字符(^)让python查看字符串的开头，$让python查看字符串末尾
    # 总之，这个正则表达式让python查找开头和末尾没有任何东西的URL。
    # 其他URL都与这个正则表达式不匹配，若请求的URL与任何URL都不匹配，Django将返回一个错误页面

    # url(r'^$', views.index, name='index'),
]
