from django.contrib.auth.decorators import login_required
from django.db.models import OuterRef, Exists
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.decorators.csrf import csrf_protect
from django.views.generic import ListView, DetailView
from .filters import PostFilter
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from .models import Post, Category, Subscription
from .forms import PostCreationForm, ArticlePostUpdateForm, NewsPostUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin


class NewsList(ListView):
    model = Post
    ordering = '-dateCreation'
    template_name = 'news_list.html'
    context_object_name = 'news'
    paginate_by = 10


class NewsDetail(LoginRequiredMixin, DetailView):
    raise_exception = True
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


class PostCreateView(PermissionRequiredMixin, CreateView, ):
    permission_required = 'news.add_post'
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


class NewsPostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
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


class ArticlePostUpdateView(PermissionRequiredMixin, UpdateView):
    permission_required = 'news.change_post'
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


class PostDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'news.delete_post'
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )
