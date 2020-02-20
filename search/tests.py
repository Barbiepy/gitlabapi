from django.test import TestCase
import requests

from search.service import GitlabProjectParser


class ProjectTestCase(TestCase):
    GITLAB_SEARCH_URL = \
        "https://gitlab.com/api/v4/projects" \
        "?per_page=50&order_by=id&sort=asc&search="

    def test_gitlab_api_headers(self):
        """
        Test gitlab api for required parameters
        :return:
        """
        search_url = ''.join([self.GITLAB_SEARCH_URL, "lol"])
        headers = requests.head(search_url).headers
        self.assertTrue(all([
            item in headers.keys() for item in ("X-Total", "X-Total-Pages")
        ]))

    def test_find_projects(self):
        """
        Test structure and count projects
        :return:
        """
        for search in ["lol", '2', 'lf', "adjsfkajdfl;aj;sdlf"]:
            search_url = ''.join([self.GITLAB_SEARCH_URL, search])

            headers = requests.head(search_url).headers

            projects = GitlabProjectParser().find_projects(search)
            self.assertEqual(int(headers["X-Total"]), len(projects))

            if projects:  # Test structure
                self.assertEqual(len(projects[0].keys()), 4)
                structure = {"id",
                             "name",
                             "description",
                             "last_activity_at"}
                self.assertEqual(set(projects[0]) - structure, set())
