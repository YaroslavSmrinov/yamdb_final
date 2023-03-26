from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.views import TokenObtainView, UserViewSet, user_sign_up

from .views import (CategoryViewSet, CommentViewSet, GenresViewSet,
                    ReviewViewSet, TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register('users', UserViewSet, basename='users')
router_v1.register(r'titles', TitleViewSet, basename='title')
router_v1.register('genres', GenresViewSet, basename='Genre')
router_v1.register('categories', CategoryViewSet, basename='Category')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews')

auth_urls = [
    path(
        'auth/signup/', user_sign_up,
        name='sign_up'
    ),
    path(
        'auth/token/', TokenObtainView.as_view(),
        name='token_obtain'
    ),
]

urlpatterns = [
    path('v1/', include(auth_urls)),
    path('v1/', include(router_v1.urls))
]
