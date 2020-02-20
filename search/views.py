from django.db.models import QuerySet
from rest_framework import generics

from search.models import save_projects, Project
from search.serializers import ProjectSerializer
from search.service import GitlabProjectParser


class ListProjects(generics.ListAPIView):
    """
    List Projects
    """
    serializer_class = ProjectSerializer

    def get_queryset(self) -> QuerySet:
        """
        return filtered projects by passed string 'search'
        without any pagination
        :return: queryset
        """
        search = self.request.GET.get("search")
        if not search:
            return Project.objects.none()

        projects = GitlabProjectParser().find_projects(search)
        saved_projects = save_projects(projects)
        return saved_projects
