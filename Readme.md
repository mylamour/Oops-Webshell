## 通用检测框架

应用于Webshell检测和Apt检测


```
│  .gitignore
│  config.ini
│  Readme.md
│
├─.vscode
├─conf
│  │  Readme.txt
│  │
│  ├─blacklist
│  │      ip.txt
│  │
│  ├─features
│  │      asp.ssdeep
│  │      jsp.ssdeep
│  │      php.ssdeep
│  │
│  ├─model
│  ├─rules
│  │      asp.yar
│  │      php.yar
│  │
│  └─whitelist
├─doc
│  │  APT检测.km
│  │  Readme.md
│  │  The Pyramid Of Pain .png
│  │  version0.1.png
│  │  通用检测框架.svg
│  │
│  └─UML
│          apt UML 类图.pdf
│          apt UML 类图.png
│          apt UML 类图.vsdx
│
├─lib
│  │  backupwininfo.txt
│  │  Invoke-Parallel.ps1
│  │  test.ps1
│  │  testpy.py
│  │  windowsdefender.ps1
│  │  wininfo.ps1
│  │
│  └─PowerForensics
│      │  build.ps1
│      │  deploy.psdeploy.ps1
│      │  PowerForensics.ps1xml
│      │  PowerForensics.psd1
│      │  PowerForensics.psm1
│      │  psake.ps1
│      │  ReadMe.md
│      │
│      ├─en-US
│      │      PowerForensics.dll-Help.xml
│      │
│      ├─lib
│      │  ├─coreclr
│      │  │      PowerForensics.dll
│      │  │
│      │  └─PSv2
│      │          PowerForensics.dll
│      │          PowerForensics.pdb
│      │
│      └─Tests
│              PowerForensics.Test.ps1
│
├─src
│  │  basic.py
│  │  detect.py
│  │  main.py
│  │  network.py
│  │  process.py
│  │  registry.py
│  │  util.py
│  │  __init__.py
│  │
│  ├─bin
│  │      ssdeep
│  │      ssdeep.exe
│  │      yara
│  │      yara.exe
│  │
│  ├─fileinfo
│  │  │  binfile.py
│  │  │  docfile.py
│  │  │  logfile.py
│  │  │  __init__.py
│  │  │
│  │  ├─data
│  │  │  ├─Account
│  │  │  ├─Log
│  │  │  ├─Network
│  │  │  ├─Process
│  │  │  ├─Registry
│  │  │  └─Service
│  │  └─__pycache__
│  │          logfile.cpython-36.pyc
│  │          __init__.cpython-36.pyc
│  │
│  ├─ml
│  │  │  baseline.py
│  │  │  bayes.py
│  │  │
│  │  └─text cnn classfication
│  └─__pycache__
│          basic.cpython-36.pyc
│          detect.cpython-36.pyc
│          util.cpython-36.pyc
│          __init__.cpython-36.pyc
│
├─tests
│      404.asp
│      Ani-Shell.php
│      file.txt
│      hp.exe
│      test_detect.py
│      test_network.py
│      yara.exe
│      __init__.py
│
└─__pycache__
        detect.cpython-36.pyc
        util.cpython-36.pyc

```
