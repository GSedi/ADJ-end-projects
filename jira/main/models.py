from django.db import models
from django.db.models import Q, Max, Min, Avg, Sum, Count, F

from utils import constants, upload, validators
from users.models import MainUser


class ProjectManager(models.Manager):
    def filter_by_name(self, name):
        return self.filter(name__contains=name)

    def by_creator(self, creator):
        return self.filter(creator=creator)

    def by_limit_offset(self, limit=1000, offset=0):
        return self.all()[offset:limit]

    def by_created_at(self, year, month, day, hour, minute, second):
        return self.filter(created_at__year=year, created_at__month=month, created_at__day=day)


class Project(models.Model):
    name = models.CharField(max_length=21)
    description = models.TextField(max_length=500)
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_projects')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = ProjectManager()


class MemberProject(models.Model):
    member = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BLockManager(models.Manager):
    def by_type(self, typi):
        return self.filter(type=typi)

    def by_project(self, project):
        return self.filter(project=project)

class Block(models.Model):
    name = models.CharField(max_length=21)
    type = models.CharField(max_length=11, choices=constants.BLOCK_TYPES, default=constants.TODO)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_blocks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BLockManager


class TaskManager(models.Manager):
    def tasks_by_block(self, block):
        return self.filter(block=block)

    def tasks_by_creator_and_block(self, block, user):
        return self.filter(block=block, creator=user)

    def tasks_by_executor_and_block(self, block, user):
        return self.filter(Q(block=block) & Q(executor=user))


class Task(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=500)
    order = models.IntegerField(blank=True, default=None)
    block = models.ForeignKey(Block, on_delete=models.DO_NOTHING, related_name='block_tasks')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_tasks')
    executor = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='executor_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = TaskManager()


class TaskDocument(models.Model):
    document = models.FileField(upload_to=upload.task_document_path,
                                validators=[validators.task_document_size, validators.task_document_extension],
                                null=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_documents')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_documents')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskCommentManager(models.Manager):
    def by_creator(self, creator):
        return self.filter(creator=creator)

    def by_task(self, task):
        return self.filter(task=task)


class TaskComment(models.Model):
    body = models.TextField(max_length=500)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')
    creator = models.ForeignKey(MainUser, on_delete=models.DO_NOTHING, related_name='creator_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
