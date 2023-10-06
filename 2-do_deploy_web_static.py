#!/usr/bin/python3
""" 
Module doc
"""
from os.path import exists, basename, splitext
from datetime import datetime
from fabric.api import env, task, put, local, run

env.hosts = ["54.237.61.71", "54.146.64.127"]


def do_pack():
    """
    Function Docs
    """
    file = "versions/web_static_{}.tgz".format(
            datetime.now().strftime('%Y%m%d%H%M%S')
            )
    print(f"Packing web_static to {file}")
    if local(f"mkdir -p versions && tar -cvzf {file} web_static").succeeded:
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
                f"rm -rf {web_static_dir}{no_ext}/",
                f"mkdir -p {web_static_dir}{no_ext}/",
                f"tar -xzf /tmp/{ext} -C {web_static_dir}{no_ext}/",
                f"rm /tmp/{ext}",
                f"mv {web_static_dir}{no_ext}/web_static/* {web_static_dir}{no_ext}/",
                f"rm -rf {web_static_dir}{no_ext}/web_static",
                f"rm -rf /data/web_static/current",
                f"ln -s {web_static_dir}{no_ext}/ /data/web_static/current",
                ]
        for command in commands:
            run(command)
        print("New version deployed!")
        return True
    except Exception:
        return False
