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
def StringToGitLink(textToParse:str) -> str:
    """
        StringToGitLink:
        ================
        Summary:
        --------
        This function's purpose
        is to transform and validate a given
        string into a valid git repository link
        that can be used with git clone console
        commands.

        Warning:
        --------
        This really isn't perfect at all.
        It can add missing https:// or github.com to the
        links given, or missing .git at the end but any
        special git link that isn't from github https won't work
        greatly.

        Example:
        --------
        - `"amongus"` -> Invalid
        - `"LyamBRS/among_us"` -> "https://github.com/LyamBRS/among_us.git"

        Returns:
        --------
        - `Execution.Failed` = Invalid string given.
        - `str` = Parsed git string
    """
    if(type(textToParse) != str):
        raise(Exception(f"[BRS]: You tried giving {textToParse} to StringToGitLink. This function only accepts str typed variables as input parameter."))

    # Check if string has / in it.
    if ("/" not in textToParse):
        return Execution.Failed

    # Is there .git at the end?
    if (not textToParse.endswith(".git")):
        textToParse = textToParse + ".git"

    # Is there a git hosting website name in the link? "github.com"
    if (not ".com" in textToParse):
        if(textToParse.startswith("/")):
            textToParse = "github.com" + textToParse
        else:
            textToParse = "github.com/" + textToParse

    # There is no HTTPS in the text given.
    if (not "https://" in textToParse):
        textToParse = "https://" + textToParse

    return textToParse
# ----------------------------------------------------------------
def RepoLinkIsValid(linkToVerify:str) -> bool:
    """
        IsRepoLinkValid:
        ================
        Summary:
        --------
        This function uses `git ls-remote` to verify
        the validity of a given repository link. If
        your internet connection is not valid, links
        cannot be verified.

        Returns:
        --------
        - `True` -> Repository is valid and can be accessed.
        - `False` -> Repository is not valid or can't be accessed.
    """
    if(type(linkToVerify) != str):
        raise(Exception(f"[BRS]: You tried giving {linkToVerify} to RepoLinkIsValid. This function only accepts str typed variables as input parameter."))

    result = subprocess.run(f"git ls-remote {linkToVerify}")
    if(result.returncode != 0):
        return False
    else:
        return True

def GetRepoFromLink(repositoryLink:str) -> str:
    """
        GetRepoFromLink:
        ================
        Summary:
        --------
        This function's purpose is to extract
        the name of a repository from a `git clone`
        compatible git repository link. The function
        will throw an exception if anything else
        than a string is given to it.
    """
    if(type(repositoryLink) != str):
        raise(Exception(f"[BRS]: You tried giving {repositoryLink} to GetRepoFromLink. This function only accepts str typed variables as input parameter."))

    repositoryLink = repositoryLink.strip()
    repositoryLink = repositoryLink.replace(".git", "")
    repository = repositoryLink.split("/")[-1]
    return repository
