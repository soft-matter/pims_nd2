ND2 Read SDK
============

1) Content of this package
--------------------------
 ReadMe.txt           - This file
 doc                  - documentation folder. Open doc/index.html in web browser
 bin				  - Windows dlls and example executables for 32 and 64 bit system
 src                  - sources of example projects
 lib			      - import library
 include	          - Header file defining SDK interface. Required for linking with ND2 SDK framework


2) Examples
------------------------------
 ND2ReadSDK_simple    - simple application displaying image and additional text info available for 32 a 64 bit system
 ND2ReadSDK_QT        - complex application with QT GUI using the most of the SDK features available for 32 bit system only

3) Running examples
------------------------------
 Execute ND2ReadSDK_simple.exe or ND2ReadSDK_QT.exe in bin/x86 or bin/x64 folder according to 32/64 bit version.
 
3) Building examples from source
-------------------------------
 Open ND2ReadSDK_simple.sln or ND2ReadSDK_QT.sln from appropriate subfolder in the 'src' folder using MS Visual studio 2008 or higher.
 Choose the platform (32/64bit) and build the solution as usual. If you do not use QT library for GUI, it is not necessary to include QT binaries (QtCore4.dll, QtGui4.dll) into your project.

-------------------------------

If you have any question, do not hesitate and contact us at nd2sdk-owners@nd2sdk.com.