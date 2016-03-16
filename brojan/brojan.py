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
    username = "mantvydo@gmail.com"
    username = "mantvydasb"
    session = ''

    def __init__(self, username=username):
        password = input("Github password: ")
        self.session = Github(username, password)
        self.repository = self.session.get_repo(self.username + "/network-playground")
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
        self.loadModules(config)

    def getConfig(self):
        config = self.getFileContents(self.configPath)
        config = base64.b64decode(config.content).decode("utf8")
        configJson = json.loads(config)
        return configJson

    def getFileContents(self, filePath):
        return self.github.getFileContents(filePath)

    def loadModules(self, config):
        for module in config['modules']:
            if module not in sys.modules:
                print("Loading module '%s' " % module)
                newModule = importlib.import_module('modules.%s' % module)
                sys.modules[module] = newModule
                print(sys.modules)

        self.configured =  True

Brojan()


