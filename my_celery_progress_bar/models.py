# from django.db import models
# from accounts.models import User
#
#
# # Create your models here.
#
# class JobModel(models.Model):
#     user = models.ForeignKey(User, models.CASCADE)
#     task_id = models.CharField(max_length=40, unique=True)
#     submission_time = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.task_id
