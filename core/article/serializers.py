from rest_framework import serializers
from .models import Article, Review, Like, Tag


class ArticleSerializer(serializers.ModelSerializer):
    likes = serializers.SerializerMethodField()
    reviews = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = '__all__'


    def get_likes(self, obj):
        result = obj.article_like.all()
        return LikeSerializer(result, many=True).data

    def get_reviews(self, obj):
        result = obj.reviews.all()
        return ReviewSerializer(result, many=True).data


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
