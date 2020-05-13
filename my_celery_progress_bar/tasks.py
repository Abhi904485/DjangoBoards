from celery import shared_task, current_task

from accounts.models import User
import string
from django.utils.crypto import get_random_string


@shared_task
def create_random_users(total):
    User.objects.all().delete()
    for i in range(total):
        username = "{}".format(get_random_string(10, string.ascii_letters))
        email = "{}@gmail.com".format(username)
        password = get_random_string(50, string.ascii_letters)
        percent = int(100 * float(i) / float(total))
        current_task.update_state(state='PROGRESS',
                                  meta={'current': i, 'total': total, 'percent': percent})
        User.objects.create_user(email=email, username=username, password=password)
    return "{} random user created with success".format(total)
