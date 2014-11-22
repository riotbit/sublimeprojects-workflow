#!/usr/bin/python
# encoding: utf-8

import sys

from workflow import Workflow

log = None

def main(wf):
    import subprocess

    # Get args from Workflow as normalized Unicode
    args = wf.args

    # get the paths of query matches
    project_paths = subprocess.check_output(['mdfind', 'kMDItemFSName=*.sublime-project']).splitlines()

    if not args:
        query_matches = project_paths # return all project files
    else:
        query_matches = wf.filter(args[0].encode("utf-8"), project_paths)

    # Add matches to Alfred feedback
    for match_path in query_matches:
        wf.add_item(match_path.split('/')[-1].split('.')[0], match_path, uid=match_path, arg=match_path, valid=True, icon="icon.png")

    # Send output to Alfred
    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow()
    # Assign Workflow logger to a global variable, so all module
    # functions can access it without having to pass the Workflow
    # instance around
    log = wf.logger
    sys.exit(wf.run(main))