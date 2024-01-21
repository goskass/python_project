from django.shortcuts import render, get_object_or_404
from .models import Post

def news_list(request):
    news = Post.objects.filter(categoryType='NW').order_by('-dateCreation')[:10]
    return render(request, 'news/news_list.html', {'news': news})

def article_list(request):
    article = Post.objects.filter(categoryType='AR').order_by('-dateCreation')[:10]
    return render(request, 'news/article_list.html', {'article': article})

def news_detail(request, pk):
    news = get_object_or_404(Post, pk=pk)
    return render(request, 'news/news_detail.html', {'news': news})

def article_detail(request, pk):
    article = get_object_or_404(Post, pk=pk)
    return render(request, 'news/article_detail.html', {'article': article})