"""
    Allows you to keep track of which file is loading which files when starting your application
"""

class LoadingLog:
    #region --------------------------------- MEMBERS
    _currentDepth = 0
    _indentationStyle = "!\t"
    #endregion

    def Start(fileName:str):
        '''Indicates the start of a debugging chain for fast, auto indentation that doesn't rely on getting the stack size'''
        LoadingLog.Log("["+fileName+"]:")
        LoadingLog._currentDepth = LoadingLog._currentDepth + 1
        pass

    def End(fileName:str):
        '''Closes an indentation when debugging. Put this at the end of debugged functions, along with a start at the top'''
        if LoadingLog._currentDepth > 0:
            indentation = ""

            LoadingLog._currentDepth = LoadingLog._currentDepth - 1
            if LoadingLog._currentDepth > 0:
                for x in range(0, LoadingLog._currentDepth):
                    indentation = indentation + LoadingLog._indentationStyle
            print(indentation + f"~")
        pass

    def Log(logged:str):
        #Calculate and create indentations
        indentation = ""
        if LoadingLog._currentDepth > 0:
            for x in range(0, LoadingLog._currentDepth):
                indentation = indentation + LoadingLog._indentationStyle

        print(indentation + logged)