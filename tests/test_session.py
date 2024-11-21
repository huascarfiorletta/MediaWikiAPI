# -*- coding: utf-8 -*-
import unittest

from mediawikiapi import MediaWikiAPI
from mediawikiapi.requestsession import deep_update_unique

api = MediaWikiAPI()


class TestSession(unittest.TestCase):
    def test_new_session(self) -> None:
        """Test the new_session function"""
        api.session.new_session()
        s1 = api.session.session
        self.assertIsNotNone(s1)

        api.session.new_session()
        s2 = api.session.session
        self.assertIsNotNone(s2)

        self.assertNotEqual(s1, s2)

    def test_get_session(self) -> None:
        """Test the get_session function"""
        api.session.new_session()
        s1 = api.session.session
        self.assertIsNotNone(s1)

        s2 = api.session.session
        self.assertIsNotNone(s2)
        self.assertEqual(s1, s2)

    def test_deep_update_unique(self) -> None:
        # Test case 1: Basic dictionary update
        target = {'a': 1, 'b': 2}
        source = {'c': 3, 'd': 4}
        expected = {'a': 1, 'b': 2, 'c': 3, 'd': 4}
        assert deep_update_unique(target, source) == expected
        assert target == expected

        # Test case 2: Nested dictionary update
        target = {
            'x': 1,
            'nested': {'a': 10, 'b': 20}
        }
        source = {
            'y': 2,
            'nested': {'c': 30, 'a': 100}  # Note: 'a' already exists
        }
        expected = {
            'x': 1,
            'y': 2,
            'nested': {'a': 10, 'b': 20, 'c': 30}
        }
        assert deep_update_unique(target, source) == expected
        assert target == expected

        # Test case 3: List update with unique items
        target = {
            'list1': [1, 2, 3],
            'list2': [{'a': 1}, {'b': 2}]
        }
        source = {
            'list1': [3, 4, 5],
            'list2': [{'a': 1}, {'c': 3}],
            'new_list': [10, 20]
        }
        expected = {
            'list1': [1, 2, 3, 4, 5],
            'list2': [{'a': 1}, {'b': 2}, {'c': 3}],
            'new_list': [10, 20]
        }
        result = deep_update_unique(target, source)
        assert result == expected
        assert target == expected

        # Test case 4: Empty source dictionary
        target = {'a': 1, 'b': 2}
        source = {}
        expected = {'a': 1, 'b': 2}
        assert deep_update_unique(target, source) == expected
        assert target == expected

        # Test case 5: Empty target dictionary
        target = {}
        source = {'a': 1, 'b': 2}
        expected = {'a': 1, 'b': 2}
        assert deep_update_unique(target, source) == expected
        assert target == expected

        # Test case 6: Complex nested structure
        target = {
            'users': {
                'admin': {'permissions': ['read', 'write']},
                'guest': {'permissions': ['read']}
            }
        }
        source = {
            'users': {
                'moderator': {'permissions': ['moderate']},
                'admin': {'role': 'super'}
            }
        }
        expected = {
            'users': {
                'admin': {
                    'permissions': ['read', 'write'],
                    'role': 'super'
                },
                'guest': {'permissions': ['read']},
                'moderator': {'permissions': ['moderate']}
            }
        }
        result = deep_update_unique(target, source)
        assert result == expected
        assert target == expected
