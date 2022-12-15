#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import threading


# static lock
class Account:
    def __init__(self, _id, balance):
        self.id = _id
        self.balance = balance
    def withdraw(self, amount):
        self.balance -= amount
    def deposit(self, amount):
        self.balance += amount


def transfera_b(_from, to, amount):
    lock_a.acquire()  # 锁住自己的账户
    time.sleep(1)  # 让交易时间变长，2个交易线程时间上重叠，有足够时间来产生死锁
    _from.withdraw(amount)
    print('wait for lock_b')
    lock_b.acquire()  # 锁住对方的账户
    to.deposit(amount)
    lock_b.release()
    lock_a.release()


def transferb_a(_from, to, amount):
    lock_b.acquire()  # 锁住自己的账户
    time.sleep(1)  # 让交易时间变长，2个交易线程时间上重叠，有足够时间来产生死锁
    _from.withdraw(amount)
    print('wait for lock_a')
    lock_a.acquire()  # 锁住对方的账户
    to.deposit(amount)
    lock_a.release()
    lock_b.release()

lock_a = threading.Lock()
lock_b = threading.Lock()
a = Account('a', 1000)
b = Account('b', 1000)
#a往b转账100
t1 = threading.Thread(target=transfera_b, args=(a, b, 100))
t1.start()
#b往a转账200
t2 = threading.Thread(target=transferb_a, args=(b, a, 200))
t2.start()
t1.join()
t2.join()
print("a的账户余额：",a.balance)
print("b的账户余额：",b.balance)


# solve lock
class Account:
    def __init__(self, _id, balance):
        self.id = _id
        self.balance = balance
    def withdraw(self, amount):
        self.balance -= amount
    def deposit(self, amount):
        self.balance += amount


def transfera_b(_from, to, amount):
    lock_a.acquire()  # 锁住自己的账户
    time.sleep(1)  # 让交易时间变长，2个交易线程时间上重叠，有足够时间来产生死锁
    _from.withdraw(amount)
    lock_b.acquire()  # 锁住对方的账户
    to.deposit(amount)
    lock_b.release()
    lock_a.release()


def transferb_a(_from, to, amount):
    lock_a.acquire()  # 锁住自己的账户
    time.sleep(1)  # 让交易时间变长，2个交易线程时间上重叠，有足够时间来产生死锁
    _from.withdraw(amount)
    lock_b.acquire()  # 锁住对方的账户
    to.deposit(amount)
    lock_b.release()
    lock_a.release()

lock_a = threading.Lock()
lock_b = threading.Lock()
a = Account('a', 1000)
b = Account('b', 1000)
#a往b转账100
t1 = threading.Thread(target=transfera_b, args=(a, b, 100))
t1.start()
#b往a转账200
t2 = threading.Thread(target=transferb_a, args=(b, a, 200))
t2.start()
t1.join()
t2.join()
print("a的账户余额：",a.balance)
print("b的账户余额：",b.balance)


# move lock
class Account:
    def __init__(self, _id, balance):
        self.id = _id
        self.balance = balance
        self.lock = threading.Lock()
    def withdraw(self, amount):
        self.balance -= amount
    def deposit(self, amount):
        self.balance += amount

def transfer(_from,to, amount):
    _from.lock.acquire()  # 锁住自己的账户
    time.sleep(1)  # 让交易时间变长，2个交易线程时间上重叠，有足够时间来产生死锁
    _from.withdraw(amount)
    print('wait for lock')
    to.lock.acquire()  # 锁住对方的账户
    to.deposit(amount)
    to.lock.release()
    _from.lock.release()

a = Account('a', 1000)
b = Account('b', 1000)
#a往b转账100
t1 = threading.Thread(target=transfer, args=(a, b, 100))
t1.start()
#b往a转账200
t2 = threading.Thread(target=transfer, args=(b, a, 200))
t2.start()
t1.join()
t2.join()
print("a的账户余额：",a.balance)
print("b的账户余额：",b.balance)

# slove lock
class Account:
    def __init__(self, _id, balance):
        self.id = _id
        self.balance = balance
        self.lock = threading.Lock()
    def withdraw(self, amount):
        self.balance -= amount
    def deposit(self, amount):
        self.balance += amount

def transfer(_from, to, amount):
    hasha,hashb = hashlock(_from, to)
    if hasha >hashb:
        _from.lock.acquire()  # 锁住自己的账户
        to.lock.acquire()  # 锁住对方的账户
        #交易#################
        _from.withdraw(amount)
        to.deposit(amount)
        #################
        to.lock.release()
        _from.lock.release()
    elif hasha < hashb:
        to.lock.acquire()  # 锁住自己的账户
        _from.lock.acquire()  # 锁住对方的账户
        # 交易#################
        _from.withdraw(amount)
        to.deposit(amount)
        #################
        _from.lock.release()
        to.lock.release()
    else: ##hash值相等，最上层使用mylock锁，你可以把transfer做成一个类，此类中实例一个mylock。
        mylock.acquire()
        _from.lock.acquire()  # 锁住自己的账户
        to.lock.acquire()  # 锁住对方的账户
        # 交易#################
        _from.withdraw(amount)
        to.deposit(amount)
        #################
        to.lock.release()
        _from.lock.release()
        mylock.release()

def hashlock(_from,to):
    hash1 = hashlib.md5()
    hash1.update(bytes(_from.id, encoding='utf-8'))
    hasha = hash1.hexdigest()
    hash = hashlib.md5()
    hash.update(bytes(to.id, encoding='utf-8'))
    hashb = hash.hexdigest()
    return hasha,hashb

a = Account('a', 1000)
b = Account('b', 1000)
mylock = threading.Lock()
#a往b转账100
t1 = threading.Thread(target=transfer, args=(a, b, 100))
t1.start()
#b往a转账200
t2 = threading.Thread(target=transfer, args=(b, a, 200))
t2.start()
t1.join()
t2.join()
print("a的账户余额：",a.balance)
print("b的账户余额：",b.balance)

"""
使用定时锁-：

加上一个超时时间，若一个线程没有在给定的时限内成功获得所有需要的锁，则会进行回退并释放所有已经获得的锁，然后等待一段随机的时间再重试。

但是如果有非常多的线程同一时间去竞争同一批资源，就算有超时和回退机制，还是可能会导致这些线程重复地尝试但却始终得不到锁。
"""


"""
上下文管理器
import threading
from contextlib import contextmanager
 
# Thread-local state to stored information on locks already acquired
_local = threading.local()
 
@contextmanager
def acquire(*locks):
  # Sort locks by object identifier
  locks = sorted(locks, key=lambda x: id(x))
 
  # Make sure lock order of previously acquired locks is not violated
  acquired = getattr(_local,'acquired',[])
  if acquired and max(id(lock) for lock in acquired) >= id(locks[0]):
    raise RuntimeError('Lock Order Violation')
 
  # Acquire all of the locks
  acquired.extend(locks)
  _local.acquired = acquired
 
  try:
    for lock in locks:
      lock.acquire()
    yield
  finally:
    # Release locks in reverse order of acquisition
    for lock in reversed(locks):
      lock.release()
    del acquired[-len(locks):]


### code test:
import threading
x_lock = threading.Lock()
y_lock = threading.Lock()
 
def thread_1():
  while True:
    with acquire(x_lock, y_lock):
      print('Thread-1')
 
def thread_2():
  while True:
    with acquire(y_lock, x_lock):
      print('Thread-2')
 
t1 = threading.Thread(target=thread_1)
t1.daemon = True
t1.start()
 
t2 = threading.Thread(target=thread_2)
t2.daemon = True
t2.start()
"""
