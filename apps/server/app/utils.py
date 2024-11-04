from rest_framework.response import Response


def json_response(message=None, data=None, status_code=200):
    return Response({"message": message, "data": data}, status=status_code)
