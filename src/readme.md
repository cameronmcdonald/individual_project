# Readme

The code provided for this project handles the detection of vehicles, sending of coordinates and the moving of a 3d object based on the coordinates recieved over UDP.

## Build instructions

**You must** include the instructions necessary to build and deploy this project successfully. If appropriate, also include 
instructions to run automated tests. 

### Requirements

* Python 2.7
* Zed 2 SDK

* Unity Hub
* Unity Editor
* Mixed Reality Kit
* Mized Reality Feature Tool
* Windows SDK

### Build steps

No building steps are required for the Python script for the Zed2. Simply download Zed SDK and run the scripts with the camera attached using USB.

For Unity, build settings must be configured as well as player settings. This varies heavily depending on version of Unity editor and platform however you want to choose all of the settings for universal windows platform.

Mixed reality tool kit must be imported, follow the download instructions.

Ensure the build target is setup for the HoloLens 2.