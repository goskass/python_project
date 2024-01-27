from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f"{self.authorUser.username}"

class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    NEWS = 'NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICE = (
        (NEWS, 'Новости'),
        (ARTICLE, 'Статья'),
    )

    categoryType = models.CharField(max_length=2, choices=CATEGORY_CHOICE, default=NEWS)
    dateCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, 'PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField()
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return f'{self.text[0:123]}...'

    def __str__(self):
        return f"Новость: {self.title}"


class PostCategory(models.Model):
    categoryThrough = models.ForeignKey(Category, on_delete=models.CASCADE)
    postThrough = models.ForeignKey(Post, on_delete=models.CASCADE)


class Comment(models.Model):
    commentPost = models.ForeignKey(Post, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreations = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def __str__(self):
        return f"Комментарий пользователя {self.commentUser.username} к новости: {self.commentPost.title}"