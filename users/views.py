from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.permissions import IsRealUser
from users.serializers import UserOtherSerializer, UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (AllowAny,)
        if self.action in ["destroy", "update", "partial_update"]:
            self.permission_classes = (IsRealUser,)
        return super().get_permissions()

    def get_serializer_class(self):
        if getattr(self, "swagger_fake_view", False):
            return UserSerializer
        if self.action == "create":
            return UserSerializer
        if self.action == "list":
            return UserOtherSerializer
        if self.action == "retrieve":
            if self.get_object() == self.request.user:
                return UserSerializer
            else:
                return UserOtherSerializer
        if self.action in ["update", "partial_update"]:
            if self.get_object() == self.request.user:
                return UserSerializer
