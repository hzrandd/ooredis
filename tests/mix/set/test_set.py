#! /usr/bin/env python2.7
# coding: utf-8

import redis
import unittest

from ooredis.client import connect

from ooredis.mix.key import Key
from ooredis.mix.set import Set
from ooredis.mix.helper import format_key
    
class TestSet(unittest.TestCase):

    def setUp(self):
        connect()

        self.redispy = redis.Redis()
        self.redispy.flushdb()

        self.s = Set('set')
        self.another = Set('another')
        self.third = Set('third')

        self.element = 'element'

    def tearDown(self):
        self.redispy.flushdb()

    def set_wrong_type(self, key_object):
        self.redispy.set(key_object.name, 'string')

    # __repr__

    def test__repr__(self):
        assert repr(self.s) == \
               format_key(self.s, self.s.name, set(self.s))

    # __len__

    def test__len__with_EMPTY_SET(self):
        assert len(self.s) == 0

    def test__len__with_NOT_EMPTY_SET(self):
        self.s.add(self.element)
        assert len(self.s) == 1

    def test__len__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            len(self.s)

    # __iter__

    def test__iter__with_EMPTY_SET(self):
        assert list(iter(self.s)) == []

    def test__iter__with_NOT_EMPTY_SET(self):
        self.s.add(self.element)
        assert list(iter(self.s)) == [self.element]

    def test__iter__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            list(iter(self.s))

    # __contains__

    def test__contains__FALSE(self):
        assert self.element not in self.s

    def test__contains__TRUE(self):
        self.s.add(self.element)
        assert self.element in self.s

    def test__contains__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.element in self.s

    # add

    def test_add_with_EMPTY_SET(self):
        self.s.add(self.element)
        assert set(self.s) == set([self.element])

    def test_add_when_ELEMENT_IS_SET_MEMBER(self):
        self.s.add(self.element)

        self.s.add(self.element)
        assert set(self.s) == set([self.element])

    def test_add_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.add(self.element)

    # remove

    def test_remove_when_ELEMENT_EXISTS(self):
        self.s.add(self.element)

        self.s.remove(self.element)
        assert set(self.s) == set()

    def test_remove_RAISE_when_ELEMENT_NOT_EXISTS(self):
        with self.assertRaises(KeyError):
            self.s.remove(self.element)

    def test_remove_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.remove(self.element)

    # pop

    def test_pop_RAISE_when_SET_EMPTY(self):
        with self.assertRaises(KeyError):
            self.s.pop()

    def test_pop_with_NOT_EMPTY_SET(self):
        self.s.add(self.element)

        assert self.s.pop() == self.element
        assert len(self.s) == 0

    def test_pop_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.pop()

    # random

    def test_random_with_EMPTY_SET(self):
        assert self.s.random() is None

    def test_random_with_NOT_EMPTY_SET(self):
        self.s.add(self.element)

        assert self.s.random() == self.element

        assert len(self.s) == 1
        assert set(self.s) == set([self.element])

    def test_random_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.random()

    # move

    def test_move_ELEMENT_NOT_EXISTS_IN_DESTINATION_SET(self):
        self.s.add(self.element)

        self.s.move(self.another, self.element)

        # remove self.element from self.s
        assert len(self.s) == 0 
        # move ok
        assert len(self.another) == 1
        assert set(self.another) == set([self.element])

    def test_move_ELEMENT_EXISTS_IN_DESTINATION_SET(self):
        self.s.add(self.element)
        self.another.add(self.element)

        self.s.move(self.another, self.element)

        # remove self.element from self.s
        assert len(self.s) == 0

        # self.another not change(cause self.element alread exists)
        assert len(self.another) == 1
        assert set(self.another) == set([self.element])

    def test_move_RAISE_KEY_ERROR_when_ELEMENT_NOT_SET_MEMBER(self):
        with self.assertRaises(KeyError):
            self.s.move(self.another, 'not_exists_member')

    def test_move_RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.move(self.another, self.element)

    def test_move_RAISE_when_DESTINATION_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.s.add(self.element)

            self.set_wrong_type(self.another)
            self.s.move(self.another, self.element)

    # isdisjoint

    def test_isdisjoint_True(self):
        self.s.add(self.element)
        assert self.s.isdisjoint(self.another)

    def test_isdisjoint_False(self):
        self.s.add(self.element)
        self.another.add(self.element)

        assert not self.s.isdisjoint(self.another)

    def test_idisjoint_with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s.isdisjoint(set())

    def test_isdisjoint_RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s.isdisjoint(set())

    def test_isdisjoint_RAISE_when_OTHER_SET_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s.isdisjoint(self.another)

    # __le__

    def test__le__True(self):
        assert self.s <= self.another

    def test__le__False(self):
        self.s.add(self.element)
        assert not self.s <= self.another

    def test__le__with_PYTHON_SET(self):
        assert self.s <= set()

    def test__le__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s <= self.another

    def test__le__RAISE_when_OTHER_SET_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s <= self.another

    # issubset

    def test_issubset(self):
        self.s.issubset(self.another)

    # __lt__

    def test__lt__True(self):
        self.another.add(self.element)
        assert self.s < self.another

    def test__lt__False(self):
        self.s.add(self.element)
        assert not self.s < self.another

    def test__lt__with_PYTHON_SET(self):
        assert not self.s < set()  

    def test__lt__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s < self.another

    def test__lt__RAISE_when_OTHER_SET_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s < self.another

    # __ge__

    def test__ge__TRUE(self):
        assert self.s >= self.another

    def test__ge__FALSE(self):
        self.another.add(self.element)
        assert not self.s >= self.another

    def test__ge__with_PYTHON_SET(self):
        assert self.s >= set()

    def test__ge__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s >= self.another

    def test__ge__RAISE_when_OTHER_SET_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s >= self.another

    # issuperset

    def test_issuperset(self):   
        self.s.issuperset(self.another)

    # __gt__

    def test__gt__True(self):
        self.s.add(self.element)
        assert self.s > self.another

    def test__gt__FALSE(self):
        self.another.add(self.element)
        assert not self.s > self.another

    def test__gt__with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s > set()
    
    def test__gt__RAISE_when_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s > self.another

    def test__gt__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s > self.another

    # __or__

    def test__or__(self):
        self.s.add(self.element)
        assert self.s | self.another == {self.element}

    def test__or__with_MULTI_OPERAND(self):
        self.s.add(self.element)
        assert self.s | self.another | self.third == {self.element}

    def test__or__with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s | set() == {self.element}

    def test__or__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s | self.another

    def test__or__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s | self.another

    # __ror__

    def test__ror__(self):
        self.s.add(self.element)
        assert self.another | self.s == {self.element}

    # __ior__

    def test__ior__with_EMPTY_SET(self):
        self.s |= self.another

        assert set(self.s) == set()
        assert set(self.another) == set()

    def test__ior__with_NOT_EMPTY_SET(self):
        self.another.add(self.element)

        self.s |= self.another

        assert set(self.s) == set(self.another)
        assert set(self.another) == {self.element}

    def test_ior_with_PYTHON_SET(self):
        self.s |= {1, 2, 3}

        self.assertEqual(
            set(self.s) ,
            {1, 2, 3}
        )

    def test__ior__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s |= self.another

    def test__ior__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s |= self.another

    # __and__

    def test__and__(self):
        self.s.add(self.element)
        self.another.add(self.element)

        assert self.s & self.another == {self.element}

    def test__and__with_MULTI_OPERAND(self):
        self.s.add(self.element)
        self.another.add(self.element)
        self.third.add(self.element)

        assert self.s & self.another & self.third == {self.element}
            
    def test__and__with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s & {self.element} == {self.element}

    def test__and__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s & self.another

    def test__and__RAISE_when_OTHER_SET_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s & self.another

    # __rand__

    def test__rand__(self):
        self.s.add(self.element)
        assert {self.element} & self.s == {self.element}

    # __iand__

    def test__iand__with_EMPTY_SET(self):
        self.s &= self.another

        assert set(self.s) == set()
        assert set(self.s) == set(self.another)

    def test__iand__with_NOT_EMPTY_SET(self):   
        self.s.add(self.element)

        self.another.add(self.element)
        
        self.s &= self.another

        assert set(self.s) == {self.element}
        assert set(self.s) == set(self.another)

    def test__iand__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s &= self.another
   
    def test__iand__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s &= self.another

    # __sub__

    def test__sub__with_EMPTY_SET(self):
        assert self.s - self.another == set()

    def test__sub__with_NOT_EMPTY_SET(self):
        self.s.add(self.element)
        assert self.s - self.another == {self.element}

    def test__sub__with_MULTI_OPERAND(self):
        self.s.add(self.element)
        self.another.add(self.element)
        self.third.add(self.element)

        assert self.s - self.another - self.third == set()

    def test__sub__with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s - set() == {self.element}

    def test__sub__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s - self.another

    def test__sub__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s - self.another

    # __rsub__

    def test__rsub__(self):
        self.s.add(self.element)
        assert set() - self.s == set() 

    #__isub__

    def test__isub__with_EMPTY_SET(self):
        self.s -= self.another

        assert set(self.s) == set()
        assert set(self.another) == set()

    def test__isub__with_NOT_EMPTY_SET(self):
        self.s.add(self.element)

        self.s -= self.another

        assert set(self.s) == {self.element}
        assert set(self.another) == set()

    def test__isub__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s -= self.another

    def test__isub__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s -= self.another

    # __xor__

    def test__xor__with_EMPTY_SET(self):
        assert self.s ^ self.another == set()

    def test__xor__with_NOT_EMPTY_SET(self):
        self.s.add(self.element)
        assert self.s ^ self.another == {self.element}

    def test__xor__with_MULTI_OPERAND(self):
        self.s.add(self.element)

        assert self.s ^ self.another ^ self.third == {self.element}

    def test__xor__with_PYTHON_SET(self):
        self.s.add(self.element)
        assert self.s ^ set() == {self.element}

    def test__xor__RAISE_when_SELF_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.s)
            self.s ^ self.another

    def test__xor__RAISE_when_OTHER_WRONG_TYPE(self):
        with self.assertRaises(TypeError):
            self.set_wrong_type(self.another)
            self.s ^ self.another

    # __rxor__

    def test__rxor__(self):
        assert {self.element} ^ self.s == {self.element}

if __name__ == "__main__":
    unittest.main()
