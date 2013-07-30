
import os.path
import shutil 
import sys

fileTypes = (video, audio, images, documents, archive, code, others,) = range(7)
#Set file type priority for each of the above. 
fileTypesPriority = (5, 5, 1, 5, 5 ,10, 1) 
#names of the folders for each type. 
folders = { video:"video", audio:"audio", images:"images", documents:"documents", archive:"archive", code:"code", others:"others"} 
audioTypes = [".mp3",".wav" , ".wma" , ".mp2" , ".flac" ]
videoTypes = [".3gpp", ".mp4", ".mov", ".wmv", ".avi", ".dat" , ".mpg" , ".mpeg" , ".mkv" , ".avi"  ]
imageTypes = [".png", ".jpeg", ".jpg", ".gif", ".bmp" , ".ttf" , ".svg" , ".ico"] 
archiveTypes = [".exe", ".rar", ".iso", ".rar", ".dll", ".7z", ".zip" , ".msi" , ".gz" , ".bz2" , ".tar" , ".tgz"] 
documentTypes = [".pdf", ".chm", ".djv", ".pds", ".txt", ".djvu", ".xls", ".ppt" ,".doc", ".docx", ".one" , ".mobi" , ".rtf" ] 
codeTypes = [".c" , ".cpp" , ".c++" , ".h" , ".js" , ".css" , ".java" , ".bat" , ".php", ".py", ".html", ".htm", ".xhtml" , ".obj", ".cs" , ".xml" , ".vb" , ".sln" ,".xaml", ".resx" , ".resw" , ".aspx" ]

def checkDirectory(path):
    if not os.path.exists(path):
        print "Path does not exist, please specify a valid one"
        return
    listNames = os.listdir(path)
    for name in listNames:
        fullpath = os.path.join(path, name)	
        if  os.path.isfile(fullpath) : 
            typeF = getFileType(fullpath)
            copyFile(fullpath, typeF)
        if os.path.isdir(fullpath) :
            if  name in folders.values(): 
                continue 
            typeD = getType(fullpath)
            copyDir(fullpath, typeD)
    print "\t\t\n*** Done ***\t\t\n"        

def copyFile(fullpath, typeF): 
    (path, name) = os.path.split(fullpath)
    if not name:
        return 
    newpath = os.path.join(path, folders[typeF])
    print fullpath + " --> " + newpath
    try: 
        if os.path.exists(newpath): 
            shutil.move(fullpath, newpath) 
        else: 
            os.mkdir(newpath)
            shutil.move(fullpath, newpath)
    except:
        print "unable to copy %s to %s" %(fullpath,newpath)
        print "Ignoring Error:", sys.exc_info()

def copyDir(fullpath, typeD): 
    (path, name) = os.path.split(fullpath)
    if not name:
        return
    newpath = os.path.join(path, folders[typeD])
    print fullpath + " --> " + newpath
    try:
        if os.path.exists(newpath): 
            shutil.move(fullpath, newpath) 
        else: 
            os.mkdir(newpath)
            shutil.move(fullpath, newpath)
    except:
        print "Unable to copy %s to %s" %(fullpath, newpath) 
        print "Ignoring Error" , sys.exc_info()[0] 
	
    
def getTypeDir(fullpath):
    typesList = [0.0] * len(fileTypes)
    for root, dirs, files in os.walk(fullpath) : 
        for name in files: 
            typeF = getFileType(os.path.join(root, name))
            typesList[typeF] += 1
    sumL = 0 
    for item in typesList:
        sumL += item
    i = 0
    if sumL == 0 :
        return others 
    while (i < len(typesList)) : 
        typesList[i] = (typesList[i] * 100 * fileTypesPriority[i]) / sumL  
        i += 1
    maxIndex = i = 0 
    maxL = typesList[i]
    while (i < len(typesList)) : 
        if typesList[i] > maxL : 
            maxL = typesList[i]
            maxIndex = i   
        i += 1
    return maxIndex     

def getType(path):
    listNames = os.listdir(path)
    typesList = [0.0] * len(fileTypes)
    for name in listNames:
        fullpath = os.path.join(path,name) 
        if os.path.isdir(fullpath) and not os.path.islink(fullpath):
            typesList[getType(fullpath)] += 1 
        if os.path.isfile(fullpath) :
            typesList[getFileType(fullpath)] += 1 
    sumL = 0 
    for item in typesList:
        sumL += item
    i = 0
    
    if sumL == 0: 
        return others 
    
    while (i < len(typesList)) : 
        typesList[i] = (typesList[i] * 100 * fileTypesPriority[i]) / sumL  
        i += 1
    maxIndex = i = 0 
    maxL = typesList[i]
    while (i < len(typesList)) : 
        if typesList[i] > maxL : 
            maxL = typesList[i]
            maxIndex = i   
        i += 1
    return maxIndex     
    
	
def getFileType(path): 
    ext = os.path.splitext(path)[1] 
    if not ext: 
        return others  
    ext = ext.lower()
    if ext in audioTypes: 
        return audio
    elif ext in videoTypes:
        return video 
    elif ext in imageTypes:
        return images
    elif ext in documentTypes: 
        return documents
    elif ext in archiveTypes:
        return archive 
    else:
        return others

if __name__ == "__main__" :
    if  len(sys.argv) != 2 : 
        print 'Usage :: manageDownloads \\your\\directory\\path \n'
    if  not os.path.exists( sys.argv[1] ) :
        print "Path is not a valid one \n"
    checkDirectory( sys.argv[1] )
    