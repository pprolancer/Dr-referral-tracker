from django.contrib.auth import logout
from rest_framework import views, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, SessionSerializer


class SessionView(views.APIView):
    '''
    rest view set for Session
    '''
    class SessionPermission(permissions.BasePermission):

        def has_permission(self, request, view):
            if request.method == 'POST':
                return True
            return request.user.is_authenticated()

    permission_classes = (SessionPermission,)
    serializer_class = SessionSerializer

    def get(self, request, format=None):
        return Response(UserSerializer(request.user).data)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.filter(
            username=serializer.data['username']).first()
        if user and not user.is_active:
            return Response({'reason': 'User is inactive'}, status=403)

        if not user or not user.check_password(serializer.data['password']):
            return Response({'reason': 'Username or password is incorrect'},
                            status=400)
        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        user_id = request.user.id
        logout(request)
        return Response({'id': user_id})
