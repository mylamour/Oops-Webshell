# coding: utf-8

import  psutil

psutil.LINUX

http_services = ['apahce','apahce2','nginx','http','systemd']

def get_host_services():
    host_services = []
    # host_services = {}
    for _ in psutil.pids():
        try :
            p = psutil.Process(_)
            name = p.name()
            exe = p.exe()
            cmdline = p.cmdline()
            username = p.username()
            tmp = {'name':name,'pid':_ ,'exe':exe, 'cmdline': cmdline,'username':username}
            host_services.append(tmp)
    #         host_services.update(tmp)
        except psutil.AccessDenied as e:
            # print ("if you want get " + name + "Info.May be you need a high level priviallge, eg.root")
            # print(name)
            pass
        finally:
            pass
    return host_services

def search(name, host_services):
    return [element for element in host_services if element['name'] == name]

def get_service_path(servicename):
    m_host_services = get_host_services()
    result = search(servicename,m_host_services)
    path = []
    if len(result) > 1:
        for _ in result:
            path.append(_['exe'])
        return set(path)
    else:
        return 

def test():
    for _ in http_services:
        if get_service_path(_) is not None :
            print(_,get_service_path(_))

if __name__ == '__main__':
    test()