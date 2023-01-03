
class Debug:
    #region --------------------------------- MEMBERS
    enableConsole = False
    _currentDepth = 0
    _indentationStyle = "|\t"
    #endregion

    def Start():
        '''Indicates the start of a debugging chain for fast, auto indentation that doesn't rely on getting the stack size'''
        if Debug.enableConsole == True:
            Debug._currentDepth = Debug._currentDepth + 1
        pass

    def End():
        '''Closes an indentation when debugging. Put this at the end of debugged functions, along with a start at the top'''
        if Debug.enableConsole == True and Debug._currentDepth > 0:
            Debug._currentDepth = Debug._currentDepth - 1
        pass

    def Log(logged:str):
        if Debug.enableConsole:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            print(indentation + logged)
        pass

    def Warn(logged:str):
        if Debug.enableConsole:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            print(indentation + " [WARNING]:\t" + logged)
        pass

    def Error(logged:str):
        if Debug.enableConsole:
            #Calculate and create indentations
            indentation = ""
            if Debug._currentDepth > 0:
                for x in range(0, Debug._currentDepth):
                    indentation = indentation + Debug._indentationStyle

            print(indentation + " [ERROR]:\t" + logged)
        pass