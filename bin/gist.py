#!/Users/nolan/.virtualenv/gist/bin/python
"""
Simple script to create a gist from a text file.
"""
from github.Github import Github
from github import InputFileContent

__author__ = "Nolan Nichols <nolan.nichols@gmail.com>"

def get_user(username, password):
    """
    Get a Github Authenticated User Object
    """
    user = Github(username, password).get_user()
    return user

def post_gist(auth, gist_file, description=None, public=True):
    """
    Post a gist
    
    Parameters
    ==========
    auth        : username and password dictionary
    gist_file   : Text file to post as a Gist  
    description : Gist description (optional)
    public      : False sets the Gist to private
    """
    f = open(gist_file)
    file_name = f.name
    content = InputFileContent(f.read())
    files = {file_name:content}

    user = get_user(auth['username'], auth['password'])
    
    if description:
        gist = user.create_gist(public, files, description)
    else:
        gist = user.create_gist(public, files)
    return gist

if __name__ == '__main__':
    import getpass
    from argparse import ArgumentParser
    from configobj import ConfigObj
    
    parser = ArgumentParser()
    parser.add_argument("gist_file", help="Text file to post as a Gist")
    parser.add_argument("-d", "--description", help="Gist description (Optional)")
    parser.add_argument("-p", "--private", help="Flags the Gist as private", action="store_false")
    args = parser.parse_args()

    GIT_CONFIG = "/Users/nolan/.gitconfig"
    config = ConfigObj(GIT_CONFIG)
    auth = dict(username = config['github']['user'],
                password = getpass.getpass())
    
    gist = post_gist(auth, args.gist_file, description=args.description, public=args.private)
    
    print "Gist available at: " + gist.html_url
        
