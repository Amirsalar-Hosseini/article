from .models import Article, Review, Like
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .serializers import ArticleSerializer, ReviewSerializer, LikeSerializer, TagSerializer


class ArticleListView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        articles = self.queryset.filter(is_confirmed=True)
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        article = self.queryset.get(pk=pk)
        serializer = self.serializer_class(article)
        return Response(serializer.data, status=status.HTTP_200_OK)
