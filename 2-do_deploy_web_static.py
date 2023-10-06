#!/usr/bin/python3
"""
Module doc
"""
from os.path import exists, basename, splitext
from datetime import datetime
from fabric.api import env, task, put, local, run
env.use_ssh_config = True
env.hosts = ["54.237.61.71", "54.146.64.127"]


def do_pack():
    """
    Function Docs
    """
    file = "versions/web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S')
            )
    print("Packing web_static to {file}".format(file))
    if local("mkdir -p versions && tar -cvzf {file} web_static".format(file)).succeeded:
        return file
    return None


def do_deploy(archive_path):
    """
    Function Docs
    """
    try:
        if not exists(archive_path):
            return False
        ext = basename(archive_path)
        no_ext, ext = splitext(ext)
        web_static_dir = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        commands = [
                "rm -rf {}{}/".format(web_static_dir, no_ext),
                "mkdir -p {}{}/".format(web_static_dir, no_ext),
                "tar -xzf /tmp/{} -C {}{}/".format(ext, web_static_dir, no_ext),
                "rm /tmp/{}".format(ext),
                "mv {0}{1}/web_static/* {0}{1}/".format(web_static_dir, no_ext),
                "rm -rf {}{}/web_static".format(web_static_dir, no_ext),
                "rm -rf /data/web_static/current",
                "ln -s {}{}/ /data/web_static/current".format(web_static_dir, no_ext),
                ]
        for command in commands:
            run(command)
        print("New version deployed!")
        return True
    except Exception:
        return False
