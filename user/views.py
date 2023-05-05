from django.contrib.auth import get_user_model
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import generics, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.models import Profile
from user.serializers import (
    UserSerializer,
    ProfileListSerializer,
    ProfileDetailSerializer,
)
from .permissions import IsUserOrReadOnly


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class ManageProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticated, IsUserOrReadOnly)

    def get_queryset(self):
        queryset = self.queryset
        username = self.request.query_params.get("username")

        if username:
            queryset = queryset.filter(username__icontains=username)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ProfileDetailSerializer

        return ProfileListSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=["GET"], detail=True, url_path="follow")
    def follow_unfollow_user(self, request, pk=None):
        user = get_user_model().objects.get(id=request.user.id)
        following = get_user_model().objects.get(id=pk)
        if user != following:
            if user in following.profile.followers.all():
                following.profile.followers.remove(user.id)
            else:
                following.profile.followers.add(user.id)

            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                "username",
                type=OpenApiTypes.STR,
                description="Filter by user's username (ex. ?username=user)",
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
