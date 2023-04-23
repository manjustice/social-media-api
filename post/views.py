from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Post
from .serializers import PostSerializer, PostListSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().prefetch_related("hashtags")
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    @staticmethod
    def _params_to_ints(qs):
        """Converts a list of string IDs to a list of integers"""
        return [int(str_id) for str_id in qs.split(",")]

    def get_queryset(self):
        followed_users_ids = (
            self.request.user.profile.followers.all()
        )
        user_profile_id = self.request.user.profile.id

        queryset = self.queryset.filter(
            author__in=list(followed_users_ids) + [user_profile_id]
        )

        hashtags = self.request.query_params.get("hashtags")
        if hashtags:
            hashtags_ids = self._params_to_ints(hashtags)
            queryset = (queryset.filter(hashtags__id__in=hashtags_ids))

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return PostListSerializer
        return PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "hashtags",
                type={"type": "list", "items": {"type": "number"}},
                description="Filter by hashtags id (ex. ?hashtags=2,5)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