# ----------------------------------------------------------------
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
# ----------------------------------------------------------------
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
    
    def GetLocalVersion() -> str:
        """
            GetLocalVersion:
            ================
            Summary:
            --------
            This function returns the version of your
            Kontrol branch (usually master) in the
            form of a string. If no branch release
            version is found, `"None"` is returned.

            Returns:
            --------
            String containing Kontrol's release version.
        """
        Debug.Start("ManualGitHub -> GetLocalVersion")

        Debug.End()
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
    LocalRepository:list = {"url": None, "branch": None, "commit_hash": None, "version": None, "name": None}
    """
        LocalRepository:
        ================
        Summary:
        --------
        A list of the local repository's information.
        This list is updated when `GetLocalRepository` is called.

        Default:
        --------
        `{"url": None, "branch": None, "commit_hash": None, "version": None, "name": None}`
        - `"url"`: .git url to the repository
        - `"branch"`: Name of the local branch (example: "master")
        - `"commit_hash"`: The local branch's commit value
        - `"version"`: The local branch's release version (example: "0.0.0")
        - `"name"`: The name of the local branch (example: "brs-kontrol")
    """
    ListOfRepositories:list = None
    MatchedRepository:list = None
    MasterBranch:list = None
    LatestCommit:list = None
    CommitTags:list = None

    LatestTag:str = None
    """ The latest release available on GitHub. For example: "0.0.0" """
    CurrentTag:str = None
    """ The local tag of Kontrol's release saved locally. For example: "0.0.0" """

    LatestError:str = "None"
    """Stores the latest error that happened while using this class"""
    #endregion
    #region   --------------------------- METHODS
    def GetUser(username:str):
        """
            GetUser:
            ========
            Summary:
            --------
            Gets a user's object and updates the GitHub class
            with it to avoid useless API requests. To view
            the user's information, use `GitHub.Object`.

            Args:
            -----
            - `username` = the username which published the device's branch.
        """
        Debug.Start("GetUser")
        GitHub.username = username
        try:
            GitHub.userInformation = GitHub.Object.get_user(username)
            Debug.Log("Username: {username}")
        except:
            Debug.Error(f"Could not get username")
            GitHub.LatestError = "Could not get username"
            Debug.End()
            return "Could not get username"
        Debug.End()
    #------------------------------------------------
    def GetUserRepositories():
        """
            GetUserRepositories:
            ====================
            Summary:
            --------
            Saves all of the user's repositories inside of
            `ListOfRepositories`. `GetUser()` must have
            been called prior to this function's calling.
            Otherwise, the function has no idea which user
            to get repositories from.

            Returns:
            --------
            - `None`: No errors occured while executing.
            - `(str)`: Description of what went wrong.
        """
        Debug.Start("GetUserRepositories")
        try:
            if(GitHub.username == None):
                GitHub.LatestError = "No username stored in the GitHub class. Make sure to call GetAll"
                Debug.Error(GitHub.LatestError)
                Debug.End()
                return GitHub.LatestError
        except:
            GitHub.LatestError = "Error occured while getting username"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        try:
            if(GitHub.userInformation == None):
                GitHub.LatestError = "No user information were stored. Verify network connected and call GetAll"
                Debug.Error(GitHub.LatestError)
                Debug.End()
                return GitHub.LatestError
        except:
            GitHub.LatestError = "ERROR while getting user information"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

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
        """
            GetLocalRepository:
            ===================
            Summary:
            --------
            This method's purpose is to get the
            information from the repository which
            currently host this python script. It
            will gather its information, especially
            its release tag and store it in the
            `GitHub` class.

            See:
            - `GitHub.CurrentTag`: The local branch's release
            - `GitHub.LocalRepository`: The local branch's information

            Returns:
            --------
            - `None`: No errors occurred while executing.
            - `(str)`: Description of what went wrong.
        """

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
        """
            GetMatchingRepository:
            ======================
            Summary:
            --------
            This method's purpose is to find a repository
            in the list gathered when `GetUserRepositories`
            that matches the local repository found when
            `GetLocalRepository` was called.

            Returns:
            --------
            - `(str)`: Name of the repository that matched
            - `(str)`: Error that occured when calling this method.
        """
        Debug.Start("GetMatchingRepository")
        # [Step 0]: Check if the needed information is present.
        if(GitHub.LocalRepository == None):
            GitHub.LatestError = "The local repository was not initialized."
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        if(GitHub.userInformation == None):
            GitHub.LatestError = "No GitHub users were initialized."
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        if(GitHub.ListOfRepositories == None):
            GitHub.LatestError = "User's repositories were not initialized"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        # [Step 1]: Find the matching repository names in the list of repositories
        wanted = GitHub.LocalRepository["name"]
        gotten = ""

        for name,repo in GitHub.ListOfRepositories.items():
            if wanted in name:
                Debug.Log(f"Found matching repository: {repo}")
                GitHub.MatchedRepository = repo
                Debug.End()
                return None

        GitHub.LatestError = "No matching repositories. Make sure you are using a cloned repository."
        Debug.Error(GitHub.LatestError)
        Debug.End()
        return GitHub.LatestError
    #------------------------------------------------
    def GetMatchingRepositoryTag() -> None:
        """
            GetMatchingRepositoryTag:
            =========================
            Summary:
            --------
            Method that gets the release
            tags of the matching repository
            found when `GetMatchingRepository`
            was called.

            Returns:
            --------
            - (str): Error that occurred while executing this method
            - None : No error occurred while executing this method
        """
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
            GitHub.LatestError = "Failed to get master branch of matched repository"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        Debug.Log("Getting latest commit of the master branch")
        try:
            GitHub.LatestCommit = GitHub.MasterBranch.commit
            Debug.Log("Latest commit found")
        except:
            GitHub.LatestError = "Failed to get master branch's commits"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        Debug.Log("Getting the tags of that latest commit")
        try:
            GitHub.CommitTags = GitHub.MatchedRepository.get_tags()
            Debug.Log("Found tags of matching repository")
        except:
            GitHub.LatestError = "Failed to get tags of the matching repository"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError
        Debug.Log(f"CommitTags = {GitHub.CommitTags}")

        Debug.Log("Getting the latest tag of that commit")
        try:
            GitHub.LatestTag = sorted(GitHub.CommitTags, key=lambda t: t.commit.commit.committer.date)[-1]
            GitHub.LatestTag = GitHub.LatestTag.name
            Debug.Log(f"Found latest tag of repository: {GitHub.LatestTag}")
        except:
            GitHub.LatestError = "Failed to sort repositories commit tags"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return GitHub.LatestError

        Debug.Log("Success")
        Debug.End()
    #------------------------------------------------
    def GetAll(username:str = "LyamBRS") -> int:
        """
            GetAll:
            =======
            Summary:
            --------
            Initializes GitHub class automatically.
            it will return `None` if everything went well and a message if an error occurred.

            Make sure the local repository is cloned from GitHub and not initialized.
            Otherwise, it will be impossible to get the name of the repository.

            Arguments:
            ----------
            - `username:str` = Github username that will initialize this class. Defaults to `"LyamBRS"`
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
        Debug.Start("CheckIfBehind")
        if(GitHub.userInformation == None):
            GitHub.LatestError = "user information member not set up properly."
            Debug.Error("user information member not set up properly.")
            Debug.End()
            return GitHub.LatestError

        if(GitHub.LatestTag == None):
            GitHub.LatestError = "No latest tags found to compare local tag with"
            Debug.Error("No latest tags found to compare local tag with")
            Debug.End()
            return GitHub.LatestError

        if(GitHub.LocalRepository["version"] > GitHub.LatestTag):
            Debug.Error("Version of local repository is higher than latest tag. UPDATE IT ANYWAYS BRUH.")
            Debug.End()
            return True

        if(GitHub.LocalRepository["version"] < GitHub.LatestTag):
            Debug.Error("Version is behind and needs to be updated.")
            Debug.End()
            return True
        
        Debug.End()
        return False
    #------------------------------------------------
    def UpdateDevice():
        """
            UpdateDevice:
            =============
            Summary:
            --------
            Deprecated method which used allow a simple
            `git pull -- rebase` of the current branch.

            `ATTENTION`
            -----------
            This method is no longer used but is kept
            here for various reasons such as old code
            needing it. Please abstain from using it
            in any circumstances. Also note that it
            does not pull recursively meaning submodules
            will not get updated. Also note that the
            pull is executed at run time meaning that
            programs currently executing may experience
            errors.
        """

        Debug.Start("UpdateDevice")
        gitStuff = subprocess.run(['git', 'pull', "--rebase"])
        if(gitStuff == 0):
            Debug.Log("Pull successfull")
        else:
            GitHub.LatestError = "Failed to execute git pull."
            Debug.Error(GitHub.LatestError)

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
            GitHub.LatestError = "Could not execute: get_rate_limit"
            Debug.Error(GitHub.LatestError)
            Debug.End()
            return False
    #endregion
    #region   --------------------------- CONSTRUCTOR
    #endregion
    pass
#====================================================================#
LoadingLog.End("GitHub.py")