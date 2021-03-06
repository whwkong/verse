"""
Test `checkers.projects.webservers` file
"""
import pytest

from checkers import base
from checkers.projects import webservers


class TestApacheVersionChecker:
    """
    Test `webservers.ApacheVersionChecker` class
    """
    @pytest.fixture
    def instance(self):
        return webservers.ApacheVersionChecker()

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, base.BaseVersionChecker)
        assert isinstance(instance, base.GitHubVersionChecker)

    def test_class_properties(self, instance):
        """Test class properties"""
        assert instance.name == 'Apache HTTP Server'
        assert instance.slug == 'apache-httpd'
        assert instance.homepage == 'http://httpd.apache.org/'
        assert instance.repository == 'https://github.com/apache/httpd'


class TestNginxVersionChecker:
    """
    Test `webservers.NginxVersionChecker` class
    """
    @pytest.fixture
    def instance(self):
        return webservers.NginxVersionChecker()

    def test_class_inheritance(self, instance):
        """Test class inheritance"""
        assert isinstance(instance, base.BaseVersionChecker)
        assert isinstance(instance, base.GitHubVersionChecker)

    def test_class_properties(self, instance):
        """Test class properties"""
        assert instance.name == 'Nginx'
        assert instance.slug == 'nginx'
        assert instance.homepage == 'http://nginx.org/'
        assert instance.repository == 'https://github.com/nginx/nginx'

    def test_class_normalize_tag_name_method(self, instance):
        """Test class `_normalize_tag_name()` method"""
        assert instance._normalize_tag_name('release-1.11.9') == '1.11.9'
        assert instance._normalize_tag_name('1.11.9') == '1.11.9'

    def test_class_get_versions_method(self, mocker, instance):
        """Test class `get_versions()` method"""
        mocked_get_github_tags = mocker.patch.object(
            instance, '_get_github_tags',
        )

        assert instance.get_versions() == mocked_get_github_tags.return_value

        mocked_get_github_tags.assert_called_once_with(
            normalize_func=instance._normalize_tag_name,
        )
