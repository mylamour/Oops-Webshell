import pefile



def binsection(exe_path):
    pe = pefile.PE(exe_path)
    for section in pe.sections:
        print(section.Name.decode('utf-8'))
        print("\tVirtual Address: " + hex(section.VirtualAddress))
        print("\tVirtual Size: " + hex(section.Misc_VirtualSize))
        print("\tRaw Size: " + hex(section.SizeOfRawData))


# class BinFile(basic.BasicFile):
#     def __init__(self,filename):
#         super().__init__(filename)
#         # self.filename = filename
#         # pass

#     def peheader():
#         pass


def main():
    # fuck = BinFile('../tests/hp.exe')
    # print(fuck.Filename)

    binsection('../tests/yara.exe')

if __name__ == '__main__':
    main()

# exe_path = "c:\putty.exe"
# 
