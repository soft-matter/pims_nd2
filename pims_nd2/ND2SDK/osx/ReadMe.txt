ND2 Read SDK
============

1) Content of this package
--------------------------
 ReadMe.txt           - This file
 doc                  - documentation folder. Open doc/index.html in web browser
 nd2sdk.framework     - MAC OS X framework containing binary of ND2 Read SDK. Framework needs to be installed into system Frameworks folder
 example              - sources of example project
 exampleApp.app       - compiled binary of example project together with all required libraries
 nd2ReadSDK.h         - Header file defining SDK interface. Required for linking with ND2 SDK framework


2) Running example application
------------------------------
Double-click on exampleApp application to launch precompiled example binaries


3) Installing ND2 SDK to system
-------------------------------
a) Copy nd2sdk.framework into one of system Frameworks directories:
 /Library/Frameworks                  - will be available to all users, requires administrator privileges
 /System/Library/Frameworks           - will be available to all users, requires administrator privileges
 <HomeDir>/Library/Frameworks/        - will be available only to current user, no special privileges required

To install ND2 SDK for current user only, copy nd2sdk.framework directory into <HomeDir>/Library/Frameworks/ (create intermediate directories if not already present)
Following terminal commands can be used to create <HomeDir>/Library/Frameworks/ directory and copy nd2sdk.framework inside:

mkdir -p ~/Library/Frameworks/
cp -a nd2sdk.framework ~/Library/Frameworks/


4) Building example application
-------------------------------
Example application is written using Qt Framework. Following steps are required to build the example application:
 a) Install nd2sdk.framework as described in section 3
 b) Download and install Qt SDK from http://qt.nokia.com/downloads/ - use online installer 
 c) Open example/example.pro file in Qt Creator (double-click the example.pro file)
 d) Press Done on next dialog
 e) Hit Build > Run to build and run example application


-------------------------------

If you have any question, please contact us at nd2sdk-owners@nd2sdk.com

For Public Discussion with all other people registered at www.nd2sdk.com with activated Mailing list option, please use nd2sdk@nd2sdk.com