from django.conf import settings
from django.db import models


class Status(models.TextChoices):
    TO_DO = 'To Do', 'to do'
    IN_PROGRESS = 'In Progress', 'in progress'
    TEST = 'Test', 'test'
    REJECTED = 'Rejected', 'rejected'
    DONE = 'Done', 'done'
    BACKLOG = 'Backlog', 'backlog'


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='owned_projects',
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='projects',
        blank=True,
    )    # list [user1,user2,

    class Meta:
        db_table = 'project'

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(choices=Status.choices, default=Status.TO_DO, max_length=50)
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='tasks',
        blank=True,
    )
    project = models.ForeignKey('Project', on_delete=models.PROTECT, related_name='tasks')
    deadline=models.DateTimeField(blank=True,null=True)
    created_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'task'

    def __str__(self):
        return self.name
