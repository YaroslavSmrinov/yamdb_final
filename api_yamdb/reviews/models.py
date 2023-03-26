from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.constraints import UniqueConstraint

from .validators import MinMaxValidator, year_validator

User = get_user_model()


class Category(models.Model):
    """ Модель категорий произведений """
    name = models.TextField(
        verbose_name='Категория',
        blank=False,
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Ссылка',
        max_length=50,
    )

    class Meta:
        verbose_name = 'Категория произведения'
        verbose_name_plural = 'Категории произведений'
        ordering = ('name',)

    def __str__(self):
        return self.slug


class Genre(models.Model):
    name = models.TextField(
        verbose_name='Жанр',
        max_length=256,
        db_index=True,
    )
    slug = models.SlugField(
        unique=True,
        blank=False,
        verbose_name='Ссылка',
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.slug


class Title(models.Model):
    """ Модель произведений """
    name = models.TextField(
        max_length=256,
        verbose_name='Произведение',
        db_index=True,
    )
    year = models.IntegerField(
        validators=[
            year_validator,
        ],
        verbose_name='Год опубликования',
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        related_name='titles',
        verbose_name='Категория произведения',
        on_delete=models.SET_NULL,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанры',
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
    )

    def display_genre(self):
        """ Отображение жанра в админ-панели """
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Жанр'

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:256]


class Review(models.Model):
    text = models.TextField(
        verbose_name='Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[
            MinMaxValidator(
                1,
                10,
                message=(
                    'Оценка должна лежать в пределах от 1 до 10 включительно.'
                )
            ),
        ]
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['-pub_date']
        constraints = [
            UniqueConstraint(
                fields=('author', 'title'),
                name='review_from_unique_author'
            ),
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв на фильм',
    )
    text = models.TextField(
        verbose_name='Текст комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации комментария'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Комментатор',
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
