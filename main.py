import os
import subprocess

from fastapi import FastAPI

app = FastAPI()


class Config:
    username = os.getenv("USERNAME", "admin")
    password = os.getenv("PASSWORD", "admin")
    repo_path = os.getenv("REPO_PATH", "")
    branch = os.getenv("BRANCH", "master")


config = Config()


def sync_repo(path: str):
    os.chdir(path)
    result = subprocess.run(["git", "log"])
    result = subprocess.run(["git", "pull", f"origin {config.branch}:{config.branch} --force"])
    result.check_returncode()


@app.post("/sync")
async def sync_view():
    sync_repo(config.repo_path)
    return {"result": "ok"}


if __name__ == '__main__':
    sync_repo('/Users/hmj/projects/sync-webhook')

