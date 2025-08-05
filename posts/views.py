from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import SocialShare
from .serializers import SocialShareSerializer
from .tasks import handle_social_share  # Tek bir görev tüm platformları yönetecek


class SocialShareCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SocialShareSerializer(data=request.data)
        if serializer.is_valid():
            # Paylaşımı kaydet
            social_share = serializer.save(user=request.user)

            # Celery görevi: platforma göre yönlendirme yapar
            handle_social_share.delay(social_share.id)

            return Response(SocialShareSerializer(social_share).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialShareListView(generics.ListAPIView):
    queryset = SocialShare.objects.all().order_by('-created_at')
    serializer_class = SocialShareSerializer
    permission_classes = [permissions.IsAuthenticated]
