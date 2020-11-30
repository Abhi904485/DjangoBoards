from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.utils import timezone

from accounts.models import User
from .forms import NewTopicForm, ReplyPostForm, EditPostForm
from .models import Board, Post, Topic
from .utility import get_pagination


def home(request):
    boards = Board.objects.get_board_details()
    page = request.GET.get('page', 1)
    page_items = 3
    page_obj = get_pagination(queryset=boards, page=page, items=page_items)
    return render(request, 'home.html', context={'board': page_obj})


def board_topics(request, pk):
    board = get_object_or_404(Board, pk=pk)
    topics = board.get_topics()
    page = request.GET.get('page', 1)
    page_items = 3
    page_obj = get_pagination(queryset=topics, page=page, items=page_items)
    return render(request, 'topics.html', context={'board': board, 'topics': page_obj})


@login_required(login_url='/user/signin/')
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
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic.pk)
        else:
            topic_form = NewTopicForm(request.POST)
            return render(request, 'new_topic.html', context={'board': board, 'form': topic_form})
    else:
        topic_form = NewTopicForm()
        return render(request, 'new_topic.html', context={'board': board, 'form': topic_form})


def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    session_key = 'viewed_topic_{}'.format(topic_pk)  # <-- here
    if not request.session.get(session_key, False):
        topic.views += 1
        topic.save()
        request.session[session_key] = True
    page = request.GET.get('page', 1)
    posts = topic.get_all_posts()
    page_items = 2
    page_obj = get_pagination(queryset=posts, page=page, items=page_items)
    return render(request, 'topic_posts.html', {'topic': topic, 'post': page_obj})


@login_required(login_url='/user/signin/')
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    if request.method == "POST":
        reply_form = ReplyPostForm(request.POST)
        if reply_form.is_valid():
            post = reply_form.save(commit=False)
            post.topic = topic
            post.created_by = request.user
            post.save()
            topic.last_updated = timezone.now()
            topic.save()
            topic_url = reverse('boards:topic_posts', kwargs={'pk': pk, 'topic_pk': topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=get_pagination(topic.get_all_posts(), 1, 2).paginator.num_pages
            )
            return redirect(topic_post_url)
        else:
            return render(request, 'reply_topic.html', {'form': reply_form, 'topic': topic})

    else:
        reply_form = ReplyPostForm()
        return render(request, 'reply_topic.html', {'form': reply_form, 'topic': topic})


@login_required(login_url='/user/signin/')
def edit_post(request, pk, topic_pk, post_pk):
    topic = get_object_or_404(Topic, board__pk=pk, pk=topic_pk)
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        edit_post_form = EditPostForm(request.POST, instance=post)
        if edit_post_form.is_valid():
            post = edit_post_form.save(commit=False)
            post.updated_by = request.user
            post.updated_at = timezone.now()
            post.save()
            return redirect('boards:topic_posts', pk=pk, topic_pk=topic_pk)
        else:
            return render(request, 'edit_post.html', {'form': edit_post_form, 'topic': topic, 'post': post})

    else:
        edit_post_form = EditPostForm(initial={'message': post.message})
        return render(request, 'edit_post.html', {'form': edit_post_form, 'topic': topic, 'post': post})
