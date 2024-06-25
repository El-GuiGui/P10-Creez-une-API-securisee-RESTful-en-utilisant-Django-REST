from rest_framework.routers import DefaultRouter
from .views import (
    ProjectViewSet,
    ContributorViewSet,
    IssueViewSet,
    CommentViewSet,
    UserProfileViewSet,
    UserRegistrationView,
    UserDeleteView,
)
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = DefaultRouter()
router.register(r"projects", ProjectViewSet)
router.register(r"contributors", ContributorViewSet)
router.register(r"issues", IssueViewSet)
router.register(r"comments", CommentViewSet)
router.register(r"userprofiles", UserProfileViewSet)

urlpatterns = router.urls


urlpatterns = [
    path("", include(router.urls)),
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("delete/", UserDeleteView.as_view(), name="delete_user"),
]
