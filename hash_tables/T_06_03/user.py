class HashTable:
    def __init__(self, size=100003):  # Large prime number for better distribution
        self.size = size
        self.table = [None] * size
        self.deleted = object()

    def _hash(self, key):
        """ Custom hash function using polynomial rolling hash """
        p, m = 31, self.size
        hash_value = 0
        for c in key:
            hash_value = (hash_value * p + ord(c)) % m
        return hash_value

    def _probe(self, index):
        """ Linear probing """
        return (index + 1) % self.size

    def insert(self, key):
        index = self._hash(key)
        while self.table[index] is not None and self.table[index] != self.deleted:
            if self.table[index] == key:
                return  # Key already exists
            index = self._probe(index)
        self.table[index] = key

    def search(self, key):
        index = self._hash(key)
        start = index
        while self.table[index] is not None:
            if self.table[index] == key:
                return True
            index = self._probe(index)
            if index == start:
                break  # Full loop completed
        return False

    def delete(self, key):
        index = self._hash(key)
        start = index
        while self.table[index] is not None:
            if self.table[index] == key:
                self.table[index] = self.deleted
                return
            index = self._probe(index)
            if index == start:
                break


class Library:
    def __init__(self):
        self.books = HashTable()
        self.authors = {}

    def add_book(self, author, title):
        key = f"{author}={title}"
        self.books.insert(key)
        if author not in self.authors:
            self.authors[author] = set()
        self.authors[author].add(title)

    def find(self, author, title):
        return self.books.search(f"{author}={title}")

    def delete(self, author, title):
        key = f"{author}={title}"
        self.books.delete(key)
        if author in self.authors:
            self.authors[author].discard(title)

    def find_by_author(self, author):
        return sorted(self.authors.get(author, []))


library = None

def init():
    global library
    library = Library()

def addBook(author, title):
    library.add_book(author, title)

def find(author, title):
    return library.find(author, title)

def delete(author, title):
    library.delete(author, title)

def findByAuthor(author):
    return library.find_by_author(author)
