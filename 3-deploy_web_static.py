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
        local("tar -cvzf {} web_static".format(file))
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
                "mkdir -p {}{}/".format(static_dir, ext),
                "tar -xzf /tmp/{} -C {}{}/".format(file, static_dir, ext),
                "rm /tmp/{}".format(file),
                "mv {0}{1}/web_static/* {0}{1}/".format(static_dir, ext),
                "rm -rf {}{}/web_static".format(static_dir, ext),
                "rm -rf /data/web_static/current".format(),
                "ln -s {}{}/ /data/web_static/current".format(static_dir, ext),
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
