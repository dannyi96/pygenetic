import tarfile
import zipfile
import os

def checkAndCreateDownloadsFolder():
    dirname = os.path.dirname(os.path.abspath(__file__))
    try: 
        os.makedirs(os.path.join(dirname,'downloads'))
        print("\n\n\nDownloads folder Created!\n\n\n")
    except(FileExistsError):
        print("\n\n\nDownloads folder already exists!\n\n\n")
        pass


def makeCompressedfile(outputFilename, sourceDir, fileType):
    if(fileType.startswith(".tar")):
        extension = fileType.split(".")[2]
        with tarfile.open(outputFilename, "w:"+extension) as tar:
            tar.add(sourceDir, arcname=os.path.basename(sourceDir))
    
    else:
        print("outputFilename:",outputFilename)
        print("sourceDir:",sourceDir)
        with zipfile.ZipFile(outputFilename, 'w', zipfile.ZIP_DEFLATED) as ziph:
            for root, dirs, files in os.walk(sourceDir):
                for file in files:
                    ziph.write(os.path.join(root, file),os.path.relpath(os.path.join(root, file), os.path.join(sourceDir, '..')))


