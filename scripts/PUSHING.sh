#!/usr/bin/env python
#-*- coding: UTF-8 -*-

from subprocess import Popen, PIPE
import os

def get_repos(path):
    """
    get a list of root git dirs
    """
    locate = Popen(("", '-r', "%s.*/\.git$" % path), 0,
        "/usr/bin/locate", stdout=PIPE)
    output = [path[:-6] for path in locate.stdout.readlines()]

    return output


def pushing(repo):
    """
    execute pushing on the repo dir
    """
    os.chdir(repo)
    process = Popen(("pushing",), shell=True)
    return process.wait()


"""    | awk -v pwd="$PWD" '
    function exec(command){
        while (command|getline result)
            print result
        return result
    }

    {
        sub("\\.git$", "")
        exec("echo \"" $0 "\"")
#        ; cd \"" $0 "\"; pushing")
}'"""


def main():
    curdir = os.path.abspath(os.path.curdir)
    repos = get_repos(curdir)
    for repo in repos:
        print repo.replace(curdir, ".")
        pushing(repo)

if __name__ == "__main__":
    exit(main())

