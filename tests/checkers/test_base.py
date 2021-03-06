"""
Test `checkers.base` file
"""
import inspect
import random
from unittest.mock import MagicMock

import pytest
from github3.repos import Repository
from github3.repos.tag import RepoTag
from packaging.version import Version

from checkers.base import BaseVersionChecker, GitHubVersionChecker
from checkers.projects import AVAILABLE_CHECKERS


class TestBaseVersionChecker:
    """
    Test `BaseVersionChecker` class
    """
    klass = BaseVersionChecker
    versions = [
        '17.03.2-rc1', '17.03.1', '17.03.0', '1.3.1', '1.3.0', '1.2.2',
        '1.2.1', '1.2.0', '1.0', '0.6.1', '0.6.0', '0.5', '0.1.1', '0.1',
    ]

    @pytest.fixture
    def instance(self, mocker):
        """Helper fixture for creating instance of an abstract class"""
        mocker.patch.multiple(self.klass, __abstractmethods__=set())
        return self.klass()

    def test_class_abstraction(self):
        """Test if the class is an abstract class"""
        assert inspect.isabstract(self.klass)

    def test_class_initialization(self, mocker):
        """Test class `__init__` method"""
        mocker.patch.multiple(self.klass, __abstractmethods__=set())

        name = 'python'
        homepage = 'https://www.python.org/'
        repository = 'https://github.com/python/cpython'

        instance = self.klass(
            name=name, homepage=homepage, repository=repository,
        )

        assert instance.name == name
        assert instance.homepage == homepage
        assert instance.repository == repository

    def test_class_get_versions_method(self, instance):
        """Test class `get_versions()` method"""
        with pytest.raises(NotImplementedError):
            instance.get_versions()

    def test_class_get_latest_version_method(self, mocker, instance):
        """Test class `get_latest_version()` method"""
        mocker.patch.object(
            instance, 'get_versions',
            return_value=[Version(v) for v in self.versions],
        )

        assert instance.get_latest_version() == '17.3.1'

    def test_class_get_latest_major_versions_method(self, mocker, instance):
        """Test class `get_latest_major_versions()` method"""
        mocker.patch.object(
            instance, 'get_versions',
            return_value=[Version(v) for v in self.versions],
        )

        assert instance.get_latest_major_versions() == {
            '17': '17.3.1',
            '1': '1.3.1',
            '0': '0.6.1',
        }

        # Unsorted result from `get_version()`
        unsorted_versions = self.versions.copy()
        random.shuffle(unsorted_versions)
        mocker.patch.object(
            instance, 'get_versions',
            return_value=[Version(v) for v in unsorted_versions],
        )

        with pytest.raises(ValueError):
            instance.get_latest_major_versions()

    def test_class_get_latest_minor_versions_method(self, mocker, instance):
        """Test class `get_latest_minor_versions()` method"""
        mocker.patch.object(
            instance, 'get_versions',
            return_value=[Version(v) for v in self.versions],
        )

        assert instance.get_latest_minor_versions() == {
            '17.3': '17.3.1',
            '1.3': '1.3.1',
            '1.2': '1.2.2',
            '1.0': '1.0',
            '0.6': '0.6.1',
            '0.5': '0.5',
            '0.1': '0.1.1',
        }

        # Unsorted result from `get_version()`
        unsorted_versions = self.versions.copy()
        random.shuffle(unsorted_versions)
        mocker.patch.object(
            instance, 'get_versions',
            return_value=[Version(v) for v in unsorted_versions],
        )

        with pytest.raises(ValueError):
            instance.get_latest_minor_versions()


class TestGitHubVersionChecker:
    """
    Test `GitHubVersionChecker` class
    """
    @pytest.fixture
    def instance(self):
        return GitHubVersionChecker()

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, BaseVersionChecker)

    def test_class_get_github_tags_method(self, mocker, instance):
        """Test class `_get_github_tags()` method"""
        # Non GitHub URL
        with pytest.raises(ValueError):
            list(instance._get_github_tags('http://example.com'))

        # Test tag name normalization
        mocked_repo = MagicMock(autospec=Repository)

        mocked_tags = list()
        versions = [
            '17.03.2-rc1', '17.03.1', '2.1-foobar', '2.0.1', '2', 'v1.2',
            'v1.1', 'v1', 'v0.2.1', 'v0.2', '0.1.0', 'not a version',
        ]
        for version in versions:
            mocked_tag = MagicMock(autospec=RepoTag)
            mocked_tag.name = version
            mocked_tags.append(mocked_tag)

        mocked_github_client = mocker.patch('checkers.base.github_client')
        mocked_repo.iter_tags.return_value = mocked_tags
        mocked_github_client.repository.return_value = mocked_repo

        result_gen = instance._get_github_tags(
            'https://github.com/pawelad/verse'
        )
        assert inspect.isgenerator(result_gen)

        result = list(result_gen)
        expected_versions = [
            '17.3.2rc1', '17.3.1', '2.0.1', '2.0', 'v1.2',
            'v1.1', 'v1.0', 'v0.2.1', 'v0.2', '0.1.0',
        ]
        assert result == [Version(v) for v in expected_versions]

        mocked_github_client.repository.assert_called_once_with(
            'pawelad', 'verse',
        )
        mocked_repo.iter_tags.assert_called_once_with()

        # Without explicit URL
        instance.repository = 'https://github.com/pawelad/verse'
        assert result == list(instance._get_github_tags())

        # With normalize func
        normalize_func = MagicMock(side_effect=versions)
        list(instance._get_github_tags(normalize_func=normalize_func))

        assert normalize_func.call_count == len(versions)

    def test_class_get_versions_method(self, mocker, instance):
        """Test class `get_versions()` method"""
        mocked_get_github_tags = mocker.patch.object(
            instance, '_get_github_tags',
        )

        assert instance.get_versions() == mocked_get_github_tags.return_value

        mocked_get_github_tags.assert_called_once_with()


def test_checkers_slug_uniqueness():
    """Test checkers slug uniqueness"""
    used_slugs = set()
    for project in AVAILABLE_CHECKERS.values():
        slug = project.slug

        assert slug not in used_slugs

        used_slugs.add(project.slug)
