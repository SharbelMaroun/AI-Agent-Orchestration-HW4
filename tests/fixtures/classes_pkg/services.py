"""Second fixture module: composition via a typed attribute annotation."""


class Repository:
    def __init__(self):
        self.items: list = []

    def add(self, item):
        self.items.append(item)


class Service:
    def __init__(self, repo):
        self.repo: Repository = repo

    def run(self):
        return self.repo.add(1)
