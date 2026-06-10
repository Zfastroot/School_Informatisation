from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.access import is_director

from .models import User
from .serializers import CurrentUserSerializer, LoginSerializer, UserSerializer


class LoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.create_token_response())


class CurrentUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = CurrentUserSerializer(request.user)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        if not is_director(user) or not user.school_id:
            return User.objects.none()

        queryset = User.objects.filter(school=user.school)
        role = self.request.query_params.get('role')
        is_active = self.request.query_params.get('is_active')

        if role:
            queryset = queryset.filter(role=role)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() in ('1', 'true', 'yes'))

        return queryset.order_by('full_name')

    def _require_director_with_school(self):
        if not is_director(self.request.user):
            raise PermissionDenied('Only directors can manage users.')
        if not self.request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

    def perform_create(self, serializer):
        self._require_director_with_school()
        serializer.save(school=self.request.user.school)

    def perform_update(self, serializer):
        self._require_director_with_school()
        serializer.save(school=self.request.user.school)

    def destroy(self, request, *args, **kwargs):
        self._require_director_with_school()
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active'])
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['patch'])
    def deactivate(self, request, pk=None):
        self._require_director_with_school()
        user = self.get_object()
        user.is_active = False
        user.save(update_fields=['is_active'])
        serializer = self.get_serializer(user)
        return Response(serializer.data)
