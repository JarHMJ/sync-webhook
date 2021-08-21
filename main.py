import os
import secrets
import subprocess

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

app = FastAPI()


class Config:
    username = os.getenv("USERNAME", "admin")
    password = os.getenv("PASSWORD", "admin")
    repo_path = os.getenv("REPO_PATH", "")
    branch = os.getenv("BRANCH", "master")


config = Config()

security = HTTPBasic()


def check_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, config.username)
    correct_password = secrets.compare_digest(credentials.password, config.password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


basic_auth = Depends(check_basic_auth)


def sync_repo(path: str):
    os.chdir(path)
    subprocess.run(f"git pull origin {config.branch}:{config.branch} --force -v", shell=True, check=True)


@app.post("/sync", dependencies=[basic_auth])
async def sync_view():
    sync_repo(config.repo_path)
    return {"result": "ok"}


if __name__ == '__main__':
    sync_repo('/Users/hmj/projects/sync-webhook')

