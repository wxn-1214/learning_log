from django import forms
from .models import Topic, Entry


# 最简单的ModelForm只包含了一个内嵌的Meta类
# 它告诉django根据哪个模型创建表单，以及在表单中包含哪些字段
class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['text']  # 该表单只包含字段text
        labels = {'text': ''}  # 不要为字段text生成标签


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        # 小部件(widget)是一个HTML表单元素，如单/多行文本框或下拉列表
        # 通过设置属性widgets来覆盖Django选择的默认小部件
        # 通过forms.Textarea定制了字段'text'的输入小部件，将文本区域的宽度设置未80列(默认40列)
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}
