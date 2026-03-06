from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework import status
from library_app.models import AppLog, Book, Borrow, CustomUser, Favorite
from .serializers import AppLogSerializer, BookSerializer, BorrowedBookSerializer, FavoritedBookSerializer, UserSerializer
from rest_framework.decorators import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.db import transaction
import datetime
from django.db.models import Q
from .LinkedList import Node,LinkedList
from django.db import IntegrityError

# 404 handler
def handler404(request, exception):
    redirect('home')
    
# API view for listing API endpoints
class APIEndpoints(APIView):
    def get(self, request):
        # Generate a dictionary of endpoint URLs, descriptions, and access levels
        endpoints = {
            reverse('token_obtain_pair'): {
                'description': 'Get an authentication token (JWT).',
                'access_level': 'Public',  # No specific access level required
            },
            reverse('token_refresh'): {
                'description': 'Refresh an expired authentication token (JWT).',
                'access_level': 'Public',  # No specific access level required
            },
            reverse('users'): {
                'description': 'List all users.',
                'access_level': 'Superuser',  # Requires superuser access
            },
            reverse('user_profile'): {
                'description': 'View user profile information.',
                'access_level': 'Authenticated user',  # Requires authentication
            },
            reverse('register'): {
                'description': 'Register a new user account.',
                'access_level': 'Public',  # No specific access level required
            },
            reverse('logs'): {
                'description': 'Filter logs by user, date, and status code.',
                'access_level': 'Superuser',  # Requires superuser access
            },
        }
        
        # Return the dictionary of URLs, descriptions, and access levels in the response
        return Response(endpoints)
    
# API view for listing users
class UserList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    def get(self, request):
        # Retrieve a list of all users
        users = CustomUser.objects.all()
        
        # Serialize the user data
        serializer = UserSerializer(users, many=True)
        
        # Return the serialized data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogList(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        logs = AppLog.objects.select_related('user').all()

        user_id = request.GET.get('user')
        date = request.GET.get('date')
        status_code = request.GET.get('status_code')

        if user_id:
            logs = logs.filter(user_id=user_id)
        if date:
            logs = logs.filter(created_at__date=date)
        if status_code:
            logs = logs.filter(status_code=status_code)

        serializer = AppLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# API view for user profile
class UserProfile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Retrieve the user's profile based on the authenticated user's ID
        user = CustomUser.objects.get(id=request.user.id)
        
        # Serialize the user's profile data
        serializer = UserSerializer(user)
        
        # Return the serialized data in the response
        return Response(serializer.data, status=status.HTTP_200_OK)


