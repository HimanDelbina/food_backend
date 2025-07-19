from rest_framework import viewsets, permissions
from .models import PasswordItem
from .serializers import PasswordItemSerializer
from rest_framework.decorators import permission_classes, api_view, throttle_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Q


class PasswordItemViewSet(viewsets.ModelViewSet):
    serializer_class = PasswordItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PasswordItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_passwords(request):
    query = request.GET.get("search", "")
    queryset = PasswordItem.objects.all()
    
    if query:
        queryset = queryset.filter(
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(title__icontains=query) |
            Q(username__icontains=query)
        )

    serializer = PasswordItemSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)