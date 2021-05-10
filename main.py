from PIL import Image
from shutil import copy2
import os,calendar,easygui

class PictureSorter():
    def __init__(self,directory):
        self.getpictures(directory)
        self.getmetadate()
        
    #creates a list of all pictures in a given directory
    def getpictures(self,directory):
        #store list
        self.filelist = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if(file.endswith(".JPG") or file.endswith(".jpg")):
                #append the file name to the list
                    self.filelist.append(os.path.join(root,file))

    #reads metadata from pictures and retrieves the date
    def getmetadate(self):
        self.foldername = []
        for image in self.filelist:
            im = Image.open(image)
            exif = im.getexif()
            #gets time picture was taken
            creation_time = exif.get(36867)
            #checks to ensure metadata can be read
            if creation_time is not None:
                month = calendar.month_name[int(creation_time[5:7])]
                year = creation_time[0:4]
                self.foldername.append(month+"-"+year)
            else:
                #adds pictures to an undated folder
                self.foldername.append("Undated Pictures")

class FileManager():
    def __init__(self,contents):
        self.foldergeneration(contents)
        self.copyimages(contents)

    #creates folders with dates from pictures in current working directory
    def foldergeneration(self,contents):
        for item in contents.foldername:
            if not os.path.exists(item):
                os.makedirs(item)

    #copies images into current working directory
    def copyimages(self,contents):
        for i in range(len(contents.filelist)):
            cwd = os.getcwd() + "/"
            copy2(contents.filelist[i], cwd + contents.foldername[i])

if __name__ == "__main__":
    picture_directory = easygui.enterbox("What is the path of the pictures?")
    contents = PictureSorter(picture_directory)
    FileManager(contents)
