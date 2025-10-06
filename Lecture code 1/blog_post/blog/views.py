from rest_framework import mixins, viewsets, status
from rest_framework.response import Response

from blog.models import BlogPost, Author
from blog.serializers import (
    BlogPostListSerializer,
    BlogPostDetailSerializer,
    BlogPostCreateUpdateSerializer, AuthorSerializer
)


class BlogPostListViewSet(mixins.ListModelMixin,
                         viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostListSerializer


class BlogPostCreateViewSet(mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = BlogPost.objects.all()
    serializer_class = BlogPostCreateUpdateSerializer


class BlogPostDetailViewSet(mixins.RetrieveModelMixin,
                           viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostDetailSerializer


class BlogPostUpdateViewSet(mixins.UpdateModelMixin,
                           viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostCreateUpdateSerializer


class BlogPostDeleteViewSet(mixins.DestroyModelMixin,
                           viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostListSerializer


class BlogPostViewSet(viewsets.ModelViewSet):
    queryset = BlogPost.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return BlogPostCreateUpdateSerializer
        elif self.action == 'retrieve':
            return BlogPostDetailSerializer
        return BlogPostListSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        res.data = {
            "count": self.get_queryset().count(),
            "deleted_count": BlogPost.objects.filter(deleted=True).count(),
            "results": res.data,
        }
        return res

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.deleted = True
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

    def get_serializer(self, *args, **kwargs):
        if self.action == 'list':
            kwargs['fields'] = ('first_name', 'last_name')
        elif self.action == 'update':
            kwargs['fields'] = ('first_name', 'last_name', 'email')
        return super().get_serializer(*args, **kwargs)
