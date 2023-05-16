#====================================================================#
# File Information
#====================================================================#
"""
    accelerometerHandler.py
    =======================
    Summary:
    --------
    This file contains the functions and classes necessary
    for a Raspberry Pi to handle an Adafruit ADXl accelerometer
    board.
"""
#====================================================================#
# Loading Logs
#====================================================================#
from ...Debug.LoadingLog import LoadingLog
LoadingLog.Start("accelerometerHandler.py")
#====================================================================#
# Imports
#====================================================================#
#region ------------------------------------------------------ Python
LoadingLog.Import("Python")
import os
import sys
import subprocess
import time

#endregion
#region --------------------------------------------------------- BRS
LoadingLog.Import("Libraries")
from ...Utilities.Information import Information
from ...Utilities.FileHandler import JSONdata, CompareKeys, AppendPath
from ...Utilities.Enums import Execution, FileIntegrity
from ...Debug.consoleLog import Debug
#endregion
#region -------------------------------------------------------- Kivy
LoadingLog.Import("Kivy")
#endregion
#region ------------------------------------------------------ KivyMD
LoadingLog.Import('KivyMD')
#endregion
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
def _startReadingThread(accelerometerDataClass):
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

#====================================================================#
LoadingLog.End("rgbDriverHandler.py")