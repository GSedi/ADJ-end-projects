from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from main.models import TaskComment, Task
from main.serializers import TaskCommentSerializer


@api_view(['GET', 'POST'])
def task_comment_lists(request, task_id):
    try:
        task = Task.objects.get(id=task_id)
    except Task.DoesNotExist as e:
        return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        task_comments = TaskComment.objects.filter(task=task_id)
        serializer = TaskCommentSerializer(task_comments, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = TaskCommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator_id=request.user.id, task_id=task_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET', 'PUT', 'DELETE'])
def task_comment_detail(request, pk):
    try:
        task_comment = TaskComment.objects.get(id=pk)
    except TaskComment.DoesNotExist as e:
        return Response({'error': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskCommentSerializer(task_comment)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = TaskCommentSerializer(instance=task_comment, data=request.data)
        if serializer.is_valid():
            serializer.save(creator_id=task_comment.creator_id, task_id=task_comment.task_id)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    elif request.method == 'DELETE':
        task_comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
