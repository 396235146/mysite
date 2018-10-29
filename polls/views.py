from django.shortcuts import render
from django.shortcuts import get_object_or_404
# Create your views here.
from django.http import HttpResponse,HttpResponseRedirect
from .models import Question,Choice
from django.urls import reverse

def index(request):#显示最新的一些问卷
    latest_question_list=Question.objects.order_by('-pub_date')[:5]
    context={
        'latest_question_list':latest_question_list,
    }
    return render(request,'polls/index.html',context)

def detail(request, question_id):#显示一个问卷的详细文本内容，没有调查结果但是有一个投票或调查表单。
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})


def results(request, question_id):#显示某个问卷的投票或调查结果。
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):#处理针对某个问卷的某个选项的投票动作。
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # 发生choice未找到异常时，重新返回表单页面，并给出提示信息
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # 成功处理数据后，自动跳转到结果页面，防止用户连续多次提交。
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
