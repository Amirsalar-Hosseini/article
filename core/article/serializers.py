from rest_framework import serializers
from .models import Article, Review, Like, Tag


class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()
    tags = serializers.ListField(child=serializers.CharField(), write_only=True)

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
        tags_data = validated_data.pop('tags', [])
        article = Article.objects.create(**validated_data)
        for tag_name in tags_data:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            article.tags.add(tag)

        return article

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['tags'] = list(instance.tags.values_list('name', flat=True))
        return representation


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
