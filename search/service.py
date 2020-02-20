"""
Utils for working with projects
"""
import asyncio
import aiohttp
import requests
import json


class GitlabProjectParser:
    """
    Service for searching gitlab projects
    Example of usage
    search_string = 'lol'
    projects = GitlabProjectParser().find_projects(search)
    """

    # it's unreadable, but flake8 :(
    GITLAB_SEARCH_URL = \
        "https://gitlab.com/api/v4/projects" \
        "?per_page=50&order_by=id&sort=asc&search="

    async def _load_projects(self,
                             url: str,
                             session: aiohttp.ClientSession) -> None:
        """
        Load projects by passed url
        :param url:  Url
        :param session: object of aiohttp.ClientSession
        :return:
        """
        async with session.get(url) as response:
            data = await response.text()
            data = json.loads(data)

            for project in data:
                # naive realization, can be optimized for best performance
                for key in tuple(project.keys()):
                    if key not in ("id",
                                   "name",
                                   "description",
                                   "last_activity_at"):
                        del project[key]

            self.projects.extend(data)

    async def _get_data(self, urls: list) -> None:
        """
        Start loading projects asynchronously by passed urls
        :param urls: list of urls
        :return:
        """
        tasks = []

        async with aiohttp.ClientSession() as session:
            for url in urls:
                task = asyncio.create_task(self._load_projects(url, session))
                tasks.append(task)

            await asyncio.gather(*tasks)

    def find_projects(self, search: str) -> list:
        """
        Search projects which contain passed string 'search'
        :param search: string
        :return: list with projects
        """

        self.search_url = ''.join([self.GITLAB_SEARCH_URL, search])
        self.projects = []

        headers = requests.head(self.search_url).headers
        projects_count = headers["X-Total"]

        if not projects_count:
            return []

        total_pages = int(headers["X-Total-Pages"])
        urls = [''.join([self.search_url, '&page=', str(page)])
                for page in range(1, total_pages + 1)]

        asyncio.run(self._get_data(urls))

        return self.projects
