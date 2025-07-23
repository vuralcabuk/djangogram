from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics
from .models import SocialShare
from .serializers import SocialShareSerializer
from .tasks import fake_instagram_share  # bu görev birazdan çağrılacak


class SocialShareCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = SocialShareSerializer(data=request.data)
        if serializer.is_valid():
            # Modeli kaydet (ancak daha celery işlemeden)
            social_share = serializer.save(user=request.user)

            # Celery görevini çağır
            fake_instagram_share.delay(social_share.id, social_share.message)

            return Response(SocialShareSerializer(social_share).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SocialShareListView(generics.ListAPIView):
    queryset = SocialShare.objects.all().order_by('-created_at')
    serializer_class = SocialShareSerializer

