"""
Checkers for Go related projects
"""
from checkers.base import BaseVersionChecker
from checkers.utils import remove_prefix


class jQueryVersionChecker(BaseVersionChecker):
    """
    jQuery project checker
    """
    name = 'jquery'
    homepage = 'https://jquery.com/'
    repository = 'https://github.com/jquery/jquery'

    def get_versions(self):
        """
        Get the versions from GitHub tags
        """
        return self._get_github_tags()