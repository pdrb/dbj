# -*- coding: utf-8 -*-

import unittest
import os

from dbj import dbj


class testdbj(unittest.TestCase):
    def setUp(self):
        self.db = dbj('tests_dbj.db')

    def tearDown(self):
        self.db.clear()
        self.db.save()

    @classmethod
    def tearDownClass(cls):
        os.remove('tests_dbj.db')

    def test_load(self):
        self.assertEqual(self.db.size(), 0)
        self.db.insert({'test': 'testing'})
        self.db.save()
        self.db.clear()
        self.assertEqual(self.db.size(), 0)
        self.db.load()
        self.assertEqual(self.db.size(), 1)

    def test_save(self):
        self.db.insert({'test': 'testing'})
        self.assertTrue(self.db.save())

    def test_insert(self):
        with self.assertRaises(TypeError):
            self.db.insert('test')
        with self.assertRaises(TypeError):
            self.db.insert({'test': 'test'}, 1)
        with self.assertRaises(TypeError):
            self.db.insert({1: 'test'})
        with self.assertRaises(TypeError):
            self.db.insert({})
        self.assertEqual(self.db.insert({'test': 'testing'}, '1'), '1')
        self.db.insert({'test2': 'testing2'})
        self.assertEqual(self.db.size(), 2)

    def test_insertmany(self):
        with self.assertRaises(TypeError):
            self.db.insertmany({})
        with self.assertRaises(TypeError):
            self.db.insertmany([{'test': 'testing'}, 'testing'])
        docs = [
            {'test': 'testing'}, {'test2': 'testing2'}, {'test3': 'testing3'}
        ]
        self.assertEqual(self.db.insertmany(docs), 3)
        self.assertEqual(self.db.size(), 3)

    def test_get(self):
        doc = {'test': 'testing'}
        self.db.insert(doc, '1000')
        with self.assertRaises(TypeError):
            self.db.get(1000)
        self.assertFalse(self.db.get('1'))
        self.assertEqual(self.db.get('1000'), doc)

    def test_getmany(self):
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        with self.assertRaises(TypeError):
            self.db.getmany('1, 2')
        self.assertEqual(self.db.getmany(['1', '2', '3']), docs)

    def test_getall(self):
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertEqual(self.db.getall(), docs)

    def test_getallkeys(self):
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.assertEqual(self.db.getallkeys(), ['1', '2'])

    def test_getrandom(self):
        self.assertFalse(self.db.getrandom())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertIn(
            self.db.getrandom(), [{'test': 'testing'}, {'test2': 'testing2'}]
        )

    def test_getfirst(self):
        self.assertFalse(self.db.getfirst())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertEqual(self.db.getfirst(), docs[0])

    def test_getlast(self):
        self.assertFalse(self.db.getlast())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertEqual(self.db.getlast(), docs[-1])

    def test_getfirstkey(self):
        self.assertFalse(self.db.getfirstkey())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.assertEqual(self.db.getfirstkey(), '1')

    def test_getlastkey(self):
        self.assertFalse(self.db.getlastkey())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.assertEqual(self.db.getlastkey(), '2')

    def test_pop(self):
        with self.assertRaises(TypeError):
            self.db.pop(1)
        doc = {'test': 'testing'}
        self.db.insert(doc, '1')
        self.assertFalse(self.db.pop('2'))
        self.assertEqual(self.db.pop('1'), doc)
        self.assertEqual(self.db.size(), 0)

    def test_popfirst(self):
        self.assertFalse(self.db.popfirst())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertEqual(self.db.popfirst(), docs[0])
        self.assertEqual(self.db.size(), 1)

    def test_poplast(self):
        self.assertFalse(self.db.poplast())
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0])
        self.db.insert(docs[1])
        self.assertEqual(self.db.poplast(), docs[1])
        self.assertEqual(self.db.size(), 1)

    def test_delete(self):
        with self.assertRaises(TypeError):
            self.db.delete(1)
        self.db.insert({'test': 'testing'}, '1')
        self.assertFalse(self.db.delete('2'))
        self.assertTrue(self.db.delete('1'))
        self.assertEqual(self.db.size(), 0)

    def test_deletemany(self):
        with self.assertRaises(TypeError):
            self.db.deletemany('1, 2')
        docs = [{'test': 'testing'}, {'test2': 'testing2'}]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.assertEqual(self.db.deletemany(['1', '2', '3']), 2)
        self.assertEqual(self.db.size(), 0)

    def test_clear(self):
        self.db.insert({'test': 'testing'})
        self.assertEqual(self.db.size(), 1)
        self.db.clear()
        self.assertEqual(self.db.size(), 0)

    def test_size(self):
        self.db.insert({'test': 'testing'})
        self.db.insert({'test2': 'testing2'})
        self.assertEqual(self.db.size(), 2)

    def test_exists(self):
        with self.assertRaises(TypeError):
            self.db.exists(1)
        self.db.insert({'test': 'testing'}, '1')
        self.assertFalse(self.db.exists('2'))
        self.assertTrue(self.db.exists('1'))

    def test_update(self):
        with self.assertRaises(TypeError):
            self.db.update('1', 'test')
        with self.assertRaises(TypeError):
            self.db.update(1, {'test': 'testing'})
        self.db.insert({'test': 'testing'}, '1')
        self.assertFalse(self.db.update('2', {'test': 'testing'}))
        values = {'test': 'test update', 'new': 'new field'}
        self.assertTrue(self.db.update('1', values))
        doc = self.db.get('1')
        self.assertEqual(doc['test'], 'test update')
        self.assertEqual(doc['new'], 'new field')

    def test_updatemany(self):
        with self.assertRaises(TypeError):
            self.db.updatemany('1', 'test')
        with self.assertRaises(TypeError):
            self.db.updatemany('1, 2', {'test': 'testing'})
        self.db.insert({'test': 'testing'}, '1')
        self.db.insert({'test2': 'testing2'}, '2')
        values = {'new': 'new field'}
        self.assertEqual(self.db.updatemany(['1', '2', '3'], values), 2)

    def test_sort(self):
        with self.assertRaises(TypeError):
            self.db.sort('1, 2', 'test')
        with self.assertRaises(TypeError):
            self.db.sort(['1', '2'], 1)
        docs = [
            {'name': 'Ana', 'age': 18},
            {'name': 'Bia', 'age': 10},
            {'name': 'John', 'age': 30},
            {'name': 'Baby', 'age': 1},
            {'country': 'Brasil'}
        ]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.db.insert(docs[2], '3')
        self.db.insert(docs[3], '4')
        self.db.insert(docs[4], '5')
        keys = self.db.getallkeys()
        self.assertEqual(self.db.sort(keys, 'name'), ['1', '4', '2', '3'])
        self.assertEqual(self.db.sort(
            keys, 'name', reverse=True), ['3', '2', '4', '1']
        )
        self.assertEqual(self.db.sort(keys, 'age'), ['4', '2', '1', '3'])
        self.assertEqual(self.db.sort(
            keys, 'age', reverse=True), ['3', '1', '2', '4']
        )

    def test_findtext(self):
        with self.assertRaises(TypeError):
            self.db.findtext(1, 'test')
        with self.assertRaises(TypeError):
            self.db.findtext('1', 1)
        with self.assertRaises(TypeError):
            self.db.findtext('1', 'test', exact='1')
        with self.assertRaises(TypeError):
            self.db.findtext('1', 'test', sens='1')
        with self.assertRaises(TypeError):
            self.db.findtext('1', 'test', inverse='1')
        with self.assertRaises(TypeError):
            self.db.findtext('1', 'test', ascii='0')
        self.db.insert({'name': 'André'}, '1')
        self.db.insert({'name': 'andre silva'}, '2')
        self.db.insert({'country': 'Brasil'}, '3')
        self.db.insert({'name': 30}, '4')
        self.assertEqual(self.db.findtext('name', 'andre'), ['1', '2'])
        self.assertEqual(self.db.findtext('name', 'andre', exact=True), ['1'])
        self.assertEqual(self.db.findtext('name', 'andre', sens=True), ['2'])
        self.assertEqual(self.db.findtext('name', 'andre', inverse=True), [])
        self.assertEqual(self.db.findtext('name', 'andré', asc=False), ['1'])
        self.assertEqual(
            self.db.findtext('name', 'André', exact=True, sens=True), ['1']
        )

    def test_findnum(self):
        with self.assertRaises(TypeError):
            self.db.findnum(10)
        with self.assertRaises(TypeError):
            self.db.findnum('age< 18')
        with self.assertRaises(TypeError):
            self.db.findnum('age ~ 18')
        with self.assertRaises(TypeError):
            self.db.findnum('age < 2a')
        self.db.insert({'age': '18'}, '1')
        self.db.insert({'age': 10}, '2')
        self.assertEqual(self.db.findnum('age == 18'), ['1'])
        self.assertEqual(self.db.findnum('age != 18'), ['2'])
        self.assertEqual(self.db.findnum('age < 18'), ['2'])
        self.assertEqual(self.db.findnum('age <= 18'), ['1', '2'])
        self.assertEqual(self.db.findnum('age > 18'), [])
        self.assertEqual(self.db.findnum('age >= 18'), ['1'])
        self.assertEqual(self.db.findnum('salary == 10000'), [])
        self.assertEqual(self.db.findnum('age > 10'), ['1'])

    def test_find(self):
        with self.assertRaises(TypeError):
            self.db.find(10)
        with self.assertRaises(TypeError):
            self.db.find('name== "Ana"')
        with self.assertRaises(TypeError):
            self.db.find('name == "Ana" and age')
        with self.assertRaises(TypeError):
            self.db.find('name == "Ana" not age < 18')
        with self.assertRaises(TypeError):
            self.db.find('name == "Ana" and')
        with self.assertRaises(TypeError):
            self.db.find('name = "Ana"')
        docs = [
            {'name': 'André', 'age': 10},
            {'name': 'andre silva', 'age': '18'},
            {'name': 'Bob "B" Lee', 'age': '30'}
        ]
        self.db.insert(docs[0], '1')
        self.db.insert(docs[1], '2')
        self.db.insert(docs[2], '3')
        query = 'age > 30'
        self.assertEqual(self.db.find(query), [])
        query = 'name == "andre"'
        self.assertEqual(self.db.find(query), ['1'])
        query = 'name == "andre" or name ?= "bob"'
        r = self.db.find(query)
        r.sort()
        self.assertEqual(r, ['1', '3'])
        query = 'name != "andre" and age >= 30'
        self.assertEqual(self.db.find(query), ['3'])
        query = 'name ?= "andre"'
        r = self.db.find(query)
        r.sort()
        self.assertEqual(r, ['1', '2'])
        query = 'age >= 18 and name ?= "andré"'
        self.assertEqual(self.db.find(query, sens=True), ['2'])
        query = 'name ?= "andré"'
        self.assertEqual(self.db.find(query, asc=False), ['1'])
        query = 'name ?= ""Bob "B""" and age >= 30'
        self.assertEqual(self.db.find(query), ['3'])
        query = 'name == "andre" or name ?= "bob" and age > 18'
        self.assertEqual(self.db.find(query), ['3'])
        query = 'name == "andre" or name == "ana" or name == "bob"'
        self.assertEqual(self.db.find(query), ['1'])

    def test__parse_query(self):
        query = 'age <= 18'
        parsed = ['age', '<=', '18']
        self.assertEqual(self.db._parse_query(query), parsed)
        query = 'name == "bob silva" and age > 10'
        parsed = ['name', '==', '"bob silva"', 'and', 'age', '>', '10']
        self.assertEqual(self.db._parse_query(query), parsed)
        query = 'name == ""john j"" or name == "bob"'
        parsed = ['name', '==', '""john j""', 'or', 'name', '==', '"bob"']
        self.assertEqual(self.db._parse_query(query), parsed)
        query = 'name == "John John" or name == ""Bob "B" Lee"" and age >= 18'
        parsed = [
            'name', '==', '"John John"', 'or', 'name', '==', '""Bob "B" Lee""',
            'and', 'age', '>=', '18'
        ]
        self.assertEqual(self.db._parse_query(query), parsed)

    def test__isstr(self):
        self.assertFalse(self.db._isstr(1))
        self.assertTrue(self.db._isstr('1'))

    def test__autosave(self):
        self.db = dbj('tests_dbj.db', autosave=True)
        self.db.insert({'test': 'testing'})
        self.db.insert({'test2': 'testing2'})
        self.db = dbj('tests_dbj.db')
        self.assertEqual(self.db.size(), 2)


if __name__ == '__main__':
    unittest.main()
