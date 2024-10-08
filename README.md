# dbj

[![CI](https://github.com/pdrb/dbj/actions/workflows/ci.yml/badge.svg)](https://github.com/pdrb/dbj/actions/workflows/ci.yml)
[![Coverage](https://coveralls.io/repos/github/pdrb/dbj/badge.svg?branch=master)](https://coveralls.io/github/pdrb/dbj?branch=master)
[![Version](https://img.shields.io/pypi/v/dbj.svg)](https://pypi.python.org/pypi/dbj)
[![Downloads](https://static.pepy.tech/badge/dbj)](https://pepy.tech/project/dbj)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![LICENSE](https://img.shields.io/github/license/pdrb/dbj)](https://github.com/pdrb/dbj/blob/master/LICENSE)

dbj is a simple embedded in memory json database.

It is easy to use, fast and has a simple query language.

The code is fully documented, tested and beginner friendly.

Only the standard library is used and it works on Python 3.8+. For older Python (2.7, 3.4...) use version `0.1.10`.

## Usage

```python
>>> from dbj import dbj
>>> db = dbj('mydb.json')

>>> # Insert using an auto generated uuid1 key
>>> db.insert({'name': 'John', 'age': 18})
'a71d90ce0c7611e995faf23c91392d78'

>>> # Insert using a supplied key, in this case 'anab@example.org'
>>> user = {'name': 'Ana Beatriz', 'age': 10}
>>> db.insert(user, 'anab@example.org')
'anab@example.org'

>>> db.insert({'name': 'Bob', 'age': 30})
'cc6ddfe60c7611e995faf23c91392d78'

>>> db.get('a71d90ce0c7611e995faf23c91392d78')
{'name': 'John', 'age': 18}

>>> db.get('anab@example.org')
{'name': 'Ana Beatriz', 'age': 10}

>>> db.find('age >= 18')
['a71d90ce0c7611e995faf23c91392d78', 'cc6ddfe60c7611e995faf23c91392d78']

>>> db.find('name == "ana beatriz"')
['anab@example.org']

>>> r = db.find('name == "John" or name == "Bob" and age > 10')
>>> db.getmany(r)
[{'name': 'Bob', 'age': 30}, {'name': 'John', 'age': 18}]

>>> # Sort the result by age
>>> r = db.sort(r, 'age')
>>> db.getmany(r)
[{'name': 'John', 'age': 18}, {'name': 'Bob', 'age': 30}]

>>> # Sort can also be used from find directly
>>> r = db.find('age >= 10', sortby='age')
>>> db.getmany(r)
[{'name': 'Ana Beatriz', 'age': 10}, {'name': 'John', 'age': 18}, {'name': 'Bob', 'age': 30}]

>>> # One-liner:
>>> db.getmany(db.find('age >= 10', sortby='age'))
[{'name': 'Ana Beatriz', 'age': 10}, {'name': 'John', 'age': 18}, {'name': 'Bob', 'age': 30}]

>>> db.save()
True
```

## Install

Install using pip:

```shell
pip install dbj
```

## Examples
Check the [available commands](#available-commands) for a full list of supported methods.

Import the module and create a new database:

```python
>>> from dbj import dbj
>>> db = dbj('mydb.json')
```

Insert a few documents with auto generated key:

```python
>>> doc = {'name': 'John Doe', 'age': 18}
>>> db.insert(doc)
'7a5ebd420cb211e98a0ff23c91392d78'

>>> docs = [{'name': 'Beatriz', 'age': 30}, {'name': 'Ana', 'age': 10}]
>>> db.insertmany(docs)
2
```

Insert with a supplied key:

```python
>>> doc = {'name': 'john', 'age': 20, 'country': 'Brasil'}
>>> db.insert(doc, '1')
1

>>> db.insert({'name': 'Bob', 'age': 40}, '2')
2

>>> db.getallkeys()
['7a5ebd420cb211e98a0ff23c91392d78', 'db21baf80cb211e98a0ff23c91392d78', 'db21edde0cb211e98a0ff23c91392d78', '1', '2']
```

Pop and delete:

```python
>>> db.delete('1')
True

>>> db.poplast()
{'name': 'Bob', 'age': 40}

>>> db.size()
3

>>> db.getallkeys()
['7a5ebd420cb211e98a0ff23c91392d78', 'db21baf80cb211e98a0ff23c91392d78', 'db21edde0cb211e98a0ff23c91392d78']
```

Updating an existing document:

```python
>>> db.insert({'name': 'Ethan', 'age': 40}, '1000')
'1000'

>>> db.get('1000')
{'name': 'Ethan', 'age': 40}

>>> db.update('1000', {'age': 50})
True

>>> db.get('1000')
{'name': 'Ethan', 'age': 50}

>>> db.update('1000', {'name': 'Ethan Doe', 'gender': 'male'})
True

>>> db.pop('1000')
{'name': 'Ethan Doe', 'age': 50, 'gender': 'male'}
```

Retrieving some documents:

```python
>>> db.getall()
[{'name': 'John Doe', 'age': 18}, {'name': 'Beatriz', 'age': 30}, {'name': 'Ana', 'age': 10}]

>>> db.getfirst()
{'name': 'John Doe', 'age': 18}

>>> db.getlast()
{'name': 'Ana', 'age': 10}

>>> db.getrandom() # returns a random document
{'name': 'Ana', 'age': 10}
```

Check for existance:

```python
>>> db.exists('7a5ebd420cb211e98a0ff23c91392d78')
True
```

Searchin and sorting:

```python
>>> r = db.sort(db.getallkeys(), 'name')
>>> db.getmany(r)
[{'name': 'Ana', 'age': 10}, {'name': 'Beatriz', 'age': 30}, {'name': 'John Doe', 'age': 18}]

>>> r = db.find('name ?= "john"')
>>> db.getmany(r)
[{'name': 'John Doe', 'age': 18}]

>>> query = 'name == "john doe" or name == "ana" and age >= 10'
>>> r = db.find(query)
>>> db.getmany(r)
[{'name': 'John Doe', 'age': 18}, {'name': 'Ana', 'age': 10}]

>>> r = db.find('age < 40', sortby='age')
>>> db.getmany(r)
[{'name': 'Ana', 'age': 10}, {'name': 'John Doe', 'age': 18}, {'name': 'Beatriz', 'age': 30}]
```

Save the database to disk:

```python
>>> db.save()
True
```

To save a prettified json, use indent:

```python
>>> db.save(indent=4)
True
```

Enable auto saving to disk after a insert, update or delete:

```python
>>> db = dbj('mydb.json', autosave=True)
```

## About the simple query language

The query for the find command uses the following pattern:

*field operator value and/or field operator value...*

**Spaces are mandatory** and used as a separator by the parser. For example,
the following query **will not work**:

```text
name=="John" and age >=18
```

**A valid example**:

```text
name == "John Doe" and age >= 18
```

Strings must be enclosed by quotes. Quoted text can be searched using double
quotes as the string delimiter, like:

```text
name == ""Bob "B" Lee""
```

Please note that if value is a string, a search for text will be executed
(using the string operators below) and if value is a number, a number comparison
search will be used.

The supported string operators are:

```text
'==' -> Exact match. 'John' will not match 'John Doe' but will match 'john'
by default. If case sensitive is desired, just use find with sens=True. See
available commands below for the full find method signature.

'?=' -> Partial match. In this case, 'John' will match 'John Doe'.

'!=' -> Not equal operator.
```

The numbers comparison operators are:

```text
'==', '!=', '<', '<=', '>', '>='
```

The supported logical operatos are:

```text
and, or
```

## Important changes

0.1.4:
------

* The insert() method will raise a TypeError exception if the document dict is not json serializable.

## Performance

Since the entire database is a dict in memory, performance is pretty
good, it can handle dozens of thousands operations per second.

A simple benchmark is included to get a roughly estimative of operations per
second. Here is the result running on my personal machine (Ryzen 5 1600)
using Ubuntu 22 (via Windows WSL2) on Python 3.11:

```text
$ python3.11 bench_dbj.py

--------------------------------

Inserting 100000 documents using auto generated uuid1 key...
Done! Time spent: 0.50s
Inserted: 100000
Rate: 199738 ops/s

--------------------------------

Clearing the database...
Done!

--------------------------------

Inserting 100000 documents using a supplied key...
Done! Time spent: 0.24s
Inserted: 100000
Rate: 419375 ops/s

--------------------------------

Retrieving 100000 documents one at a time...
Done! Time spent: 0.02s
Retrieved: 100000
Rate: 6307774 ops/s

--------------------------------

Saving database to disk...
Done! Time spent: 0.20s

--------------------------------

Deleting 100000 documents one at a time...
Done! Time spent: 0.03s
Deleted: 100000
Rate: 3827445 ops/s

--------------------------------

Removing file...
Done!

Peak memory usage: 45.36 MB
```

## Available commands

```text
insert(document, key=None) -> Create a new document on database.
    Args:
        | document (dict): The document to be created.
        | key (str, optional): The document unique key. Defaults to uuid1.
    Returns:
        The document key.

insertmany(documents) -> Insert multiple documents on database.
    Args:
        documents (list): List containing the documents to insert.
    Returns:
        Number of inserted documents.

save(indent=None) -> Save database to disk.
    Args:
        indent (int or str, optional): If provided, save a prettified json with that indent level. 0, negative or "" will only insert newlines.
    Returns:
        True if successful.

clear() -> Remove all documents from database.
    Returns:
        True if successful.

size() -> Return the database size.
    Returns:
        Number of documents on database.

exists(key) -> Check if a document exists on database.
    Args:
        key (str): The document key.
    Returns:
        True or False if it does not exist.

delete(key) -> Delete a document on database.
    Args:
        key (str): The document key.
    Returns:
        True or False if it does not exist.

deletemany(keys) -> Delete multiple documents on database.
    Args:
        keys (list): List containing the keys of the documents to delete.
    Returns:
        Number of deleted documents.

update(key, values) -> Add/update values on a document.
    Args:
        | key (str): The document key.
        | values (dict): The values to be added/updated.
    Returns:
        True or False if document does not exist.

updatemany(keys, values) -> Add/update values on multiple documents.
    Args:
        | keys (list): List containing the keys of the documents to update.
        | values (dict): The values to be added/updated.
    Returns:
        Number of updated documents.

get(key) -> Get a document on database.
    Args:
        key (str): The document key.
    Returns:
        The document or False if it does not exist.

getmany(keys) -> Get multiple documents from database.
    Args:
        keys (list): List containing the keys of the documents to retrieve.
    Returns:
        List of documents.

getall() -> Return a list containing all documents on database.
    Returns:
        List with all database documents.

getallkeys() -> Return a list containing all keys on database.
    Returns:
        List with all database keys.

getrandom() -> Get a random document on database.
    Returns:
        A document or False if database is empty.

getfirst() -> Get the first inserted document on database.
    Returns:
        The first inserted document or False if database is empty.

getlast() -> Get the last inserted document on database.
    Returns:
        The last inserted document or False if database is empty.

getfirstkey() -> Get the first key on database.
    Returns:
        The first key or False if database is empty.

getlastkey() -> Get the last key on database.
    Returns:
        The last key or False if database is empty.

pop(key) -> Get the document from database and remove it.
    Args:
        key (str): The document key.
    Returns:
        The document or False if it does not exist.

popfirst() -> Get the first inserted document on database and remove it.
    Returns:
        The first inserted document or False if database is empty.

poplast() -> Get the last inserted document on database and remove it.
    Returns:
        The last inserted document or False if database is empty.

sort(keys, field, reverse=False) -> Sort the documents using the field provided.
    Args:
        | keys (list): List containing the keys of the documents to sort.
        | field (str): Field to sort.
        | reverse (bool, optional): Reverse search. Defaults to False.
    Returns:
        Sorted list with the documents keys.

findtext(field, text, exact=False, sens=False, inverse=False, asc=True) -> Simple text search on the provided field.
    Args:
        | field (str): The field to search.
        | text (str): The value to be searched.
        | exact (bool, optional): Exact text match. Defaults to False.
        | sens (bool, optional): Case sensitive. Defaults to False.
        | inverse (bool, optional): Inverse search, return the documents that do not match the search. Defaults to False.
        | asc (bool, optional): Ascii conversion before matching, this matches text like 'cafe' and 'café'. Defaults to True.
    Returns:
        List with the keys of the documents that matched the search.

findnum(expression) -> Simple number comparison search on provided field.
    Args:
        | expression (str): The comparison expression to use, e.g., "age >= 18". The pattern is 'field operator number'.
    Returns:
        List with the keys of the documents that matched the search.

find(query, sens=False, asc=True, sortby=None, reverse=False) -> Simple query like search.
    Args:
        | query (str): The query to use.
        | sens (bool, optional): Case sensitive. Defaults to False.
        | asc (bool, optional): Ascii conversion before matching, this matches text like 'cafe' and 'café'. Defaults to True.
        | sortby (string, optional): Sort using the provided field.
        | reverse (bool, optional): Reverse sort. Defaults to False.
    Returns:
        List with the keys of the documents that matched the search.
```
