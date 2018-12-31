import os
import timeit
import resource

from dbj import dbj


db = dbj('bench_database.json')
n = 100000


def insert_auto():
    for i in range(n):
        db.insert({'index': i})


def insert_sup():
    for i in range(n):
        db.insert({'index': i}, str(i))


def retrieve_all():
    for key in db.getallkeys():
        db.get(key)


def delete_all():
    for key in db.getallkeys():
        db.delete(key)


print('\n' + '-' * 32)
print('\nInserting {} documents using auto generated uuid1 key...'.format(n))
spent_time = timeit.timeit(insert_auto, number=1)
print('Done! Time spent: {:.2f}s\nInserted: {}\nRate: {} ops/s'.format(
    spent_time, db.size(), int(db.size()/spent_time)))

print('\n' + '-' * 32)
print('\nClearing the database...')
db.clear()
print('Done!')

print('\n' + '-' * 32)
print('\nInserting {} documents using a supplied key...'.format(n))
spent_time = timeit.timeit(insert_sup, number=1)
print('Done! Time spent: {:.2f}s\nInserted: {}\nRate: {} ops/s'.format(
    spent_time, db.size(), int(db.size()/spent_time)))

print('\n' + '-' * 32)
print('\nRetrieving {} documents one at a time...'.format(db.size()))
spent_time = timeit.timeit(retrieve_all, number=1)
print('Done! Time spent: {:.2f}s\nRetrieved: {}\nRate: {} ops/s'.format(
    spent_time, db.size(), int(db.size()/spent_time)))

print('\n' + '-' * 32)
print('\nSaving database to disk...')
spent_time = timeit.timeit(db.save, number=1)
print('Done! Time spent: {:.2f}s'.format(spent_time))

print('\n' + '-' * 32)
print('\nDeleting {} documents one at a time...'.format(db.size()))
spent_time = timeit.timeit(delete_all, number=1)
print('Done! Time spent: {:.2f}s\nDeleted: {}\nRate: {} ops/s'.format(
    spent_time, n, int(n/spent_time)))

print('\n' + '-' * 32)
print('\nRemoving file...')
os.remove('bench_database.json')
used_mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
print('Done!\n\nPeak memory usage: {:.2f} MB\n'.format(used_mem/1024.0))
