# -*- coding: utf-8 -*-

# dbj 0.1.9
# simple embedded in memory json database
# author: Pedro Buteri Gonring
# email: pedro@bigode.net
# date: 2020-05-20

import json
import uuid
import signal
import random
import unicodedata
import sys
import os

# This is necessary for Python 2.7-3.5, since Python 3.6+ dicts are ordered
from collections import OrderedDict


class KillProtected(object):
    '''Protect using 'with' statement from common kill signals'''
    def __init__(self):
        self.killed = False

    def kill_handler(self, signum, frame):
        self.killed = True

    # The signal.signal() returns the previous handler
    def __enter__(self):
        self.prev_sigint = signal.signal(signal.SIGINT, self.kill_handler)
        self.prev_sigterm = signal.signal(signal.SIGTERM, self.kill_handler)

    def __exit__(self, type, value, traceback):
        if self.killed:
            sys.exit(0)
        signal.signal(signal.SIGINT, self.prev_sigint)
        signal.signal(signal.SIGTERM, self.prev_sigterm)


class dbj(object):
    '''Documentation on "https://github.com/pdrb/dbj"'''
    document_type_error = TypeError('document must be dict')
    key_type_error = TypeError('document key must be string')
    keys_type_error = TypeError('keys must be a list')

    def __init__(self, path, autosave=False):
        self.path = path
        self.autosave = autosave
        self.load()

    def load(self):
        '''Load the database or create a new one if the file does not exist.'''
        if os.path.exists(self.path):
            with open(self.path, 'rt') as f:
                db_data = json.load(f, object_pairs_hook=OrderedDict)
        else:
            db_data = OrderedDict()
        self.db = db_data

    def save(self, indent=None):
        '''Save database to disk protecting from kill signals.

        Args:
            indent (int or str, optional): If provided, save a prettified json
                with that indent level. 0, negative or "" will only insert
                newlines.

        Returns:
            True if saved successful.
        '''
        with open(self.path, 'wt') as f:
            with KillProtected():
                json.dump(self.db, f, indent=indent)
        return True

    def insert(self, document, key=None):
        '''Create a new document on database.

        Args:
            document (dict): The document to be created.
            key (str, optional): The document unique key. Defaults to uuid1.

        Returns:
            The document key.

        Raises:
            TypeError: If document is not dict, document is empty, the optional
                key is not str, document field (dict key) is not str or
                document is not json serializable.
        '''
        if not isinstance(document, dict):
            raise self.document_type_error
        if not document:
            raise TypeError('document must not be empty')
        if key is not None and not self._isstr(key):
            raise self.key_type_error
        if key is None:
            key = uuid.uuid1().hex
        for field in document:
            if not self._isstr(field):
                raise TypeError('document field (dict key) must be string')
        if not self._is_serializable(document):
            raise TypeError('document is not json serializable')
        self.db[key] = document
        self._autosave()
        return key

    def insertmany(self, documents):
        '''Insert multiple documents on database.

        The documents list will be validated before the insertion, so all the
        documents will be inserted or none.

        Args:
            documents (list): List containing the documents to insert.

        Returns:
            Number of inserted documents.

        Raises:
            TypeError: If keys is not a list or a document is not dict.
        '''
        if not isinstance(documents, list):
            raise TypeError('documents must be a list')
        for doc in documents:
            if not isinstance(doc, dict):
                raise TypeError('invalid dict: "{}"'.format(doc))
        for doc in documents:
            self.insert(doc)
        return len(documents)

    def get(self, key):
        '''Get a document on database.

        Args:
            key (str): The document key.

        Returns:
            The document or False if it does not exist.

        Raises:
            TypeError: If key is not str.
        '''
        if not self._isstr(key):
            raise self.key_type_error
        try:
            # Convert OrderedDict (even nested) to dict so the output is better
            return json.loads(json.dumps(self.db[key]))
        except KeyError:
            return False

    def getmany(self, keys):
        '''Get multiple documents from database.

        Args:
            keys (list): List containing the keys of the documents to retrieve.

        Returns:
            List of documents.

        Raises:
            TypeError: If keys is not a list.
        '''
        if not isinstance(keys, list):
            raise self.keys_type_error
        docs_list = []
        for key in keys:
            doc = self.get(key)
            if not doc:
                continue
            docs_list.append(doc)
        return docs_list

    def getall(self):
        '''Return a list containing all documents on database.'''
        return self.getmany(self.getallkeys())

    def getallkeys(self):
        '''Return a list containing all keys on database.'''
        return list(self.db.keys())

    def getrandom(self):
        '''Get a random document on database.

        Returns:
            A document or False if database is empty.
        '''
        try:
            key = random.choice(self.getallkeys())
        except IndexError:
            return False
        return self.get(key)

    def getfirst(self):
        '''Get the first inserted document on database.

        Returns:
            The first inserted document or False if database is empty.
        '''
        first_doc_key = self.getfirstkey()
        if not first_doc_key:
            return False
        return self.get(first_doc_key)

    def getlast(self):
        '''Get the last inserted document on database.

        Returns:
            The last inserted document or False if database is empty.
        '''
        last_doc_key = self.getlastkey()
        if not last_doc_key:
            return False
        return self.get(last_doc_key)

    def getfirstkey(self):
        '''Get the first key on database.

        Returns:
            The first key or False if database is empty.
        '''
        try:
            key = next(iter(self.db))
        except StopIteration:
            return False
        return key

    def getlastkey(self):
        '''Get the last key on database.

        Returns:
            The last key or False if database is empty.
        '''
        try:
            key = next(reversed(self.db))
        except StopIteration:
            return False
        return key

    def pop(self, key):
        '''Get the document from database and remove it.

        Args:
            key (str): The document key.

        Returns:
            The document or False if it does not exist.

        Raises:
            TypeError: If key is not str.
        '''
        if not self._isstr(key):
            raise self.key_type_error
        document = self.get(key)
        if not document:
            return False
        self.delete(key)
        return document

    def popfirst(self):
        '''Get the first inserted document on database and remove it.

        Returns:
            The first inserted document or False if database is empty.
        '''
        document = self.getfirst()
        if not document:
            return False
        self.delete(self.getfirstkey())
        return document

    def poplast(self):
        '''Get the last inserted document on database and remove it.

        Returns:
            The last inserted document or False if database is empty.
        '''
        document = self.getlast()
        if not document:
            return False
        self.delete(self.getlastkey())
        return document

    def delete(self, key):
        '''Delete a document on database.

        Args:
            key (str): The document key.

        Returns:
            True or False if it does not exist.

        Raises:
            TypeError: If key is not str.
        '''
        if not self._isstr(key):
            raise self.key_type_error
        try:
            del(self.db[key])
        except KeyError:
            return False
        self._autosave()
        return True

    def deletemany(self, keys):
        '''Delete multiple documents on database.

        Args:
            keys (list): List containing the keys of the documents to delete.

        Returns:
            Number of deleted documents.

        Raises:
            TypeError: If keys is not a list.
        '''
        if not isinstance(keys, list):
            raise self.keys_type_error
        deleted = 0
        for key in keys:
            if not self.delete(key):
                continue
            deleted += 1
        return deleted

    def clear(self):
        '''Remove all documents from database.'''
        self.db.clear()
        self._autosave()
        return True

    def size(self):
        '''Return the number of documents on database.'''
        return len(self.db.keys())

    def exists(self, key):
        '''Check if a document exists on database.

        Args:
            key (str): The document key.

        Returns:
            True or False if it does not exist.

        Raises:
            TypeError: If key is not str.
        '''
        if not self._isstr(key):
            raise self.key_type_error
        if key in self.db:
            return True
        return False

    def update(self, key, values):
        '''Add/update values on a document.

        Args:
            key (str): The document key.
            values (dict): The values to be added/updated.

        Returns:
            True or False if document does not exist.

        Raises:
            TypeError: If values is not dict or key is not str.
        '''
        if not isinstance(values, dict):
            raise self.document_type_error
        if not self._isstr(key):
            raise self.key_type_error
        document = self.get(key)
        if not document:
            return False
        document.update(values)
        self.insert(document, key)
        return True

    def updatemany(self, keys, values):
        '''Add/update values on multiple documents.

        Args:
            keys (list): List containing the keys of the documents to update.
            values (dict): The values to be added/updated.

        Returns:
            Number of updated documents.

        Raises:
            TypeError: If keys is not a list or values is not dict.
        '''
        if not isinstance(values, dict):
            raise self.document_type_error
        if not isinstance(keys, list):
            raise self.keys_type_error
        updated = 0
        for key in keys:
            if not self.update(key, values):
                continue
            updated += 1
        return updated

    def sort(self, keys, field, reverse=False):
        '''Sort the documents using the field provided.

        Args:
            keys (list): List containing the keys of the documents to sort.
            field (str): Field to sort.
            reverse (bool, optional): Reverse sort. Defaults to False.

        Returns:
            Sorted list with the documents keys.

        Raises:
            TypeError: If keys is not a list or field is not string.
        '''
        if not isinstance(keys, list):
            raise self.keys_type_error
        if not self._isstr(field):
            raise TypeError('field must be string')
        sorted_list = []
        for key in keys:
            try:
                sorted_list.append((self.db[key][field], key))
            except KeyError:
                pass
        sorted_list.sort(reverse=reverse)
        sorted_keys = [elem[1] for elem in sorted_list]
        return sorted_keys

    def findtext(self, field, text, exact=False, sens=False, inverse=False,
                 asc=True):
        '''Simple text search on the provided field.

        Args:
            field (str): The field to search.
            text (str): The value to be searched.
            exact (bool, optional): Exact text match. Defaults to False.
            sens (bool, optional): Case sensitive. Defaults to False.
            inverse (bool, optional): Inverse search, return the documents that
                do not match the search. Defaults to False.
            asc (bool, optional): Ascii conversion before matching, this
                matches text like 'cafe' and 'café'. Defaults to True.

        Returns:
            List with the keys of the documents that matched the search.

        Raises:
            TypeError: If field is not str, text is not str, exact is not
                bool, sens is not bool, inverse is not bool or asc is not bool.
        '''
        if not self._isstr(field) or not self._isstr(text):
            raise TypeError('field and text must be string')
        if not isinstance(exact, bool) or not isinstance(sens, bool) or \
                not isinstance(inverse, bool) or not isinstance(asc, bool):
            raise TypeError('exact, sens, inverse and asc must be boolean')
        match_list = []
        not_match_list = []
        for doc_key in self.db.keys():
            try:
                field_value = self.db[doc_key][field]
            except KeyError:
                continue
            if not isinstance(field_value, str):
                continue
            if asc:
                # Python 2.7 compatibility code
                if sys.version_info[0:2] == (2, 7):
                    fv_nfkd = unicodedata.normalize(
                        'NFKD', unicode(field_value.decode('utf-8'))
                    )
                    field_value = fv_nfkd.encode('ASCII', 'ignore').decode()
                    text_nfkd = unicodedata.normalize(
                        'NFKD', unicode(text.decode('utf-8'))
                    )
                    text = text_nfkd.encode('ASCII', 'ignore').decode()
                else:
                    fv_nfkd = unicodedata.normalize('NFKD', field_value)
                    field_value = fv_nfkd.encode('ASCII', 'ignore').decode()
                    text_nfkd = unicodedata.normalize('NFKD', text)
                    text = text_nfkd.encode('ASCII', 'ignore').decode()
            if not exact and not sens:
                if text.lower() in field_value.lower():
                    match_list.append(doc_key)
                else:
                    not_match_list.append(doc_key)
            elif exact and not sens:
                if text.lower() == field_value.lower():
                    match_list.append(doc_key)
                else:
                    not_match_list.append(doc_key)
            elif not exact and sens:
                if text in field_value:
                    match_list.append(doc_key)
                else:
                    not_match_list.append(doc_key)
            else:
                if text == field_value:
                    match_list.append(doc_key)
                else:
                    not_match_list.append(doc_key)
        if inverse:
            return not_match_list
        return match_list

    def findnum(self, expression):
        '''Simple number comparison search on provided field.

        Args:
            expression (str): The comparison expression to use, e.g.,
                "age >= 18". The pattern is 'field operator number'.

        Returns:
            List with the keys of the documents that matched the search.

        Raises:
            TypeError: If expression is invalid.
        '''
        if not self._isstr(expression):
            raise TypeError('expression must be string')
        operators = ('==', '!=', '<', '<=', '>', '>=')
        tokens = expression.split(' ')
        if len(tokens) != 3:
            raise TypeError('invalid expression: "{}"'.format(expression))
        field = tokens[0]
        operator = tokens[1]
        if operator not in operators:
            raise TypeError('invalid number operator: "{}"'.format(operator))
        try:
            number = float(tokens[2])
        except ValueError:
            raise TypeError('invalid number: "{}"'.format(tokens[2]))
        match_list = []
        for doc_key in self.db.keys():
            try:
                field_value = float(self.db[doc_key][field])
            except (KeyError, ValueError):
                continue
            if operator == '==':
                if field_value == number:
                    match_list.append(doc_key)
            elif operator == '!=':
                if field_value != number:
                    match_list.append(doc_key)
            elif operator == '<':
                if field_value < number:
                    match_list.append(doc_key)
            elif operator == '<=':
                if field_value <= number:
                    match_list.append(doc_key)
            elif operator == '>':
                if field_value > number:
                    match_list.append(doc_key)
            elif operator == '>=':
                if field_value >= number:
                    match_list.append(doc_key)
        return match_list

    def find(self, query, sens=False, asc=True, sortby=None, reverse=False):
        '''Simple query like search.

        Args:
            query (str): The query to use, examples:
                1. age >= 18
                2. description ?= "dbj is a"
                3. name != "John" and age < 18
                4. name == "Ana" or name == ""Bob "B" Lee"" and age >= 30
                The pattern is:
                    'field operator value and/or field operator value...'
            sens (bool, optional): Case sensitive. Defaults to False.
            asc (bool, optional): Ascii conversion before matching, this
                matches text like 'cafe' and 'café'. Defaults to True.
            sortby (string, optional): Sort using the provided field.
            reverse (bool, optional): Reverse sort. Defaults to False.

        Returns:
            List with the keys of the documents that matched the search.

        Raises:
            TypeError: If query is invalid or sortby is not a string.
        '''
        if not self._isstr(query):
            raise TypeError('query must be string')
        if sortby is not None and not self._isstr(sortby):
            raise TypeError('sortby must be string')
        tokens = self._parse_query(query)
        if len(tokens) < 3:
            raise TypeError('invalid query: "{}"'.format(query))
        ops = []
        lops = []
        sets = []
        for i in range(0, len(tokens), 4):
            try:
                ops.append(tokens[i])
                ops.append(tokens[i+1])
                ops.append(tokens[i+2])
                lops.append(tokens[i+3])
            except IndexError:
                pass
        if len(ops) % 3 != 0:
            raise TypeError('invalid query: "{}"'.format(query))
        for lop in lops:
            if lop.lower() not in ('and', 'or'):
                raise TypeError('invalid logical operator: "{}"'.format(lop))
        if len(lops) > 0 and len(ops) / 3 != len(lops) + 1:
            raise TypeError('invalid query: "{}"'.format(query))
        for i in range(0, len(ops), 3):
            field = ops[i]
            operator = ops[i+1]
            value = ops[i+2]
            if value[0] == '"':
                if value[:2] == '""':
                    value = value[2:-2]
                else:
                    value = value[1:-1]
                if operator == '==':
                    result = self.findtext(
                        field, value, sens=sens, asc=asc, exact=True
                    )
                elif operator == '!=':
                    result = self.findtext(
                        field, value, sens=sens, asc=asc, inverse=True
                    )
                elif operator == '?=':
                    result = self.findtext(
                        field, value, sens=sens, asc=asc
                    )
                else:
                    raise TypeError(
                        'invalid string operator: "{}"'.format(operator)
                    )
            else:
                result = self.findnum(
                    '{} {} {}'.format(field, operator, value)
                )
            sets.append(set(result))
        for i in range(len(lops)):
            if i == 0:
                if lops[i] == 'and':
                    result = sets[i] & sets[i+1]
                elif lops[i] == 'or':
                    result = sets[i] | sets[i+1]
            else:
                if lops[i] == 'and':
                    result = result & sets[i+1]
                elif lops[i] == 'or':
                    result = result | sets[i+1]
        if sortby is not None:
            result = self.sort(list(result), sortby, reverse=reverse)
        return list(result)

    def _parse_query(self, query):
        '''Parse the query string and return a tokens list.'''
        tokens = query.split(' ')
        parsed_tokens = []
        string_open = False
        value_str = ''
        string_delimiter = '"'
        i = 0
        while i < len(tokens):
            if tokens[i][:2] == '""':
                string_delimiter = '""'
            if tokens[i][:len(string_delimiter)] == string_delimiter and \
                    tokens[i][-len(string_delimiter):] == string_delimiter:
                parsed_tokens.append(tokens[i])
                i += 1
            elif tokens[i][:len(string_delimiter)] == string_delimiter:
                string_open = True
                value_str = tokens[i] + ' '
                i += 1
            elif string_open:
                if tokens[i][-len(string_delimiter):] == string_delimiter:
                    string_open = False
                    value_str += tokens[i]
                    parsed_tokens.append(value_str)
                    value_str = ''
                    string_delimiter = '"'
                    i += 1
                else:
                    value_str += tokens[i] + ' '
                    i += 1
            else:
                parsed_tokens.append(tokens[i])
                i += 1
        return parsed_tokens

    def _isstr(self, string):
        '''Check string instance based on Python version'''
        if sys.version_info[0:2] == (2, 7):
            return isinstance(string, basestring)
        else:
            return isinstance(string, str)

    def _is_serializable(self, obj):
        '''Check if the object is json serializable'''
        try:
            json.dumps(obj)
        except (TypeError, OverflowError):
            return False
        return True

    def _autosave(self):
        '''Save if autosave is enabled'''
        if self.autosave:
            self.save()
