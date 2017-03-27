"""
Checkers for Go related projects
"""
from checkers.base import BaseVersionChecker
from checkers.utils import remove_prefix


class GoVersionChecker(BaseVersionChecker):
    """
    Go project checker
    """
    name = 'go'
    homepage = 'https://golang.org/'
    repository = 'https://github.com/golang/go'

    @staticmethod
    def _normalize_tag_name(name):
        """
        Normalizes GitHub tag name to be a PEP 404 compliant version name,
        which in this case means removing 'go' prefix
        Example:
            go1.8 -> 1.8

        :param name: tag name
        :type name: str
        :returns: normalized version name
        :rtype: str
        """
        return remove_prefix(name, 'go')

    def get_versions(self):
        """
        Get the versions from GitHub tags
        """
        return self._get_github_tags(normalize_func=self._normalize_tag_name)


class DockerVersionChecker(BaseVersionChecker):
    """
    Docker project checker
    """
    name = 'docker'
    homepage = 'https://www.docker.com/'
    repository = 'https://github.com/docker/docker'

    @staticmethod
    def _normalize_tag_name(name):
        """
        Normalizes GitHub tag name to be a PEP 404 compliant version name,
        which in this case means removing '-ce' (community edition)
        Example:
           v17.03.0-ce  -> v17.03.0

        :param name: tag name
        :type name: str
        :returns: normalized version name
        :rtype: str
        """
        if '-ce' in name:
            name = name.replace('-ce', '')

        return name

    def get_versions(self):
        """
        Get the versions from GitHub tags
        """
        return self._get_github_tags(normalize_func=self._normalize_tag_name)


class KubernetesVersionChecker(BaseVersionChecker):
    """
    Kubernetes project checker
    """
    name = 'kubernetes'
    homepage = 'https://kubernetes.io/'
    repository = 'https://github.com/kubernetes/kubernetes'

    def get_versions(self):
        """
        Get the versions from GitHub tags
        """
        return self._get_github_tags()
