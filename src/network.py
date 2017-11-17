import psutil
import subprocess
from util import getPowerShellRes as grs
from basic import BasicFile

class NetWork(BasicFile):
    """
        Get Basic Network Info, DnsCache and NetRoute is useful for apt detect
    """
    def __init__(self, output='csv', dirpath=None, yara_path=None, yara_rule_path=None):
        self.outputformat = output
        self.DnsClientCache = self.getDnsClientCache()
        self.NetIPAddress = self.getNetIPAddress()
        self.NetAdapter = self.getNetAdapter()
        self.NetRoute = self.getNetRoute()

        # We Need use yara to match netroute file and dnsclientcache file, and we can't use ssdeep to do this
        # set this attribute, you can use the function,yarahit
        self.Filename = dirpath
        self.YaraPath = yara_path
        self.YaraRulePath = yara_rule_path

    def getDnsClientCache(self):
        return grs('Get-DnsClientCache', self.outputformat)

    def getNetRoute(self):
        return grs('Get-NetRoute', self.outputformat)

    def getNetIPAddress(self):
        return grs('Get-NetIPAddress', self.outputformat)

    def getNetAdapter(self):
        return grs('NetAdapter', self.outputformat)

    # Sniffer
    # Pcap


    
# def main():
    # test = NetWork('csv')
    # import basic
    # print(basic.bcolors.OKGREEN, test.DnsClientCache, basic.bcolors.ENDC)
    # print(basic.bcolors.FAIL, test.NetIPAddress, basic.bcolors.ENDC)
    # print(basic.bcolors.WARNING, test.NetAdapter, basic.bcolors.ENDC)
    # print(basic.bcolors.OKBLUE, test.NetRoute, basic.bcolors.ENDC)

# if __name__ == '__main__':
    # main()


