from rest_framework import serializers
from blog.models import BlogPost, BannerImage, Author

class DynamicFieldsModelSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)
        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class AuthorSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'first_name', 'last_name', 'email']


class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BannerImage
        fields = ['id', 'image']

class BlogPostListSerializer(serializers.ModelSerializer):
    banner_image = serializers.SerializerMethodField()

    def get_banner_image(self, obj):
        if hasattr(obj, "banner_image") and obj.banner_image and obj.banner_image.image:
            return obj.banner_image.image.url
        return None

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'category', 'banner_image']


class BlogPostDetailSerializer(BlogPostListSerializer):

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'category', 'banner_image', 'text', 'website', 'create_date']


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    banner_image = serializers.ImageField(required=False)

    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'text', 'website', 'banner_image']

    def create(self, validated_data):
        banner_image = validated_data.pop('banner_image', None)
        blog_post = BlogPost.objects.create(**validated_data)
        if banner_image:
            BannerImage.objects.create(blog_post=blog_post, image=banner_image)
        return blog_post

    def update(self, instance, validated_data):
        banner_image = validated_data.pop('banner_image', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if banner_image:
            if hasattr(instance, 'banner_image') and instance.banner_image is not None:
                instance.banner_image.image = banner_image
                instance.banner_image.save()
            else:
                BannerImage.objects.create(blog_post=instance, image=banner_image)

        return instance
