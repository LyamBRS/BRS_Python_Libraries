"""
    pythonKiller.py
    ===============
    Summary:
    --------
    This file contains a function
    that kills the python interpreter
    if something incredibly bad happens.

    This is to be used if your application
    crashes but threads are still running.
    This will kill the threads preventing
    your device from being frozen with the
    app never terminating.

    Warning:
    --------
    There is high chances that this will kill
    ALL python processes running including
    services running in python on your device.
    BE VERY FUCKING CAREFUL, this is a last
    resort moment that you should be using
    only when debugging.
"""

def KillPython():
    """
        KillPython:
        ========================
        Summary:
        --------
        This function's purpose
        is to force close the
        python interpreter
        currently running your
        script by force.
    """
    import os
    import signal
    os.kill(os.getpid(), signal.SIGINT)

