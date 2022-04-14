def printPrettyMatrix(objStr, matrix):
    objStr+="\t\t["   
    for row in matrix:
        objStr+="["
        for col in row:
             objStr+=f" {col:.02f},"
        objStr= objStr[:-1]+"],"
        objStr+="\n \t\t"
    objStr=objStr[:-5]+"]" 
    return objStr  