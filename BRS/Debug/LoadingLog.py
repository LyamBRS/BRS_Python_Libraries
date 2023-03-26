"""
    Allows you to keep track of which file is loading which files when starting your application
"""
from colorama import Fore, Back, Style

class LoadingLog:
    #region --------------------------------- MEMBERS
    _currentDepth = 0
    _indentationStyle = "!\t"
    useANSI = False

    _start      = "START   "
    _end        = "END     "
    _log        = "LOG     "
    _class      = "CLASS   "
    _function   = "FUNCTION"
    _import     = "IMPORT  "
    _variable   = "VARIABLE"
    _method     = "METHOD  "
    _member     = "MEMBER  "
    #endregion
    #region --------------------------------- Methods
    def Start(fileName:str):
        '''
            Start:
            ======
            Summary:
            --------
            Indicates the start of a debugging chain
            for fast, auto indentation that doesn't
            rely on getting the stack size to indent
            itself.
            Don't forget to call :ref:`End`
        '''
        LoadingLog._print(LoadingLog._start, fileName, "File", Fore.LIGHTRED_EX)
        LoadingLog._currentDepth = LoadingLog._currentDepth + 1
        pass
    # ------------------------------------------------
    def End(fileName:str):
        '''
            End:
            ====
            Summary:
            --------
            Closes an indentation when debugging.
            Put this at the end of debugged functions,
            along with a start at the top of them
        '''
        if(LoadingLog._currentDepth > 0):
            LoadingLog._currentDepth = LoadingLog._currentDepth - 1
        LoadingLog._print(LoadingLog._end, "~", "End", Fore.LIGHTRED_EX)
    # -------------------------------------------------
    def Log(logged:str):
        '''
            Log:
            ====
            Summary:
            --------
            Legacy logging method which simply adds a
            message in the terminal defined by the
            input variable: logged. Do not use this
            anymore.
        '''
        LoadingLog._print(LoadingLog._log, logged, "Log", Fore.WHITE)
    # -------------------------------------------------
    def Class(className:str):
        '''
            Class:
            ======
            Summary:
            --------
            Put this before a class definition for it
            to be logged when your application starts.
        '''
        LoadingLog._print(LoadingLog._class, className, "Class", Fore.GREEN)
    # -------------------------------------------------
    def Function(functionName:str):
        '''
            Function:
            =========
            Summary:
            --------
            Put this before a function definition for it
            to be logged when your application starts.
        '''
        LoadingLog._print(LoadingLog._function, functionName, "Function", Fore.YELLOW)
    # -------------------------------------------------
    def Import(importName:str):
        '''
            Import:
            =======
            Summary:
            --------
            Put this before an import for it
            to be logged when your application starts.
        '''
        LoadingLog._print(LoadingLog._import, importName, "Import", Fore.MAGENTA)
    # -------------------------------------------------
    def GlobalVariable(globalVariable:str):
        '''
            GlobalVariable:
            ===============
            Summary:
            --------
            Put this before a global variable for it
            to be logged when your application starts.
        '''
        LoadingLog._print(LoadingLog._variable, globalVariable, "GlobalVariable", Fore.CYAN)
    # -------------------------------------------------
    def Method(methodName:str):
        '''
            Method:
            =======
            Summary:
            --------
            Put this before a Method for it
            to be logged when your application starts.
        '''
        #Calculate and create indentations
        LoadingLog._print(LoadingLog._method, f"    {methodName}", "Method", Fore.LIGHTYELLOW_EX)
    # -------------------------------------------------
    def Member(memberName:str):
        '''
            Member:
            =======
            Summary:
            --------
            Put this before a Member for it
            to be logged when your application starts.
        '''
        LoadingLog._print(LoadingLog._member, f"    {memberName}", "Member", Fore.LIGHTCYAN_EX)
    # -------------------------------------------------
    def _print(header:str, message:str, messageStyle:str,  color):
        #Calculate and create indentations
        indentation = "" 
        if LoadingLog._currentDepth > 0:
            for x in range(0, LoadingLog._currentDepth):
                indentation = indentation + LoadingLog._indentationStyle

        if(LoadingLog.useANSI):
            message = f"{color}{message}{Fore.RESET}"
            header = f"[{color}{header}{Fore.RESET}]"
            indentation = f"{Fore.LIGHTBLACK_EX}{indentation}{Fore.RESET}"
        else:
            header = f"[{header}]"

        if(messageStyle == "File"):
            message = f"[{message}]:"
        elif(messageStyle == "Class"):
            message = f"({message}):"
        elif(messageStyle == "End"):
            message = f"[END]"
        elif(messageStyle == "Member" or messageStyle == "Method"):
            message = f"    > {message}"
        else:
            message = f"> {message}"

        print(f"{header}{indentation}{message}")
    #endregion