from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.access import is_director

from .serializers import SchoolSerializer


class SchoolView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        if not request.user.school_id:
            return Response({})
        serializer = SchoolSerializer(request.user.school)
        return Response(serializer.data)

    def patch(self, request):
        if not is_director(request.user):
            raise PermissionDenied('Only directors can update school information.')
        if not request.user.school_id:
            raise PermissionDenied('Your account is not connected to a school.')

        serializer = SchoolSerializer(
            request.user.school,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
