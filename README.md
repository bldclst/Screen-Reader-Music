# Overview

Screen Reader Music is a Python Application that acts as a Web Server. You can upload music scores as MusicXML files.

Note: .musicxml or .xml are the only compatible formats. Do not try uploading xompressed MusicXML files like .mxl.

## Example output:

### Title - # Measures

Measure 1

Dynamic: f

Note: D4, Type: quarter, Duration: 1.0, Staccato Tenuto

Note: D4, Type: quarter, Duration: 1.0, Staccato Tenuto

Note: A3, Type: quarter, Duration: 1.0, Staccato Tenuto

Note: A3, Type: quarter, Duration: 1.0, Staccato Tenuto

### Navigation Buttons (Previous, Next, Jump to specified measure)
### Current Time Signature: 4/4
### Current Key Signature: D-major

# Deployment Instructions

## Step 1 - Download Python:

Install the latest version of Python: https://www.python.org/downloads/

Note: Use custom install and verify both pip is installed and that your systems PATH variable is updated.

## Step 2 - Download the app:

You can download the app code from this page by navigating to the "Code" menu Drop-down button. Marked as a form control by screen reader. Then navigate to the "Download ZIP" link.

Move and unzip the app code in a folder of your choosing.

## Step 3 - Setup:

You can open the unzipped folder's properties and copy its path from the window.

Open a command prompt. This will be Terminal in Mac, and Command Prompt or Powershell in Windows.

Type:

```
cd "paste the path to your folder here between the quotes"
```

Run the setup.py script:

```
python3 setup.py
```

## Step 4 - Run:

Based on your machine and shell environment, if the setup successfully runs then you should see one of the following:
```
run.sh
run.bat
run.ps1
```

You can start the application by executing this script:
'''
.\run.ps1
.\run.bat
./run.sh
'''

If you use powershell, make sure you can execute local scripts. Run Powershekk as Administrator and execute the following command:
```
Set-ExecutionPolicy RemoteSigned

```