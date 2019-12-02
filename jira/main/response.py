from rest_framework.response import Response
from rest_framework import status as status_codes


def send_response(message='',
                 status=status_codes.HTTP_200_OK,
                 success=True,
                 data=None):
    return Response(
        data={
            'status': status,
            'success': success,
            'message': message,
            'data': data
        }
    )
