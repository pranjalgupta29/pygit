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
    