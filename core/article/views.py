from permissions import IsVerify, IsOwner
from .models import Article, Review, Like
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import ArticleSerializer, ReviewSerializer, LikeSerializer, TagSerializer
from accounts.models import User

class ArticleListView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request):
        articles = self.queryset.filter(is_confirmed=True)
        ser_data = self.serializer_class(articles, many=True)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ArticleDetailView(APIView):
    serializer_class = ArticleSerializer
    queryset = Article.objects.all()
    permission_classes = (AllowAny,)

    def get(self, request, pk):
        article = self.queryset.get(pk=pk)
        ser_data = self.serializer_class(article)
        return Response(ser_data.data, status=status.HTTP_200_OK)


class ArticleCreateView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = (IsVerify,)
    queryset = Article.objects.all()

    def post(self, request, *args, **kwargs):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            ser_data.save(author=request.user)
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleUpdateView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = (IsVerify, IsOwner)
    queryset = Article.objects.all()

    def put(self, request, pk):
        article = self.queryset.get(pk=pk)
        ser_data = self.serializer_class(instance=article, data=request.data, partial=True)
        if ser_data.is_valid():
            ser_data.save(author=request.user)
            return Response(ser_data.data, status=status.HTTP_200_OK)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class ArticleDeleteView(APIView):
    serializer_class = ArticleSerializer
    permission_classes = (IsVerify, IsOwner)
    queryset = Article.objects.all()

    def delete(self, request, pk):
        article = self.queryset.get(pk=pk)
        self.check_object_permissions(request, article)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
