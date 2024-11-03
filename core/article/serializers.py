from rest_framework import serializers
from .models import Article, Review, Like, Tag


class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Article
        fields = '__all__'
        read_only_fields = ['author',]

    def get_likes(self, obj):
        result = obj.article_like.all()
        return LikeSerializer(result, many=True).data

    def get_reviews(self, obj):
        result = obj.reviews.all()
        return ReviewSerializer(result, many=True).data

    def create(self, validated_data):
        tags_data = validated_data.pop('tags')
        article = Article.objects.create(**validated_data)
        tag_objects = []
        for tag_name in tags_data:
            tag, created = Tag.objects.get_or_create(name=tag_name)
            tag_objects.append(tag)

        article.tags.set(tag_objects)
        return article


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'
