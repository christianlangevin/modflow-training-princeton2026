# Setting up MODFLOW and class environment

These are instructions for installing the extended version of MODFLOW 6 (with parallel and netcdf support), and for getting access to class materials and preparing the Python environment so you can follow along with the demos and exercises. 

We support Windows, Linux, and MacOS operating systems and the steps to follow are the same. In case you prefer to run in a Linux environment on Windows, using WSL is a good option. Below you will find instructions on how to install WSL. After a successful installation you should be ready to proceed with step 1.

## 1. Clone the class repo 

On Windows, start a CMD shell or open a terminal window in your favorite MacOS, Linux, or WSL environment.

In the terminal, clone the class repo using the following command:

```
git clone https://github.com/christianlangevin/modflow-training-princeton2026.git
```

If you do not have `git` installed (yet), you can find instructions how to do this [here](https://git-scm.com/downloads). Alternatively, you can download the zip archive from the repository at the following location:

https://github.com/christianlangevin/modflow-training-princeton2026/archive/refs/heads/main.zip

and unzip and rename the folder to modflow-training-princeton2026 and continue with the next step.

## 2. Setting up MODFLOW 6 and pixi environment

In order to set up MODFLOW 6, install the latest version of pixi. Instructions to get the Windows installer (or Powershell command) can be found at [https://pixi.sh/dev/installation/](https://pixi.sh/dev/installation/), for Linux and MacOS you can simply do:

```
curl -fsSL https://pixi.sh/install.sh | bash
```

and make sure to restart your shell. In case you already have pixi on your system, update to the latest version by doing: 

```
pixi self-update
```

Next execute:

```
cd modflow-training-princeton2026
pixi run install
```

This will take a bit of time, somewhere between 5 and 15 minutes, largely depending on the available network bandwidth. A successful installation sequence concludes with the message:

```
Successful testing of pixi environment and MODFLOW 6
```

## 3. Start Jupyter Lab

The class exercises will be run using jupyter notebooks. Jupyter Lab can be started by executing:

```
pixi run jupyter
```
and, when a browser window is not automatically opened, by clicking or copying the link at the end of the message which will look roughly like this:

```
 To access the server, open this file in a browser:
      file:///home/user/.local/share/jupyter/...
 Or copy and paste one of these URLs:
      http://localhost:8888/lab?token=...
      http://127.0.0.1:8888/lab?token=...
```

## Alternative: Installing WSL
_Note that you need elevated privileges and sometimes your IT administrator to complete this step_

On a Windows machine it is relatively easy to get MODFLOW compiled and running in a WSL Ubuntu virtual machine.

Install a recent version of Ubuntu:
```
  wsl --install -d Ubuntu-24.04
```

You will be asked to provide a username and password. You'll need to remember this information for some future `sudo` operations. 

Alternatively, you can install Ubuntu-24.04 from the Microsoft Store. In that case, you (or your administrator) might need to activate WSL explicitly:

1.	Open Windows 10 Settings app.
2.	Select Apps.
3.	Click Programs and Features under the Related settings section on the right.
4.	Under the Programs and Features page, click Turn Windows features on or off on the left panel.
5.	Scroll down and enable Windows Subsystem for Linux.

## Optional Software

There are a number of optional software products that may be useful for this class. Many of you will already have them installed or will have something similar. They are free and generally easy to install.
  * [Notepad++](https://notepad-plus-plus.org/downloads/)
  * [Visual Studio Code](https://code.visualstudio.com)
  * [QGIS](https://qgis.org)

