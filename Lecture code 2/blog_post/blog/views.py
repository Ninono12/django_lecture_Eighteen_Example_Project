from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

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


class BlogPostDetailViewSet(mixins.RetrieveModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostDetailSerializer


class BlogPostUpdateViewSet(mixins.UpdateModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostCreateUpdateSerializer


class BlogPostCreateViewSet(mixins.CreateModelMixin,
                            viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostCreateUpdateSerializer


class  BlogPostDeleteViewSet(mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    queryset = BlogPost.objects.filter(deleted=False)
    serializer_class = BlogPostListSerializer


class BlogPostViewSet(ModelViewSet):
    queryset = BlogPost.objects.filter(deleted=False)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return BlogPostDetailSerializer
        elif self.action == 'create' or self.action == 'update':
            return BlogPostCreateUpdateSerializer
        else:
            return BlogPostListSerializer

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {
            "total_products": self.get_queryset().count(),
            "paginated_results": response.data
        }
        return response

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
