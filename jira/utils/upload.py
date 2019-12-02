import os
import shutil
from django.conf import settings

def task_document_path(instance, filename):
    task_id = instance.task.id
    project_id = instance.task.block.project.id
    return f'projects/project_{project_id}/task_{task_id}/{filename}'


def task_delete_path(instance):
    path = os.path.abspath(os.path.join(settings.MEDIA_ROOT,
                                        f'projects/project_{instance.block.project_id}/task_{instance.id}'))
    shutil.rmtree(path)