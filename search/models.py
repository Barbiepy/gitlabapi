from django.db import models
from django.db.models import QuerySet


class Project(models.Model):
    """
    Gitlab project model
    """

    id = models.IntegerField("Id", primary_key=True)
    name = models.CharField("name", max_length=256)
    description = models.TextField("Description", null=True)
    created_at = models.DateTimeField("Created at", auto_now_add=True)
    last_activity_at = models.DateTimeField("Last activity at")

    class Meta:
        verbose_name = "project"
        verbose_name_plural = "projects"

    def __str__(self):
        return self.name


def save_projects(projects: list) -> QuerySet:
    """
    Drop and save passed projects to db instead update one by one
    :param projects: list of projects
    :return: queryset of projects after saving
    """
    projects_ids = [project["id"] for project in projects]
    Project.objects.filter(id__in=projects_ids).delete()
    Project.objects.bulk_create([
        Project(**project) for project in projects
    ])

    return Project.objects.filter(id__in=projects_ids)
