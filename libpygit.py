import argparse         #to parse cl args
import collections      #for OrderedDict
import configparser     #for reading and writing INI format
import hashlib          #for SHA-1 function
import os               #for file system abstraction routines
import re               #regeX ugh
import sys              #for accessing cl args
import zlib             #compression

# for working with command line arg
argparser = argparse.ArgumentParser(description='The stupid content tracker')


#for implementing pygit command
#choosen subparser name will be returned as a string in field called "command"
argsubparser = argparser.add_subparsers(title="Commands", dest="command")
argsubparser.required = True

def main(argv = sys.argv[1:]):
    args = argparser.parse_args(argv)

    if args.command == "add"                : cmd_add(args)
    elif args.command == "cat-file"         : cmd_cat_file(args)
    elif args.command == "checkout"         : cmd_checkout(args)
    elif args.command == "commit"           : cmd_commit(args)
    elif args.command == "hash-object"      : cmd_hash_object(args)
    elif args.command == "init"             : cmd_init(args)
    elif args.command == "log"              : cmd_log(args)
    elif args.command == "ls-tree"          : cmd_ls_tree(args)
    elif args.command == "merge"            : cmd_merge(args)
    elif args.command == "rebase"           : cmd_rebase(args)
    elif args.command == "rev-parse"        : cmd_rev_parse(args)
    elif args.command == "rm"               : cmd_rm(args)
    elif args.command == "show-ref"         : cmd_show_ref(args)
    elif args.command == "tag"              : cmd_tag(args)
    
#pygit init
class GitRepository(object):
    """A git repository"""

    worktree = None
    gitdir = None
    conf = None

    def __init__(self, path, force=False):
        self.worktree = path
        self.gitdir = os.path.join(path, ".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception("Not a Git Repository %s" % path)


        #Read the configuration file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Exception("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion %s" % vers)


    # Member funtion for creating missing directories
    def repo_path(repo, *path):

        """Compute path under repo's gitdir. """
        return os.path.join(repo.gitdir, *path)

    #for returning and creating a path to a dir
    def repo_file(repo, *path, mkdir=False):
        """Same as repo_path, but it creates dirname(*path) if absent. For
        example, repo_file(r, \"refs\", \"remotes\", \"origin\", \"HEAD\") will create
        .git/refs/remotes/origin."""

        if repo_dir(repo, *path[:-1], mkdir=mkdir):
            return repo_path(repo, *path)

    
    def repo_dir(repo, *path, mkdir=False):
        """Same as repo_path but mkdir *path if absent if mkdir """

        path = repo_path(repo, *path)

        if os.path.exists(path):
            if(os.path.isdir(path)):
                return path
            else:
                raise Exception("Not a directory %s" % path)

        
        if mkdir:
            os.makedirs(path)
            return path

        else:
            return None

    
    """Creating paths for initializing the project """

    def repo_create(path):
        """Create a new repository at path"""

        repo = GitRepository(path, True)

        #First, making sure that the path either doesn't exist
        #or is an empty dir

        if os.path.exists(repo.worktree):
            if not os.path.isdir(repo.worktree):
                raise Exception("%s is not a directory!" % path)
            if os.listdir(repo.worktree):
                raise Exception("%s is not empty!" % path)
        else:
            os.makedirs(repo.worktree)

        assert(repo_dir(repo, "branches", mkdir=True))
        assert(repo_dir(repo, "objects", mkdir=True))
        assert(repo_dir(repo, "refs", "tags", mkdir=True))
        assert(repo_dir(repo, "refs", "heads", mkdir=True))

        #.git/description
        with open(repo_file(repo, "description"), "w") as f:
            f.write("Unnamed repository; edit this file 'description to name the repository. \n")

        #.git/HEAD
        with open(repo_file(repo, "HEAD"), "w") as f:
            f.write("ref: refs/heads/master \n")

        with open(repo_file(repo, "config"), "w") as f:
            config = repo_default_config()
            config.write(f)

        return repo