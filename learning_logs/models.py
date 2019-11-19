from django.db import models
from django.contrib.auth.models import User


class Topic(models.Model):  # Model是Django中一个定义了模型基本功能的类
    """用户学习的主题"""
    # CharField是由字符或文本组成的数据
    # 定义CharField属性时，必须告诉Django该在数据库中预留多少空间。
    # 在这里，我们将max_length设置成了200（即200个字符）
    text = models.CharField(max_length=200)
    # DateTimeField记录时间和日期的数据
    # 实参auto_now_add=True让每当用户创建新主题时,让Django将这个属性自动设为当前时间和日期
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)  # 建立到模型User的外键关系

    def __str__(self):  # 返回存储在属性text中的字符串
        """返回模型的字符串表示"""
        return self.text

    class Meta:
        verbose_name_plural = '主题'


class Entry(models.Model):
    """学到的有关某个主题的具体知识"""
    # 一个ForeignKey实例，它引用数据库中的另一条记录，将每个条目关联到特定的主题
    # 对于多对一的关系定义，我们需要传递两个位参，一个是要参照的模型，一个是on_delete选项
    # 以自己来创建多对一关系，使用models.ForeignKey('self', on_delete=models.CASCADE)
    #
    # on_delete=models.CASCADE:
    # 当被参照对象被删除的时候，对应的删除与他有参照关系的对象（例如当你删除一篇博客的时候，所有的评论也会被删除），
    # 这个定义与SQL中的CASCADE相等（ON DELETE CASCADE）
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    # 一个不限制长度的TextField实例
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    # 嵌套的Meta类，存储用于管理模型的额外信息
    # 在这里我们能够设置一个特殊属性，让Django在需要时使用Entries来表示多个条目。
    # 如果没有这个类，Django将使用Entrys来表示多个条目
    class Meta:
        verbose_name_plural = '条目'

    def __str__(self):
        """返回模型的字符串表示"""
        # 只显示text的前50个字符，并用...指出显示内容并非整个条目
        return self.text[:50] + '...'


