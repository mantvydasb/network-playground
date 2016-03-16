import subprocess

def execute(**kwargs):
    return subprocess.check_output("uptime", shell=True).decode("utf8")