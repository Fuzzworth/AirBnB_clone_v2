#!/usr/bin/python3
"""
Module Docs
"""
from os.path import exists, isdir
from datetime import datetime
from fabric.api import put, local, env, run
env.hosts = ["54.237.61.71", "54.146.64.127"]


def do_pack():
    """
    Function Docs
    """
    try:
        if isdir("versions") is False:
            local("mkdir versions")
        file = "versions/web_static_{}.tgz".format(
                    datetime.now().strftime("%Y%m%d%H%M%S")
                )
        local(f"tar -cvzf {file} web_static")
        return file
    except Exception:
        return None


def do_deploy(archive_path):
    """
    Function Docs
    """
    if exists(archive_path) is False:
        return False
    try:
        file = archive_path.split("/")[-1]
        ext = file.split(".")[0]
        static_dir = "/data/web_static/releases/"
        put(archive_path, '/tmp/')
        commands = [
                f"mkdir -p {static_dir}{ext}/",
                f"tar -xzf /tmp/{file} -C {static_dir}{ext}/",
                f"rm /tmp/{file}",
                f"mv {static_dir}{ext}/web_static/* {static_dir}{ext}/",
                f"rm -rf {static_dir}{ext}/web_static",
                f"rm -rf /data/web_static/current",
                f"ln -s {static_dir}{ext}/ /data/web_static/current",
                ]
        for command in commands:
            run(command)
        return True
    except Exception:
        return False


def deploy():
    """
    Function Docs
    """
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
