import subprocess

def run(**kwargs):
    return subprocess.check_output("uptime", shell=True).decode("utf8")