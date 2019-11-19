from django.contrib import admin
from learning_logs.models import Topic, Entry

admin.site.register(Topic)  # 通过管理网站管理模型
admin.site.register(Entry)  # 注册模型Entry
