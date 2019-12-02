from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status as status_codes

import logging

from django.shortcuts import get_object_or_404

from main.models import Task, Block, MainUser, \
    MemberProject, Project, TaskDocument, TaskComment
from main.serializers import TaskSerializerCreateUpdate, TaskSerializerGet, \
    MemberProjectSerializer, TaskDocumentSerializer, TaskCommentSerializer

logger = logging.getLogger(__name__)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    permission_classes = (IsAuthenticated, )

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSerializerGet
        else:
            return TaskSerializerCreateUpdate

    def perform_create(self, serializer):
        creator = self.request.user
        executor = get_object_or_404(MainUser, pk=self.request.data['executor_id'])
        block = get_object_or_404(Block, pk=self.request.data['block_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, executor=executor, block=block)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        executor = get_object_or_404(MainUser, pk=self.request.data['executor_id'])
        block = get_object_or_404(Block, pk=self.request.data['block_id'])
        if serializer.is_valid():
            serializer.save(executor=executor, block=block)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)


class MemberProjectViewSet(viewsets.ModelViewSet):
    queryset = MemberProject.objects.all()
    serializer_class = MemberProjectSerializer

    def perform_create(self, serializer):
        member = get_object_or_404(MainUser, pk=self.request.data['member_id'])
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        if serializer.is_valid():
            serializer.save(member=member, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        member = get_object_or_404(MainUser, pk=self.request.data['member_id'])
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        if serializer.is_valid():
            serializer.save(member=member, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

class TaskDocumentViewSet(viewsets.ModelViewSet):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            logger.info(f"{creator} created document for task: \"{task.name}\" with id \'{task.id}\'")
            logger.warning('HAHAHAHAHA')
            logger.error('AAAAAAAAAAAAAAAAAAAAAA')
            logger.critical('NONONONONONONONONONO')
            return Response(serializer.data)
        logger.error('asdcsdcsdc')
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status_codes.HTTP_400_BAD_REQUEST)
