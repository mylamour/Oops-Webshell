from util import getPowerShellRes as grs
# from basic import BasicFile

class Process:

    def __init__(self, output_format='csv'):
        self.outputformat = output_format 
        self.Process = self.getprocess()
        self.Win32Process = self.getwin32Process()

    def getprocess(self):
        return grs('Get-Process',self.outputformat)

    def getwin32Process(self):
        return grs('Get-WmiObject -Class Win32_Process',self.outputformat)

    def getwin32SystemProcess(self):
        return grs('Get-WmiObject -Class Win32_SystemProcesses',self.outputformat)

    def getwin32Thread(self):
        return grs('Get-WmiObject -Class Win32_Thread',self.outputformat)

def main():
    test = Process()
    win32Process = test.getwin32Process()
    for _ in win32Process:
        print(_)
if __name__ == '__main__':
    main()