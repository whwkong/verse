"""
Projects module URLs config
"""
from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from projects import views


urlpatterns = [
    url(r'^projects/', include([
        url(
            r'^$',
            views.ProjectsVersionsViewSet.as_view(
                actions={'get': 'list'},
                suffix='List',
            ),
            name='list',
        ),
        url(
            r'^(?P<project>[-_\w]+)/$',
            views.ProjectsVersionsViewSet.as_view(
                actions={'get': 'retrieve'},
                suffix='Latest',
            ),
            name='latest',
        ),
        url(
            r'^(?P<project>[-_\w]+)/major/$',
            views.ProjectsVersionsViewSet.as_view(
                actions={'get': 'major'},
                suffix='Major',
            ),
            name='major',
        ),
        url(
            r'^(?P<project>[-_\w]+)/minor/$',
            views.ProjectsVersionsViewSet.as_view(
                actions={'get': 'minor'},
                suffix='Minor',
            ),
            name='minor',
        ),
    ], namespace='projects')),
    url(r'^gh/', include([
        url(
            r'^(?P<owner>[-_\w]+)/(?P<repo>[-_\w]+)/$',
            views.GitHubProjectsVersionsViewSet.as_view(
                actions={'get': 'retrieve'},
                suffix='Latest',
            ),
            name='latest',
        ),
        url(
            r'^(?P<owner>[-_\w]+)/(?P<repo>[-_\w]+)/major/$',
            views.GitHubProjectsVersionsViewSet.as_view(
                actions={'get': 'major'},
                suffix='Major',
            ),
            name='major',
        ),
        url(
            r'^(?P<owner>[-_\w]+)/(?P<repo>[-_\w]+)/minor/$',
            views.GitHubProjectsVersionsViewSet.as_view(
                actions={'get': 'minor'},
                suffix='Minor',
            ),
            name='minor',
        ),
    ], namespace='github-projects')),
]

urlpatterns = format_suffix_patterns(urlpatterns)
