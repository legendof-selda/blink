import subprocess
import os
import sys


def current_version(commits_ahead=False):
    if isinstance(commits_ahead, str):
        commits_ahead = commits_ahead.lower() == "true"
    env = os.environ.copy()
    output = subprocess.run(
        "git describe --tags --long",
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if output.returncode == 0:
        output = output.stdout.decode("utf-8").strip()
    else:
        output = "v0.0.0-0-0"
    output = output.split("-")
    tag = output[0]
    if commits_ahead:
        return tag, output[1]
    return tag


def latest_version():
    tag, patch = current_version(commits_ahead=True)
    tag = tag.split(".")
    patch = int(tag[-1]) + int(patch)
    tag = ".".join(tag[:-1]) + "." + str(patch)
    return tag


def update_version_tag():
    tag = latest_version()
    env = os.environ.copy()
    subprocess.run(
        f'git tag -a {tag} -m "updated to new version {tag}"', shell=True, env=env
    )
    return current_version()


def revert_version_tag():
    tag = current_version()
    env = os.environ.copy()
    subprocess.run(f"git tag -d {tag}", shell=True, env=env)
    return current_version()


def new_version(new_tag: str, update_patch: bool = True):
    tag = new_tag
    if isinstance(update_patch, str):
        update_patch = update_patch.lower() != "false"
    if update_patch:
        _, patch = current_version(commits_ahead=True)
        tag = tag.split(".")
        if len(tag) < 3 or tag[-1] == "":
            tag = ".".join(tag[:-1]) + "." + str(patch)
        else:
            patch = int(tag[-1]) + int(patch)
            tag = ".".join(tag[:-1]) + "." + str(patch)
    return tag


def create_new_version_tag(
    new_tag: str,
    new_version_description: str = "Release Version",
    update_patch: bool = True,
):
    tag = new_version(new_tag, update_patch)
    env = os.environ.copy()
    subprocess.run(
        f'git tag -a {tag} -m "{new_version_description} - {tag}"', shell=True, env=env
    )
    return current_version()


def view_releases():
    env = os.environ.copy()
    output = subprocess.run(
        'git tag -l --sort=-version:refname "v*" -n3',
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if output.returncode == 0:
        return output.stdout.decode("utf-8")
    else:
        return None


def set_version_in_environemnt(env: str):
    with open("./Dockerfile", "r+") as docker:
        content = docker.read()
        content.replace()


def get_remote_url():
    env = os.environ.copy()
    output = subprocess.run(
        "git config --get remote.origin.url",
        shell=True,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if output.returncode == 0:
        return output.stdout.decode("utf-8").replace(".git", "")
    else:
        return None


if __name__ == "__main__":
    try:
        function = sys.argv[1]
        params = sys.argv[2:]
        print(globals()[function](*params))
    except IndexError:
        print(current_version())
    except KeyError:
        raise Exception(f"Invalid argument {function}")
