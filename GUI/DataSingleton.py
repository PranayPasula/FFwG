import cv2

class DataSingleton:
    __instance = None

    imageSrc = None
    imageFFT = None
    imageGrey = None
    imageDst = None

    OnSrcChanged = None
    OnFFTChanged = None
    OnDstChanged = None

    @staticmethod
    def GetInstance():
        if DataSingleton.__instance == None:
            DataSingleton()
        return DataSingleton.__instance

    def __init__(self):
        if DataSingleton.__instance != None:
            raise Exception("This should only be called once")
        else:
            DataSingleton.__instance = self

    def GetImageSrc(self, greyscale):
        if greyscale:
            image = self.imageGrey
        else:
            image = self.imageSrc
        return image

    def SetImageSrc(self, image):
        self.imageSrc = image
        self.imageGrey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        self.OnSrcChanged()

    def GetImageDst(self):
        return self.imageDst

    def SetImageDst(self, image):
        self.imageDst = image
        self.OnDstChanged()

    def GetImageFFT(self):
        return self.imageFFT

    def SetImageFFT(self, image):
        self.imageFFT = image
        self.OnFFTChanged()
    
    def SetOnSrcChanged(self, callback):
        self.OnSrcChanged = callback

    def SetOnFFTChanged(self, callback):
        self.OnFFTChanged = callback

    def SetOnDstChanged(self, callback):
        self.OnDstChanged = callback



