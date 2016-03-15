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

    def __init__(self, username=username):
        password = input("Github password: ")
        self.session = Github(username, password)


class Brojan():

    def __init__(self):
        github = GitHubSession()
        repository = github.session.get_repo(github.username + "/network-playground")




Brojan()
