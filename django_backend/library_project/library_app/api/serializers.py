from rest_framework import serializers
from library_app.models import CustomUser
from library_app.models import AppLog, Book, Borrow, Favorite

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True},
            'profile_image': {'required': False, 'allow_null': True},
        }
        

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowedBookSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Borrow
        fields = ('book',)

    def get_book(self, obj):
        book = obj.book
        return {
            'id' : book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'quantity': book.quantity,
            'cover_image': book.cover_image.url,
            'isbn': book.isbn, 
            'inserted_date': book.inserted_date,
        }


class FavoritedBookSerializer(serializers.ModelSerializer):
    book = serializers.SerializerMethodField()

    class Meta:
        model = Favorite
        fields = ('book',)

    def get_book(self, obj):
        book = obj.book
        return {
            'id' : book.id,
            'title': book.title,
            'author': book.author,
            'genre': book.genre,
            'quantity': book.quantity,
            'cover_image': book.cover_image.url,
            'isbn': book.isbn, 
            'inserted_date': book.inserted_date,
        }


class AppLogSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.user_name', read_only=True)

    class Meta:
        model = AppLog
        fields = (
            'id',
            'user',
            'user_name',
            'level',
            'event',
            'message',
            'path',
            'method',
            'status_code',
            'metadata',
            'created_at',
        )
