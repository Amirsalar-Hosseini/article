from django.db import models
from accounts.models import User


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    poster = models.ImageField(upload_to="articles/%Y/%m/%d")
    duration = models.IntegerField(help_text='duration in minutes for reading')
    tags = models.ManyToManyField('Tag', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_confirmed = models.BooleanField(default=False)


    def __str__(self):
        return self.title

    def likes_count(self):
        return self.article_like.count()

    def user_can_like(self, user):
        user_like = user.user_likes.filter(article=self)
        if user_like.exists():
            return True
        return False


class Tag(models.Model):
    """
    for tags category
    """
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Review(models.Model):
    """
    define user comments
    """
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
    is_reply = models.BooleanField(default=False)

    def __str__(self):
        return f'Review by {self.author.first_name} {self.author.last_name} for {self.article.title}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_like')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_like')


    def __str__(self):
        return f'{self.user} liked {self.article}'