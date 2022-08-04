from book.models import*

def create_book(books, title_request):
    book_status = False
    book_exist = Book.objects.filter(title=title_request).exists()

    if book_exist:
        book_status = True
        return book_exist

    for book in books:
        title = book['title']
        book_exist2 = Book.objects.filter(title=book['title']).exists()

        if book_exist2 is False and title == title_request:
            download_count = book['download_count']
            book_obj = Book.objects.create(
                title=title,
                download_count=download_count)
            
            authors = book['authors']
            for author in authors:
                author_exist = Authors.objects.filter(
                    name=author['name'],
                    birth_year=author['birth_year'],
                    death_year=author['death_year'],
                ).exists()

                if author_exist is False:
                    author = Authors.objects.create(
                        name=author['name'],
                        birth_year=author['birth_year'],
                        death_year=author['death_year'],
                        # books=book_obj
                    )
                    author.books.add(book_obj)
                else:
                    author = Authors.objects.get(
                        name=author['name'],
                        birth_year=author['birth_year'],
                        death_year=author['death_year'],
                    )
                    author.books.add(book_obj)

            
            languages = book['languages']
            for language in languages:
                language_exists = Language.objects.filter(
                    language=language
                ).exists()

                if language_exists is False:
                    language = Language.objects.create(
                        language=language,
                        # book=book_obj
                    )
                    language.books.add(book_obj)
                else:
                    language = Language.objects.get(
                        language=language
                    )
                    language.books.add(book_obj)
            
            book_status = True

    return book_status
