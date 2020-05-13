from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from .forms import NewTopicForm
from .models import Board, Post


def home(request):
    boards = Board.objects.get_board_details()
    return render(request, 'home.html', context={'boards': boards})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.get_topics()
    return render(request, 'topics.html', context={'board': board, 'topics': topics})


@login_required(login_url='/signin')
def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    starter = User.objects.first()
    if request.method == "POST":
        topic_form = NewTopicForm(request.POST)
        if topic_form.is_valid():
            topic = topic_form.save(commit=False)
            topic.board = board
            topic.starter = starter
            topic.save()
            message = topic_form.cleaned_data['message']
            post = Post.objects.create(message=message, topic=topic, created_by=starter)
            post.save()
            return redirect('board_topics', pk=board.pk)
        else:
            topic_form = NewTopicForm(request.POST)
            return render(request, 'new_topic.html', context={'board': board, 'form': topic_form})
    else:
        topic_form = NewTopicForm()
        return render(request, 'new_topic.html', context={'board': board, 'form': topic_form})
