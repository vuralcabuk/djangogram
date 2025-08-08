from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Post, SocialShare
from .serializers import PostSerializer, SocialShareSerializer
from .tasks import fake_facebook_share, fake_whatsapp_share, handle_social_share


class SocialShareCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = SocialShareSerializer(data=request.data)
        if serializer.is_valid():
            social_share = serializer.save(user=request.user)

            # Paylaşımı Celery ile yönet
            handle_social_share.delay(social_share.id)

            return Response(SocialShareSerializer(social_share).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SocialShareListView(generics.ListAPIView):
    queryset = SocialShare.objects.all().order_by('-created_at')
    serializer_class = SocialShareSerializer
    permission_classes = [permissions.IsAuthenticated]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        post = serializer.save(user=self.request.user)

        # Simülasyon paylaşım görevleri (Celery)
        fake_facebook_share.delay(post.id)
        fake_whatsapp_share.delay(post.id)
