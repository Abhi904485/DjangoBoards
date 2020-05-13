from django.shortcuts import render
from django.views.generic import ListView

from accounts.models import User
from .tasks import create_random_users


class UserListView(ListView):
    model = User
    template_name = 'users_list.html'


def create_user_view(request):
    if request.method == "POST":
        total = request.POST['total']
        result = create_random_users.delay(int(total))
        return render(request, 'display_progress.html', context={'task_id': result.task_id})
    else:
        return render(request, 'generate_view.html')
