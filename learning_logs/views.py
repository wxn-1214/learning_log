from django.shortcuts import render, get_object_or_404, redirect
from .models import Topic, Entry
from .forms import TopicForm, EntryForm
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie


def index(request):
    """学习笔记的主页"""
    return render(request, 'learning_logs/index.html')


# 装饰器(decorator)是放在函数定义前面的指令，在函数运行前根据它来修改函数代码行为
@login_required  # 装饰器@login_required检查用户是否登录，仅当用户登录时才运行topic()
def topics(request):
    """显示所有的主题"""
    # 查询数据库请求提供Topic对象，并按属性data_added对它们进行排序
    # 用户登录后，request对象将有一个user属性
    # filter(owner=request.user)让Django只从数据库中获取owner属性为当前用户的Topic对象
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    # 定义一个将要发送给模板的上下文(字典)，键是在模板中访问数据的名称，值是要发送给模板的数据
    context = {'topics': topics}
    # 将变量context传递给render()
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """显示单个主题及其所有条目"""
    # 向数据库查询特定的信息
    topic = get_object_or_404(Topic, id=topic_id)
    # 确认请求的主题属于当前用户,当请求的主题不属于该用户时返回404错误页面
    if topic.owner != request.user:
        raise Http404
    entries = topic.entry_set.order_by('-date_added')  # -指定按降序排序

    context = {'topic': topic, 'entries': entries}
    return render(request, 'learning_logs/topic.html', context)


@login_required
# @method_decorator(ensure_csrf_cookie)
def delete_topic(request, topic_id):
    """删除主题"""
    # if request.method == 'POST':
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404
    topic.delete()
    return redirect('learning_logs:topics')
    # else:
    # return HttpResponse('仅允许POST请求')


@login_required
# @method_decorator(ensure_csrf_cookie)
def delete_entry(request, entry_id):
    """删除条目"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404
    entry.delete()
    return redirect(reverse('learning_logs:topic', args=[topic.id]))


@login_required
def new_topic(request):
    """添加新主题"""
    if request.method != 'POST':  # 判断请求方法是GET还是POST
        # 未提交数据:创建一个新表单
        form = TopicForm()
    else:
        # POST提交的数据，对数据进行处理
        form = TopicForm(request.POST)  # 用户输入的数据保存在request.POST中
        # is_valid()核实用户填写了所有必不可少的字段(表单默认字段)
        # 且输入的数据与要求的字段类型一致(如字段text少于200个字符，这在models.py中已指定)
        if form.is_valid():
            new_topic = form.save(commit=False)  # 先修改主题，后保存到数据库中
            new_topic.owner = request.user
            new_topic.save()
            # form.save()  # 将表单中的数据写入数据库
            # 重定向到网页topics，使用reverse()获取页面topics的URL
            return HttpResponseRedirect(reverse('learning_logs:topics'))

    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """在特定的主题添加新条目"""
    topic = get_object_or_404(Topic, id=topic_id)
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = EntryForm()
    else:
        form = EntryForm(request.POST)
        if form.is_valid():
            # 传递实参commit=False，让Django创建一个新的条目对象，并将其存储到new_entry中，但不保存到数据库
            new_entry = form.save(commit=False)
            # 将条目保存到数据库，并将其与正确的主题相关联
            new_entry.topic = topic
            new_entry.save()
            # 调用reverse提供两个实参:根据它来生成URL的URL模式的名称，args包含在URL中的所有实参
            return HttpResponseRedirect(reverse('learning_logs:topic',
                                                args=[topic_id]))

    context = {'topic': topic, 'form': form}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """编辑已有条目"""
    entry = get_object_or_404(Entry, id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # 初次请求，使用当前条目填充表单
        form = EntryForm(instance=entry)
    else:
        # POST提交的数据，对数据进行处理
        # 根据现有条目对象创建一个表单实例，并根据request.POST中的相关数据对其进行修改
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('learning_logs:topic'),
                                        args=[topic.id])

    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
