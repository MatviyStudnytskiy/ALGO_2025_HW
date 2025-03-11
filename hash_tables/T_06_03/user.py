class Book:
    def __init__(self, author, title):
        self.author = author
        self.title = title

class Library:
    def __init__(self, size=100):  # Default hash table size is 100
        self.size = size
        self.table = [None] * size

    def _hash_function(self, author):
        # Basic custom hash function (forbidden to use built-in hash())
        hash_value = 0
        for char in author:
            hash_value += ord(char)
        return hash_value % self.size

    def init(self):
        """ Called once at the beginning of program execution. """
        self.table = [None] * self.size

    def addBook(self, author, title):
        """ Adds a book to the library. """
        index = self._hash_function(author)
        while self.table[index] is not None:
            index = (index + 1) % self.size
        self.table[index] = Book(author, title)

    def find(self, author, title):
        """ Checks if the given book is in the library. """
        index = self._hash_function(author)
        while self.table[index] is not None:
            if self.table[index].author == author and self.table[index].title == title:
                return True
            index = (index + 1) % self.size
        return False

    def delete(self, author, title):
        """ Deletes a book from the library. """
        index = self._hash_function(author)
        while self.table[index] is not None:
            if self.table[index].author == author and self.table[index].title == title:
                self.table[index] = None
                return
            index = (index + 1) % self.size

    def findByAuthor(self, author):
        """ Returns a list of books by the specified author. """
        books_by_author = []
        for book in self.table:
            if book and book.author == author:
                books_by_author.append(book.title)
        books_by_author.sort()  # Sort alphabetically
        return books_by_author

# Example usage:
if __name__ == "__main__":
    library = Library()

    # Adding books
    library.addBook("Stephen King", "The Shining")
    library.addBook("Stephen King", "It")
    library.addBook("J.K. Rowling", "Harry Potter and the Philosopher's Stone")
    library.addBook("J.K. Rowling", "Harry Potter and the Chamber of Secrets")

    # Finding books
    print(library.find("Stephen King", "It"))  # True
    print(library.find("J.K. Rowling", "Harry Potter"))  # False

    # Deleting a book
    library.delete("Stephen King", "It")
    print(library.find("Stephen King", "It"))  # False

    # Finding books by author
    print(library.findByAuthor("J.K. Rowling"))  # ['Harry Potter and the Chamber of Secrets', 'Harry Potter and the Philosopher's Stone']
