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
        dpath = "/data/web_static/releases/"
        put(archive_path, "/tmp/")
        run("rm -rf {}{}/".format(dpath, fn_no_ext))
        run("mkdir -p {}{}/".format(dpath, fn_no_ext))
        run("tar -xzf /tmp/{} -C {}{}/".format(fn_with_ext, dpath, fn_no_ext))
        run("rm /tmp/{}".format(fn_with_ext))
        run("mv {0}{1}/web_static/* {0}{1}/".format(dpath, fn_no_ext))
        run("rm -rf {}{}/web_static".format(dpath, fn_no_ext))
        run("rm -rf /data/web_static/current")
        run("ln -s {}{}/ /data/web_static/current".format(dpath, fn_no_ext))
        print("New version deployed!")
        return True
    except Exception:
        return False
