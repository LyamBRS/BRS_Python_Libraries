from .LoadingLog import LoadingLog
LoadingLog.Start("consoleLog.py")


class Debug:
    #region --------------------------------- MEMBERS
    enableConsole = False
    _currentDepth = 0
    _indentationStyle = "|\t"
    _DontDebugEnabled:bool = False
    #endregion

    def Start(functionName:str=None, DontDebug:bool=False):
        '''Indicates the start of a debugging chain for fast, auto indentation that doesn't rely on getting the stack size'''
        if(DontDebug):
            Debug._DontDebugEnabled = True

        if Debug.enableConsole == True and not Debug._DontDebugEnabled:
            
            if(DontDebug):
                Debug._DontDebugEnabled = True

            if(functionName != None):
                Debug.Log("["+functionName+"]:")
            Debug._currentDepth = Debug._currentDepth + 1
        pass

    def End(ContinueDebug:bool = False):
        '''Closes an indentation when debugging. Put this at the end of debugged functions, along with a start at the top'''
        if Debug.enableConsole == True and Debug._currentDepth > 0 and not Debug._DontDebugEnabled:
            indentation = ""
            Debug._currentDepth = Debug._currentDepth - 1
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle
            print(indentation + "-")

        if(ContinueDebug and Debug._DontDebugEnabled):
            Debug._DontDebugEnabled = False

    def End(functionName:str=None, ContinueDebug:bool = False):
        '''Closes an indentation when debugging. Put this at the end of debugged functions, along with a start at the top'''
        if Debug.enableConsole == True and Debug._currentDepth > 0 and not Debug._DontDebugEnabled:
            indentation = ""

            Debug._currentDepth = Debug._currentDepth - 1
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle
            if(functionName != None):
                print(indentation + f"-{functionName}-")
            else:
                print(indentation + "-")

        if(ContinueDebug and Debug._DontDebugEnabled):
            Debug._DontDebugEnabled = False

    def Log(logged:str):
        if Debug.enableConsole and not Debug._DontDebugEnabled:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            print(indentation + str(logged))
        pass

    def Warn(logged:str):
        if Debug.enableConsole and not Debug._DontDebugEnabled:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            print(indentation + "[WARNING]:\t" + logged)
        pass

    def Error(logged:str, FileName:str = None, Line:int = None):
        if Debug.enableConsole and not Debug._DontDebugEnabled:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            if(FileName != None and Line != None):
                print(f"{indentation} [ERROR -> {FileName};ln{str(Line)}]:\t {logged}")
            else:
                print(indentation + "[ERROR]:\t" + logged)
        pass

LoadingLog.End("consoleLog.py")