# API view for user registration
class Register(APIView):
    def post(self, request):
        # Deserialize the request data using the UserSerializer
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            try:
                # If the serializer data is valid, create a new CustomUser
                CustomUser.objects.create_user(
                    user_name=serializer.validated_data['user_name'],
                    email=serializer.validated_data['email'],
                    password=serializer.validated_data['password'],
                    first_name=serializer.validated_data['first_name'],
                    last_name=serializer.validated_data['last_name'],
                    profile_image=serializer.validated_data.get('profile_image')
                )
                # Return a success response
                return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response(
                    {'user_name': ['A user with this user name already exists.']},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            except Exception as exc:
                return Response(
                    {'detail': f'Registration failed: {str(exc)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            # Return a response with serializer errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# API view for listing Books 
class BookList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
# API view for searching books
class SearchBook(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.GET.get('query', '').strip()
        print(query)    
        if(query == "author" or query == "title" or query == "isbn"):
            # sort = request.GET.get('sort', 'title')  # Default sort by title
            
            # Split the query by spaces
            # keywords = query.split()
            
            # Start with all books
            books = list(Book.objects.all())
            # # Filter the books based on the query keywords
            # for keyword in keywords:
            #     books = books.filter(
            #         Q(title__icontains=keyword) |
            #         Q(author__icontains=keyword) |
            #         Q(publication_date__icontains=keyword)
            #         # Add more fields as needed for your search
            #     )

            # Sort the results based on the specified sorting term using custom sorting algorithm
            if query == 'title':
                books = self.sort_by_title(books)
                print(books)
            elif query == 'author':
                print("geba")
                books = self.sort_by_author(books)
                print("weta")
                print("After sorted -> books", books)
            elif query == 'isbn':
                books = self.sort_by_isbn(books)
                print(books)
            # Serialize the book data
            serializer = BookSerializer(books, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:    
            query = request.GET.get('query', '').strip()

            # Start with all books
            books = Book.objects.all()
            
            # Filter the books based on the query parameter
            if query:
                books = books.filter( 
                    Q(author__icontains=query) |
                    Q(title__icontains=query) |
                    Q(isbn=query)
                )

            # Serialize the book's data
            serializer = BookSerializer(books, many=True)

            # Return the serialized data in the response
            return Response(serializer.data, status=status.HTTP_200_OK)
    
    def sort_by_title(self, books):
        # Custom sorting algorithm for title (bubble sort)
        n = len(books)
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if books[j].title > books[j + 1].title:
                    books[j], books[j + 1] = books[j + 1], books[j]
        return books

    def sort_by_author(self, books):
        # Custom sorting algorithm for author (selection sort)
        n = len(books) 
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if books[j].author < books[min_idx].author:
                    min_idx = j
            books[i], books[min_idx] = books[min_idx], books[i]
            
        return books

    def sort_by_isbn(self, books):
        # Custom sorting algorithm for isbn (insertion sort)
        n = len(books)
        for i in range(1, n):
            key = books[i]
            j = i - 1
            while j >= 0 and key.isbn < books[j].isbn:
                books[j + 1] = books[j]
                j -= 1
            books[j + 1] = key
        return books

class BorrowedBooksList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # get the user's object
        user = get_object_or_404(CustomUser, id=request.user.id)

        # Query for books borrowed by the usera
        borrowed_books = Borrow.objects.select_related('book').filter(user=user)

        # Serialize the borrowed book data using your serializer
        serializer = BorrowedBookSerializer(borrowed_books, many=True)

        return Response(serializer.data)

class ToggleFavoriteView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            user = request.user

            # Check if the book is already a favorite for the user
            is_favorite = Favorite.objects.filter(user=user, book=book).exists()

            if is_favorite:
                # If already a favorite, remove it
                Favorite.objects.filter(user=user, book=book).delete()
                return Response({'message': 'Book removed from favorites'}, status=status.HTTP_200_OK)
            else:
                # If not a favorite, add it
                Favorite.objects.create(user=user, book=book)
                return Response({'message': 'Book added to favorites'}, status=status.HTTP_201_CREATED)

        except Book.DoesNotExist:
            return Response({'message': 'Book not found'}, status=status.HTTP_404_NOT_FOUND)

 
class FavoritedBooksList(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # get the user's object
        user = get_object_or_404(CustomUser, id=request.user.id)

        # Query for books favorited by the usera
        favorited_books = Favorite.objects.select_related('book').filter(user=user)

        # Serialize the favorited book data using your serializer
        serializer = FavoritedBookSerializer(favorited_books, many=True)

        return Response(serializer.data)


class BorrowBookView(APIView):
    permission_classes = [IsAuthenticated]
    @transaction.atomic
    def post(self, request, book_id):
        try:
            book = Book.objects.get(pk=book_id)
            if book.quantity > 0:
                borrow = Borrow(
                    user=request.user,
                    book=book,
                    borrowed_date=datetime.date.today(),
                    quantity_borrowed=1,  # this Sets the quantity borrowed
                )
                borrow.save()

                # Decrement the book's quantity
                book.quantity -= borrow.quantity_borrowed
                book.save()

                return Response({'message': 'Book borrowed successfully.'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Book out of stock.'}, status=status.HTTP_400_BAD_REQUEST)
        except Book.DoesNotExist:
            return Response({'message': 'Book not found.'}, status=status.HTTP_404_NOT_FOUND)
