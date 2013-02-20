#!/usr/local/bin/python
import sys, os, fnmatch, getopt, errno, platform
from shutil import copyfile

def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else: raise
        
class BuildDir:
    _files = []

    def __init__(self, buildType):
        self._buildType = buildType
        plat = platform.system()
        if (plat == "Windows"):
            self._path = "C:/users/" + os.environ['USERNAME'] + "/Dropbox/poderosa"
        else:
            self._path = "binaries/poderosa"
        print("Putting " + self._buildType + " in: " + self._path + " " + os.getcwd())
            
    def buildFileList(self, pattern):
        for root, dirnames, filenames in os.walk('.'):
            for filename in fnmatch.filter(filenames, pattern):
                f = os.path.join(root, filename)
                self._files.append(f)

    def getDir(self, filename):
        index = filename.find('\\', 2)
        if (index == -1):
            index = filename.find('/', 2)
        dir = filename[2:index]
        return dir
        
    def getFile(self, filename):
        index = filename.rfind('\\')
        if (index == -1):
            index = filename.rfind('/')
        file = filename[index+1:]
        return file
        
    def copyFiles(self, maindir):
        for filename in self._files:
            dir = self.getDir(filename)
            file = self.getFile(filename)
            if ((file.find(dir) != -1) and (file.find(self._buildType))):
                if (dir in (maindir)):
                    fullpath = self._path
                else:
                    fullpath = self._path + "/" + dir
                mkdir_p(fullpath)
                copyfile(filename, fullpath + "/" + file)
                
    def run(self):
        self.buildFileList("Poderosa.*.dll")
        self.buildFileList("Poderosa.*.pdb")
        self.buildFileList("Granados.dll")
        self.buildFileList("Granados.pdb")
        maindir = ["Plugin", "Granados"]
        self.copyFiles(maindir)
        self._files = []
        copyfile("Executable/bin/" + self._buildType + "/Poderosa.exe", self._path + "/Poderosa.exe")
        copyfile("Executable/bin/" + self._buildType + "/Poderosa.pdb", self._path + "/Poderosa.pdb")
        
def main(argv):
    buildType = "Debug"
    opts, args = getopt.getopt(argv, "b:", ["build="])
    for opt, arg in opts:
        if (opt in ('-b', '--build')):
            buildType = arg;

    buildDir = BuildDir(buildType);
    buildDir.run();
    
if __name__ == "__main__":
    main(sys.argv[1:])
