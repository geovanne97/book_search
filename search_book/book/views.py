from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from book.serializer import BookSerializer, ReviewSerializer
from book.models import *
from book.utils import create_book

import requests
import json

# Create your views here.

class SearchBookViewSet(APIView):
    """Return book description."""
    http_method_names = ['post', 'get']

    def get_books(self, title):
        url='https://gutendex.com/books?search={}'.format(title)
        response = requests.get(url)

        r_bytes = response.__dict__['_content']
        r_string = r_bytes.decode('utf-8')
        r_json = json.loads(r_string)
        r_results = r_json['results']

        return r_results
    
    def create_body(self, book):
        authors = Authors.objects.filter(books__in=[book.id])
        authors_list = []
        for author in authors:
            author_dict = {}
            author_dict['name'] = author.name
            author_dict['birth_year'] = author.birth_year
            author_dict['death_year'] = author.death_year
            authors_list.append(author_dict)
        
        languages = Language.objects.filter(books__in=[book.id])
        languages_list = []
        for idiom in languages:
            languages_list.append(idiom.language)
        
        review_list = []
        reviews = Review.objects.filter(book=book.id)
        for review in reviews:
            review_list.append(review.review)
        
        data = {
            'id': book.id,
            'title': book.title,
            'authors': authors_list,
            'languages': languages_list,
            'download_count': book.download_count,
            'rating_avg': book.rating_avg,
            'reviews': review_list
        }
        return data
        
    
    def get(self, request):
        """Route to get ten top films."""
        books = Book.objects.all().order_by('-rating_avg')
        top_books = books[:10]
        results = []
        for book_item in top_books:
            data = self.create_body(book_item)
            results.append(data)

        return Response({'results': results},
                        status=status.HTTP_200_OK)

    def post(self, request, format='json'):
        """Endpoint to post book title."""
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=400)
        
        valid_data = serializer.validated_data
        title = valid_data.pop('title', [])
        books = self.get_books(title)

        if books == [] or books is None:
            return Response({'detail': 'Book not found'},
                            status=status.HTTP_400_BAD_REQUEST)

        book_status = create_book(books, title)
        if book_status is False:
            return Response({'detail': 'Not possible to create book'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        book = Book.objects.get(title=title)
        data = self.create_body(book)

        return Response(data,
                        status=status.HTTP_200_OK)


class ReviewBookViewSet(APIView):
    """Post book review."""
    http_method_names = ['post']

    def post(self, request, format='json'):
        """Endpoint to post book review."""
        serializer = ReviewSerializer(data=request.data)

        if serializer.is_valid() is False:
            return Response(serializer.errors, status=400)

        valid_data = serializer.validated_data
        book_title = valid_data['book']
        try:
            book = Book.objects.get(title=book_title)
        except Exception as e:
            return Response({"detail": "This book does not exist in database"},
                            status=400)
            
        try:
            Review.objects.create(
                review=valid_data['review'],
                rating=valid_data['rating'],
                book=book
            )
            book.update_rating_avg()
            return Response({"detail": "Review created"},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": "Was not possible to create review"},
                            status=400)