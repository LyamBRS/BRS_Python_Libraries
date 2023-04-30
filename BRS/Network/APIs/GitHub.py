#====================================================================#
# File Information
#====================================================================#

#====================================================================#
# Imports
#====================================================================#
import subprocess
import base64
import asyncio
import threading
import git
from github import Github as Git
from ...Debug.consoleLog import Debug
from ...Debug.LoadingLog import LoadingLog
from ...Utilities.Enums import GitHubFail
from ...Utilities.Enums import Execution
from kivymd.uix.progressbar import MDProgressBar
LoadingLog.Start("GitHub.py")
#====================================================================#
# Functions
#====================================================================#
def DownloadRepositoryAtPath(gitUrl:str, downloadPath:str, progressBar: MDProgressBar, DownloadProgressHandler) -> Execution:
    """
        DownloadRepositoryAtPath:
        ========================
        Summary:
        --------
        This function will download any Git URL at a specified
        path location. You can also specify a callback function
        which will be executed each time something happens
        during the download progress.

        Parameters:
        -----------
        - `gitUrl` = Url to clone the repository from
        - `downloadPath` = system path where the repository will be cloned
        - `progressBar` : MDProgressbar updated by download functions running asynchronously. This way your kivy app gets a live update of the download's progression.
        - `DownloadProgressHandler`: a class which contains : GoodDownload() and FailedDownload()

        Returns:
        --------
        - `Execution.Passed` = Repository successfully downloaded at specified path.
        - `Execution.Failed` = Something failed during download process.
        - `Execution.NoConnection` = Cannot download due to no internet access.
        - `Execution.APIRanOutOfRequest` = Cannot download due to no API requests left.
    """
    Debug.Start("DownloadRepositoryAtPath")
    Debug.Log("Starting async process")

    # Call the download_git_repo_async function asynchronously
    _start_download_thread(repo_url=gitUrl,
                            local_path=downloadPath,
                            progressBar=progressBar,
                            DownloadProgressHandler=DownloadProgressHandler)

    Debug.End()
    return Execution.Passed
# ----------------------------------------------------------------
def _start_download_thread(repo_url: str, local_path: str, progressBar: MDProgressBar, DownloadProgressHandler):

    class PassedValues():
        result = Execution.ByPassed
    # Define the function to run in the separate thread
    def download_thread():
        # Create a new event loop for this thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        # Define the progress update function for the callback
        def update_progress(op_code, cur_count, max_count=None, message=''):
            # Update the progress bar with the current progress
            progress = cur_count / max_count if max_count else 0
            progressBar.value = progress * 100

        # Call the download_git_repo_async function asynchronously with the progress update callback
        loop.run_until_complete(_download_git_repo_async(repo_url, local_path, update_progress, PassedValues))

        # Stop the event loop
        loop.stop()
        loop.close()
        
        if(loop.is_running()):
            print("What? loop is still running... interesting")
        else:
            if(loop.is_closed()):
                print("Loop is closed!")
            else:
                print("Loop isnt running but isnt closed? what the fuck?")

        print("FINISHED")
        if(PassedValues.result == Execution.Passed):
            DownloadProgressHandler.downloadResult = Execution.Passed
        else:
            DownloadProgressHandler.downloadResult = Execution.Failed
        progressBar.value = progressBar.max

    # Start a new thread for the download function
    thread = threading.Thread(target=download_thread)
    thread.start()

async def _download_git_repo_async(repo_url: str, local_path: str, callback_fn=None, passedClass=None) -> Execution:
    try:
        # Clone the Git repository asynchronously
        async def download():
            git.Repo.clone_from(repo_url, local_path, progress=callback_fn, recursive=True)

        await asyncio.create_task(download())
        # Create a new repo object from the local path and return the execution status
        git.Repo(local_path)
        passedClass.result = Execution.Passed
        return Execution.Passed
    except Exception as e:
        print(f"Failed to download Git repo: {e}")
        passedClass.result = Execution.Failed
        return Execution.Failed
