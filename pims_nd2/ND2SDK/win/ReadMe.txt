ND2 Read SDK
============

1) Content of this package
--------------------------
 ReadMe.txt           - This file
 doc                  - documentation folder
 bin                  - Windows dlls and example executables for 32 and 64 bit system
 src                  - sources of example projects
 lib                  - import library
 include              - Header file defining SDK interface. Required for linking with ND2 SDK framework


2) Examples
------------------------------
 ND2ReadSDK_simple    - simple application displaying image and additional text info available for 32 and 64 bit system
 ND2ReadSDK_QT        - complex application with QT GUI using the most of the SDK features available for 32 and 64 bit system

3) Running examples
------------------------------
 Execute ND2ReadSDK_simple.exe or ND2ReadSDK_QT.exe in bin/x86 or bin/x64 folder according to 32/64 bit version.
 
3) Building examples from source
-------------------------------
 Open ND2ReadSDK_simple.sln or ND2ReadSDK_QT.sln from appropriate subfolder in the 'src' folder using MS Visual studio 2008 or higher.
 Choose the platform (32/64bit) and build the solution as usual. If you do not use QT library for GUI, it is not necessary to include these QT binaries into your project:
 SDK\bin\x64\Qt5Core.dll 
 SDK\bin\x64\Qt5Gui.dll 
 SDK\bin\x64\Qt5Widgets.dll 
 SDK\bin\x64\platforms 
 SDK\lib\x64\Qt5Core.lib 
 SDK\lib\x64\Qt5Gui.lib 
 SDK\lib\x64\Qt5Widgets.lib 
 SDK\lib\x64\qtmain.lib)

-------------------------------

If you have any question, do not hesitate and contact us at techsupp@lim.cz