создаем юзеров
user1 = User.objects.create_user('Весельчак')
user2 = User.objects.create_user('Ворчун')

создаем авторов привязанных к юзерам
author1 = Author.objects.create(authorUser=user1)
author2 = Author.objects.create(authorUser=user2)

Добавление категорий
category1 = Category.objects.create(name='Книги')
category2 = Category.objects.create(name='Мультфильмы')
category3 = Category.objects.create(name='Кино')
category4 = Category.objects.create(name='Игры')

Добавить 2 статьи и 1 новость.
post1 = Post.objects.create(author=author1, categoryType='AR', title='О главном', text='все простое –самое важное')
post2 = Post.objects.create(author=author2, categoryType='AR', title='Смотреть всем', text='Никто не пожалеет')
news1 = Post.objects.create(author=author1, categoryType='NW', title='Все видели', text='Это надо смотреть')

Присвоить им категории (как минимум в одной статье/новости должно быть не меньше 2 категорий).
post1.postCategory.add(category1, category3)
post2.postCategory.add(category2, category3)
news1.postCategory.add(category2, category4)

Создать как минимум 4 комментария к разным объектам модели Post (в каждом объекте должен быть как минимум один комментарий).
comment1 = Comment.objects.create(commentPost=post1, commentUser=user1, text='вау, класс!!')
comment2 = Comment.objects.create(commentPost=post2, commentUser=user2, text='отстой')
comment3 = Comment.objects.create(commentPost=news1, commentUser=user1, text='респект')
comment4 = Comment.objects.create(commentPost=news1, commentUser=user2, text='Cойдет')

Применяя функции like() и dislike() к статьям/новостям и комментариям, скорректировать рейтинги этих объектов.
post1.like()
post1.like()
post1.like()
post2.dislike()
comment1.like()
comment2.like()
comment2.like()
comment3.dislike()
comment4.like()
comment1.like()
comment3.dislike()
comment2.like()

Обновить рейтинги пользователей
author1.update_rating()
author2.update_rating()

Вывести username и рейтинг лучшего пользователя (применяя сортировку и возвращая поля первого объекта).
best_user = Author.objects.all().order_by('-ratingAuthor').first()
 print(f'Best User: {best_user.authorUser.username}, Rating: {best_user.ratingAuthor}')

Вывести дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи, основываясь на лайках/дислайках к этой статье
best_post = Post.objects.all().order_by('-rating').first()
>>> print(f'Date: {best_post.dateCreation}, Author: {best_post.author.authorUser.username}, Rating: {best_post.rating}, Title: {best_post.title}, Preview: {best_post.preview()}')

Вывести все комментарии (дата, пользователь, рейтинг, текст) к этой статье.
comments_to_best_post = Comment.objects.filter(commentPost=best_post)
for comment in comments_to_best_post:
    print(f"Date: {comment.dateCreations}, User: {comment.commentUser.username}, "
          f"Rating: {comment.rating}, Text: {comment.text}")

