from django.contrib.auth import logout, login, authenticate
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .serializers import UserSerializer, SessionSerializer


class SessionView(viewsets.ViewSet):
    '''
    rest view set for Session
    '''
    class SessionPermission(permissions.BasePermission):
        ''' custom class to check permissions for sessions '''

        def has_permission(self, request, view):
            ''' check request permissions '''

            if request.method == 'POST':
                return True
            return request.user.is_authenticated()

    permission_classes = (SessionPermission,)
    serializer_class = SessionSerializer

    def get(self, request, format=None):
        ''' api to get current session '''

        return Response(UserSerializer(request.user).data)

    def post(self, request):
        ''' api to login '''

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.data)
        if not user:
            return Response({'reason': 'Username or password is incorrect'},
                            status=400)
        if not user.is_active:
            return Response({'reason': 'User is inactive'}, status=403)

        login(request, user)
        return Response(UserSerializer(user).data)

    def delete(self, request):
        ''' api to logout '''

        user_id = request.user.id
        logout(request)
        return Response({'id': user_id})

    create = post  # this is a trick to show this view in api-root