#====================================================================#
# Classes
#====================================================================#
class ManualGitHub:
    #region   --------------------------- DOCSTRING
    '''
        ManualGitHub:
        =============
        Summary:
        --------
        This class holds manual functions used to facilitate
        the use of the GitHub API functions without the need of
        setting up credentials or various other step based inputs
        like the regular GitHub class.
    '''
    #endregion
    #region   --------------------------- METHODS
    def GetRequestsLeft() -> int:
        """
            GetRequestsLeft:
            ================
            Summary:
            --------
            This function returns how many requests the GitHub
            API has left. it will return 0 if no internet
            connection can be established or if an error occured.
        """
        Debug.Start("ManualGitHub -> GetRequestsLeft")
        object = Git()
        rateLimit = object.get_rate_limit()
        remaining = rateLimit.core.remaining
        Debug.End()
        return remaining
    #endregion
#====================================================================#
class GitHub:
    #region   --------------------------- DOCSTRING
    '''
    '''
    #endregion
    #region   --------------------------- MEMBERS
    Object = Git()
    user:str = None
    userInformation:list = None
    LocalRepository:list = None
    ListOfRepositories:list = None
    MatchedRepository:list = None
    MasterBranch:list = None
    LatestCommit:list = None
    CommitTags:list = None
    LatestTag:str = None
    CurrentTag:str = None

    LatestError:str = "None"
    """Stores the latest error that happened while using this class"""
    #endregion
    #region   --------------------------- METHODS
    def GetUser(username):
        """
            Saves the user in the GitHub class to avoid useless requests
            To view the user's information, use "Object"
        """
        Debug.Start("GetUser")
        GitHub.username = username
        try:
            GitHub.userInformation = GitHub.Object.get_user(username)
            Debug.Log("Username: {username}")
        except:
            Debug.Error(f"Could not get username")
            Debug.End()
            return "Could not get username"
        Debug.End()
    #------------------------------------------------
    def GetUserRepositories():
        """
            Saves all of the user's repositories inside of
            ListOfRepositories. GetUser must have been called prior
            to this function's calling.
        """
        Debug.Start("GetUserRepositories")
        try:
            if(GitHub.username == None):
                Debug.Error("No username stored in the GitHub class. Make sure to call GetAll")
                Debug.End()
                return "No username stored in the GitHub class. Make sure to call GetAll"
        except:
            Debug.Error("ERROR while getting username")
            Debug.End()
            return "Error occured while getting username"

        try:
            if(GitHub.userInformation == None):
                Debug.Error("No user information were stored. Verify network connected and call GetAll")
                Debug.End()
                return "No user information were stored. Verify network connected and call GetAll"
        except:
            Debug.Error("ERROR while getting user informations")
            Debug.End()
            return "Error occured while getting user information"

        GitHub.ListOfRepositories = {}

        Debug.Log(f"Repositories of user: {GitHub.username}")
        for repo in GitHub.userInformation.get_repos():
            Debug.Log(f"Found: {repo}")
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
        # the date of the last Git push
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

        GitHub.CurrentTag = repo_version

        Debug.Log(f"repository name:    {repo_name}")
        Debug.Log(f"repository version: {repo_version}")
        Debug.Log(f"repository branch:  {repo_branch}")
        # Save local repository's information in the GitHub class.
        GitHub.LocalRepository = {"url": repo_url, "branch": repo_branch, "commit_hash": repo_commit_hash, "version": repo_version, "name": repo_name}
        Debug.End()
    #------------------------------------------------
    def GetMatchingRepository() -> str:
        Debug.Start("GetMatchingRepository")
        # [Step 0]: Check if the needed information is present.
        if(GitHub.LocalRepository == None):
            Debug.Error("The local repository was not initialized.")
            Debug.End()
            return "The local repository was not initialized."

        if(GitHub.userInformation == None):
            Debug.Error("No GitHub users were initialized.")
            Debug.End()
            return "No GitHub users were initialized."

        if(GitHub.ListOfRepositories == None):
            Debug.Error("User's repositories were not initialized")
            Debug.End()
            return "User's repositories were not initialized"

        # [Step 1]: Find the matching repository names in the list of repositories
        wanted = GitHub.LocalRepository["name"]
        gotten = ""

        for name,repo in GitHub.ListOfRepositories.items():
            if wanted in name:
                Debug.Log(f"Found matching repository: {repo}")
                GitHub.MatchedRepository = repo
                Debug.End()
                return None

        Debug.Error("No matching repositories. Make sure you are using a cloned repository.")
        Debug.End()
        return "No matching repositories. Make sure you are using a cloned repository."
    #------------------------------------------------
    def GetMatchingRepositoryTag() -> None:
        Debug.Start("GetMatchingRepositoryTag")

        if(GitHub.MatchedRepository == None):
            Debug.Error("No matched repositories to use. Make sure you are using a cloned repository.")
            Debug.End()
            return "No matched repositories to use. Make sure you are using a cloned repository."

        Debug.Log("Getting master branch")
        try:
            GitHub.MasterBranch = GitHub.MatchedRepository.get_branch("master")
            Debug.Log("Master branch found")
        except:
            Debug.Error("Failed to get master branch of matched repository")
            Debug.End()
            return "Failed to get master branch of matched repository"

        Debug.Log("Getting latest commit of the master branch")
        try:
            GitHub.LatestCommit = GitHub.MasterBranch.commit
            Debug.Log("Latest commit found")
        except:
            Debug.Error("Failed to get master branch's commits")
            Debug.End()
            return "Failed to get master branch's commits"

        Debug.Log("Getting the tags of that latest commit")
        try:
            GitHub.CommitTags = GitHub.MatchedRepository.get_tags()
            Debug.Log("Found tags of matche repository")
        except:
            Debug.Error("Failed to get tags of the matching repository")
            Debug.End()
            return "Failed to get tags of the matching repository"
        Debug.Log(f"CommitTags = {GitHub.CommitTags}")

        Debug.Log("Getting the latest tag of that commit")
        try:
            GitHub.LatestTag = sorted(GitHub.CommitTags, key=lambda t: t.commit.commit.committer.date)[-1]
            GitHub.LatestTag = GitHub.LatestTag.name
            Debug.Log(f"Found latest tag of repository: {GitHub.LatestTag}")
        except:
            Debug.Error("Failed to sort repositories commit tags")
            Debug.End()
            return "Failed to sort repositories commit tags"

        Debug.Log("Success")
        Debug.End()
    #------------------------------------------------
    def GetAll(username:str = "LyamBRS") -> int:
        """
        Initializes GitHub class automatically.
        it will return `None` if everything went well and a message if an error occured.

        Make sure the repository is cloned from GitHub and not initialized.
        Otherwise, it will be impossible to get the name of the repository.

        it will use LyamBRS as the default username.
        """
        Debug.Start("GetAll")
        # [Step 1]: Getting local repository's information.
        error = GitHub.GetLocalRepository()
        if(error != None):
            Debug.Error(error)
            Debug.End()
            return error

        # try:
        # [Step 2]: Getting GitHub user's information.
        error = GitHub.GetUser(username)
        if(error != None):
            Debug.Error(error)
            Debug.End()
            return error

        # [Step 3]: Getting all repositories of the specified user
        error = GitHub.GetUserRepositories()
        if(error != None):
            Debug.Error(error)
            Debug.End()
            return error

        # [Step 4]: Checking if the local repository exist within the user's repositories.
        error = GitHub.GetMatchingRepository()
        if(error != None):
            Debug.Error(error)
            Debug.End()
            return error

        # [Step 5]: Get the latest tag of the repository
        error = GitHub.GetMatchingRepositoryTag()
        if(error != None):
            Debug.Error(error)
            Debug.End()
            return error

        # except socket.error:
            # Debug.Error(f"Network Error")

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
    #------------------------------------------------
    def UpdateDevice():
        """When called, this will initiate a Git Pull."""
        Debug.Start("UpdateDevice")
        gitStuff = subprocess.run(['git', 'pull', "--rebase"])
        if(gitStuff == 0):
            Debug.Log("Pull successfull")
        else:
            Debug.Error("Could not pull")

        Debug.End()
        return gitStuff
    #------------------------------------------------
    def GetRequests() -> bool:
        """
            GetRequests:
            -----------------
            This function's purpose is to check if
            GitHub's API can be accessed.

            Returns `False` if API cannot be accessed
            Returns a number correlating to the request limit available
        """
        Debug.Start("GetRequests")

        try:
            requests = GitHub.Object.get_rate_limit()
            Debug.Log(f"You have {requests.core.remaining} requests available")
            Debug.End()
            return requests.core.remaining
        except:
            Debug.Error("Could not execute: get_rate_limit")
            Debug.End()
            return False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("GitHub.py")