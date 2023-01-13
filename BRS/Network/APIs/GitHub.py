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
from BRS.Debug.consoleLog import Debug
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
    user:str = None
    userInformation:list = None
    LocalRepository:list = None
    ListOfRepositories:list = None
    MatchedRepository:list = None
    MasterBranch:list = None
    LatestCommit:list = None
    CommitTags:list = None
    LatestTag:str = None
    #endregion
    #region   --------------------------- METHODS
    def GetUser(username):
        """
            Saves the user in the GitHub class to avoid useless requests
            To view the user's information, use "Object"
        """
        Debug.Start("GetUser")
        GitHub.username = username
        GitHub.userInformation = GitHub.Object.get_user(username)
        Debug.End()
    #------------------------------------------------
    def GetUserRepositories():
        """
            Saves all of the user's repositories inside of
            ListOfRepositories. GetUser must have been called prior
            to this function's calling.
        """
        Debug.Start("GetUserRepositories")
        if(GitHub.username == "None"):
            return "Error: GetUser not called"

        GitHub.ListOfRepositories = {}

        for repo in GitHub.userInformation.get_repos():
            GitHub.ListOfRepositories[str(repo.full_name)] = repo
        Debug.End()
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
        print("-"*50)
        print("Git Tags: ", str(nameOfRepository.get_git_tag()))

        print("-"*50)
        print("Branches:")
        for branch in nameOfRepository.get_branches(""):
            print(branch)

        print("-"*50)
        print("Latest release: ", str(nameOfRepository.get_latest_release()))
    #------------------------------------------------
    def GetLocalRepository():
        Debug.Start("GetLocalRepository")
        # Get current repository information through Git terminal
        repo_url = subprocess.run(['git', 'config', '--get', 'remote.origin.url'], capture_output=True, text=True).stdout.strip()
        repo_branch = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], capture_output=True, text=True).stdout.strip()
        repo_commit_hash = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], capture_output=True, text=True).stdout.strip()
        repo_version = subprocess.run(['git', 'describe', '--tags', '--abbrev=0'], capture_output=True, text=True).stdout.strip()
        repo_name = ""

        # Get name of repository
        parsedLink = repo_url.split("/")
        for word in parsedLink:
            if ".git" in word:
                repo_name = word.replace(".git", "")

        # Save local repository's information in the GitHub class.
        GitHub.LocalRepository = {"url": repo_url, "branch": repo_branch, "commit_hash": repo_commit_hash, "version": repo_version, "name": repo_name}
        Debug.End()
    #------------------------------------------------
    def GetMatchingRepository() -> str:

        # [Step 0]: Check if the needed information is present.
        if(GitHub.LocalRepository == None):
            return "The local repository was not initialized."

        if(GitHub.userInformation == None):
            return "No GitHub users were initialized."

        if(GitHub.ListOfRepositories == None):
            return "User's repositories were not initialized"

        # [Step 1]: Find the matching repository names in the list of repositories
        wanted = GitHub.LocalRepository["name"]
        gotten = ""

        for name,repo in GitHub.ListOfRepositories.items():
            if wanted in name:
                GitHub.MatchedRepository = repo
                return "GOOD"

        return "No matching repositories"
    #------------------------------------------------
    def GetMatchingRepositoryTag() -> None:
        Debug.Start("GetMatchingRepositoryTag")

        Debug.Log("Getting master branch")
        GitHub.MasterBranch = GitHub.MatchedRepository.get_branch("master")

        Debug.Log("Getting latest commit of the master branch")
        GitHub.LatestCommit = GitHub.MasterBranch.commit

        Debug.Log("Getting the tags of that latest commit")
        GitHub.CommitTags = GitHub.MatchedRepository.get_tags()

        Debug.Log("Getting the latest tag of that commit")
        GitHub.LatestTag = sorted(GitHub.CommitTags, key=lambda t: t.commit.commit.committer.date)[-1]
        GitHub.LatestTag = GitHub.LatestTag.name
        # Debug.Log("Latest tag is: ", GitHub.LatestTag)

        Debug.End()
    #------------------------------------------------
    def GetAll(username:str = "LyamBRS") -> int:
        """
        Initializes GitHub class automatically.
        it will return 0 if everything went well and 1 if an error occured.

        Make sure the repository is cloned from GitHub and not initialized.
        Otherwise, it will be impossible to get the name of the repository.

        it will use LyamBRS as the default username.
        """
        Debug.Start("GetAll")
        # [Step 1]: Getting local repository's information.
        GitHub.GetLocalRepository()

        # [Step 2]: Getting GitHub user's information.
        GitHub.GetUser(username)

        # [Step 3]: Getting all repositories of the specified user
        GitHub.GetUserRepositories()

        # [Step 4]: Checking if the local repository exist within the user's repositories.
        GitHub.GetMatchingRepository()

        # [Step 5]: Get the latest tag of the repository
        GitHub.GetMatchingRepositoryTag()

        Debug.Log("Latest tag: " + str(GitHub.LatestTag))
        Debug.End()
    #------------------------------------------------
    def CheckIfBehind() -> bool:
        """_summary_
            Checks if the repository needs updating
        Returns:
            bool: True = Repository is behind and needs updating.
            str: Error message
        """
        if(GitHub.userInformation == None):
            return "GetAll was not called properly"

        if(GitHub.LatestTag == None):
            return "No tags to compare with"

        if(GitHub.LocalRepository["version"] >= GitHub.LatestTag):
            return False

        if(GitHub.LocalRepository["version"] < GitHub.LatestTag):
            return True
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass