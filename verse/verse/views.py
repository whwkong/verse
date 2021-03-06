"""
Verse application views
"""
import random

from django.views.generic import TemplateView

from rest_framework.reverse import reverse

from checkers.projects import AVAILABLE_CHECKERS


class IndexView(TemplateView):
    """
    Verse index view
    """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        """
        Extends Django's default `get_context_data()` behaviour and adds
        available projects to view context
        """
        available_projects = list()
        for project in AVAILABLE_CHECKERS.values():
            url = reverse(
                'projects:latest', args=[project.slug], request=self.request,
            )

            project = {
                'name': project.name,
                'url': url,
            }
            available_projects.append(project)

        random.shuffle(available_projects)
        kwargs['available_projects'] = available_projects[:50]

        return super().get_context_data(**kwargs)
