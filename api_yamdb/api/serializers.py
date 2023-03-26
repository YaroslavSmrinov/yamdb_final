from django.utils import timezone
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from reviews.models import Category, Comment, Genre, Review, Title


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    score = serializers.IntegerField(min_value=1, max_value=10)
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',)

    class Meta:
        model = Review
        fields = ('id', 'author', 'text', 'score', 'pub_date',)

    def validate(self, data):
        if self.context['request'].method != 'POST':
            return data
        title = get_object_or_404(
            Title,
            id=self.context['request'].parser_context['kwargs']['title_id']
        )
        if Review.objects.filter(
            author=self.context['request'].user,
            title=title
        ).exists():
            raise serializers.ValidationError(
                'Вы пытаетесь оставить второй отзыв на фильм.'
            )
        return data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Genre


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        exclude = ('id',)
        model = Category


class GetTitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(read_only=True, many=True)
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class CreateTitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all()
    )
    genre = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Genre.objects.all(),
        many=True
    )

    class Meta:
        model = Title
        fields = '__all__'

    @staticmethod
    def validate_year(value):
        year = timezone.now().year
        if value > year:
            raise serializers.ValidationError('Произведение ещё не вышло.')
        return value
