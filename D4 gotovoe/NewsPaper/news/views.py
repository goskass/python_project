from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView
from .filters import PostFilter
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Post
from .forms import PostCreationForm,ArticlePostUpdateForm, NewsPostUpdateForm



class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10

class NewsDetail(DetailView):
    model = Post
    template_name = 'news_detail.html'
    context_object_name = 'news'

class NewsSearch(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 2

    def get_queryset(self):
           queryset = super().get_queryset()
           self.filterset = PostFilter(self.request.GET, queryset)
           return self.filterset.qs

    def get_context_data(self, **kwargs):
           context = super().get_context_data(**kwargs)
           context['filterset'] = self.filterset
           return context


class PostCreateView(CreateView):
    model = Post
    form_class = PostCreationForm
    template_name = 'post_create.html'
    success_url = '/news/'

    def form_valid(self, form):
        #  логика  для определения типа новость или статья
        post_type = self.kwargs.get('post_type')
        if post_type == 'news':
            form.instance.categoryType = Post.NEWS
        elif post_type == 'article':
            form.instance.categoryType = Post.ARTICLE

        return super().form_valid(form)


class NewsPostUpdateView(UpdateView):
    model = Post
    template_name = 'news_post_update.html'
    form_class = NewsPostUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка категории поста
        if self.object.categoryType == Post.ARTICLE and 'article' not in self.request.path:
            # Если  статья, а урлы указывают на  новость, делаем редирект
            return redirect(reverse('update_article', kwargs={'pk': self.object.pk}))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)


class ArticlePostUpdateView(UpdateView):
    model = Post
    template_name = 'article_post_update.html'
    form_class = ArticlePostUpdateForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Проверка категории поста
        if self.object.categoryType == Post.NEWS and 'news' not in self.request.path:
            # Если  новость, а урлы указывают на  статью, делаем редирект
            return redirect(reverse('update_news', kwargs={'pk': self.object.pk}))

        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        return super().form_valid(form)

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')
