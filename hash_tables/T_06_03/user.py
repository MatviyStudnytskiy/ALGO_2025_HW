# user.py

TABLE_SIZE = 100003  
AUTHOR_TABLE_SIZE = 10007 

DELETED = ("#DELETED#", "#DELETED#")

# Main book catalog hash table
books_table = [None] * TABLE_SIZE

# Author to titles index: custom secondary hash table
author_table = [None] * AUTHOR_TABLE_SIZE


def init():
    global books_table, author_table
    books_table = [None] * TABLE_SIZE
    author_table = [None] * AUTHOR_TABLE_SIZE


def simple_hash(key, mod):
    """Custom polynomial rolling hash"""
    p = 53
    hash_value = 0
    for ch in key:
        hash_value = (hash_value * p + ord(ch)) % mod
    return hash_value


def generate_key(author, title):
    return f"{author}::{title}"


def probe(table, key, mod, for_insert=False):
    """Linear probing for key in given table"""
    index = simple_hash(key, mod)
    first_deleted = -1

    for i in range(mod):
        idx = (index + i) % mod
        entry = table[idx]

        if entry is None:
            return first_deleted if for_insert and first_deleted != -1 else idx

        if entry == DELETED:
            if first_deleted == -1:
                first_deleted = idx
        elif entry[0] == key:
            return idx

    return -1  # Table full


def addBook(author, title):
    global books_table, author_table

    # Add to main books table
    key = generate_key(author, title)
    idx = probe(books_table, key, TABLE_SIZE, for_insert=True)
    if idx == -1:
        return  # Table full, skip
    books_table[idx] = (key, (author, title))

    # Add to author → titles index
    akey = author
    aidx = probe(author_table, akey, AUTHOR_TABLE_SIZE, for_insert=True)

    if aidx == -1:
        return  # Table full, skip

    if author_table[aidx] is None or author_table[aidx] == DELETED:
        author_table[aidx] = (akey, [title])
    else:
        title_list = author_table[aidx][1]
        if title not in title_list:
            title_list.append(title)


def find(author, title):
    key = generate_key(author, title)
    idx = probe(books_table, key, TABLE_SIZE)
    if idx == -1:
        return False
    return books_table[idx] != DELETED and books_table[idx][1] == (author, title)


def delete(author, title):
    global books_table, author_table

    key = generate_key(author, title)
    idx = probe(books_table, key, TABLE_SIZE)
    if idx != -1 and books_table[idx] != DELETED:
        books_table[idx] = DELETED

    # Remove from author → titles index
    aidx = probe(author_table, author, AUTHOR_TABLE_SIZE)
    if aidx != -1 and author_table[aidx] != DELETED:
        titles = author_table[aidx][1]
        if title in titles:
            titles.remove(title)
        if not titles:
            author_table[aidx] = DELETED


def findByAuthor(author):
    aidx = probe(author_table, author, AUTHOR_TABLE_SIZE)
    if aidx == -1 or author_table[aidx] == DELETED:
        return []
    return sorted(author_table[aidx][1])
