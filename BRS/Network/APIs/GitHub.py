#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
import requests
import subprocess
import base64
from github import Github as git
#====================================================================#
# Functions
#====================================================================#

#====================================================================#
# Classes
#====================================================================#
class GitHub:
    #region   --------------------------- DOCSTRING
    '''
    '''
    #endregion
    #region   --------------------------- MEMBERS
    Object = git()
    user = "None"
    userInformation = "None"
    ListOfRepositories = {}
    #endregion
    #region   --------------------------- METHODS
    def GetUser(username):
        """
            Saves the user in the GitHub class to avoid useless requests
            To view the user's information, use "Object"
        """
        GitHub.username = username
        GitHub.userInformation = GitHub.Object.get_user(username)
    #------------------------------------------------
    def GetUserRepositories():
        """
            Saves all of the user's repositories inside of
            ListOfRepositories. GetUser must have been called prior
            to this function's calling.
        """

        if(GitHub.username == "None"):
            return "Error: GetUser not called"

        for repo in GitHub.userInformation.get_repos():
            GitHub.ListOfRepositories[str(repo.full_name)] = repo
    #------------------------------------------------
    def GetRepositoryInformation(nameOfRepository):
        # repository full name
        print("Full name:", nameOfRepository.full_name)
        # repository description
        print("Description:", nameOfRepository.description)
        # the date of when the repo was created
        print("Date created:", nameOfRepository.created_at)
        # the date of the last git push
        print("Date of last push:", nameOfRepository.pushed_at)
        # home website (if available)
        print("Home Page:", nameOfRepository.homepage)
        # programming language
        print("Language:", nameOfRepository.language)
        # number of forks
        print("Number of forks:", nameOfRepository.forks)
        # number of stars
        print("Number of stars:", nameOfRepository.stargazers_count)
        print("-"*50)
        # repository content (files & directories)
        print("Contents:")
        for content in nameOfRepository.get_contents(""):
            print(content)
        try:
            # repo license
            print("License:", base64.b64decode(nameOfRepository.get_license().content.encode()).decode())
        except:
            pass
    #------------------------------------------------
    def GetLocalRevisionNumber() -> str:
        repo_url = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.strip()
        repo_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True).stdout.strip()
        repo_commit_hash = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
        repo_version = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True).stdout.strip()
        return {"url": repo_url, "branch": repo_branch, "commit_hash": repo_commit_hash, "version": repo_version}
    #------------------------------------------------
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass