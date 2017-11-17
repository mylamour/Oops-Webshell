from basic import BasicFile

# Depend Powershell script, you should add the function
# Why we need a single Class Named LogFile instead of use the BasicFile,it's not only to use ssdeep/yara, also need parser the txt file 
# for ml predict in future

class LogFile(BasicFile):
    def __init__(self,filename,fileformat='csv'):
        super().__init__(filename)
        # self.filename = filename
        # pass

    def filecontent():
        # Evt Parser??
        pass