
# CycleSpy_start

CycleSpy_start provides a template project to get up-and-running fast with CycleSpy.
## Install
This documentation is mainly written for either Ubuntu or Mac. Windows and other Linux distribution are also supported, but require some extra steps that are not explained here. Installing for Windows can be tricky as it's not trivial to install *Make* or the *ARM-GCC* compiler.

For Mac it is recommended that the package manager 'brew' is installed.

> ***Requirements:***
> - Python 3.8+
> - Git (recommended, often already installed on Ubuntu/Mac)
> - Make (only for compiling, often already installed on Ubuntu/Mac)
> - gcc-arm-none-eabi or gcc-arm-embeded (only for compiling, see installation instructions below)

> **Supported microcontrollers:**
>  *Only Cortex-M3 and Cortex-M4 microcontrollers are supported by CycleSpy at the moment*
>  - For testing: [PyOCD target support](https://pyocd.io/docs/target_support.html)
>  - For compiling: [LibOpenCM3 support](https://github.com/libopencm3/libopencm3?tab=readme-ov-file#readme)
### Clone the project

#### Git (recommended)
The easiest way to check-out the project is by cloning it using Git. The '--recursive' parameter also makes sure the submodules are downloaded. 

> IMPORTANT: make sure to be logged in or set the right SSH-keys into Github to make sure you can checkout the CycleSpy projects correctly!

``` bash
# Checkout using SSH (recommended if SSH keys are set in Github)
$ git clone --recursive git@github.com:baszn/cyclespy_start.git

# Checking out using https is also possible, but you need to provide your Github username/password during the clone
$ git clone --recursive https://github.com/baszn/cyclespy_start.git
```

#### Download directly
It's also possible to download the files directly from Github, but this will not automatically download the required submodules. The contents of the following repositories need to be placed in the right directories:

```
./cyclespy/ -> https://github.com/baszn/cyclespy/
./cyclespy_files/libopencm3/ -> https://github.com/libopencm3/libopencm3
```

### Install Python requirements
Go to the root directory of where you cloned the project and run pip on requirements.txt:

```bash
# If 'pip' doesn't work, try 'pip3' or 'pipx'
$ pip -r install requirements.txt
```

### Install gcc-arm
When compiling assembly files into an executable elf, it's required to have *Make* and the ARM GCC compiler installed.

**Make**
*Make* is often already installed on Ubuntu and Mac. To check type 'make' into a terminal and the output should be something like this:
```
make: *** No targets specified and no makefile found.  Stop.
```

Otherwise you can install it with with either apt-get or brew:

```
$ sudo apt-get install make
% brew install make
```

**ARM GCC**
CycleSpy uses the ARM GCC compiler to compile the assembly files into .elf files. To install this compiler run the following commands:

```bash
# Ubuntu
$ sudo apt-get install gcc-arm-none-eabi
# Mac
% brew install --cask gcc-arm-embedded
```
### Compiling LibOpenCM3
For LibOpenCM3 to work correctly it's required to pre-compile some binaries. To do this, go to the `./cyclespy_files/libopencm3` directory and run `make`.

```bash
$ cd ./cyclespy_files/libopencm3
$ make
```

This will build files for every supported device. Building doesn't take that long so it's often not necessary to limit the build to certain devices, but if you want to see the documentation of [LibOpenCM3](https://github.com/libopencm3/libopencm3?tab=readme-ov-file#building).

## Template files
The template files are the starting point of using/learning about CycleSpy. These template files contain comments that explain what each code segment does.

***cyclespy_recording_example.py*** 
Creates assembly test files, compiles them, flash them om the connected microcontroller and saves the results into the `./cyclespy_files/results` directory. Should be able to run without any modification when a microcontroller is connected and LibOpenCM3 and PyOCD are setup correctly.

***cyclespy_verify_example.py*** 
Example of how to verify the results with the verifier. Only Cortex-M3 results are supported at the moment.

***recording_example_no_comments.py*** 
Same as *cyclespy_recording_example.py* but without comments.

## Used libraries
### PyOCD
PyOCD is a Python package that makes it easy to communicate with a broad range of microcontrollers. It is used extensively in CycleSpy to communicate with these microcontrollers.

PyOCD relies on a *debugger* that uses SWD or JTAG to communicate with the microcontroller. It is thereby important that the debugger is supported by PyOCD (support can be found [here](https://pyocd.io/docs/debug_probes.html)). Some microcontrollers have a debugger built-in, like most modern STM32 microcontrollers, but others require an external debugger like the ST-link/V2.

PyOCD will be automatically installed when using the *requirements.txt*, but can also be manually  installed using `pip`. 

```bash
# Sometimes the command 'pip3' needs to be used instead of 'pip'
# For Ubuntu when pip gives an error, pipx can also be used
pip install pyocd
```

When correctly installed the command `pyocd` should give the following output:
```
$ pyocd
usage: __main__.py [-h] [-V] [--help-options]  ...

PyOCD debug tools for Arm Cortex devices

optional arguments:
  -h, --help       show this help message and exit
  -V, --version    show program's version number and exit
  --help-options   Display available session options.
...
```

_Note: Sometimes when Python is not correctly added to the `PATH`, the `pyocd` command doesn't work. Use instead the command `$ python3 -m pyocd`._

To test if PyOCD correctly recognises the debugger and the microcontroller correctly, type the command`pyocd list`. When PyOCD correctly identifies the microcontroller, the following output will be shown:


```bash
$ pyocd list
  #   Probe/Board     Unique ID                  Target
----------------------------------------------------------------
  0   STM32 STLink    xxxxxxxxxxxxxxxxxxxxxxx   ✔︎ stm32f103rb
      NUCLEO-F103RB
```


Not all microcontrollers are supported by PyOCD out of the box. To check if the microcontroller is supported, run `pyocd list --targets` to give an overview of all available targets. Often when the microcontroller is not listed here, or it is listed as *'pack'*, it can be installed by the `pyocd pack` command. First run `pyocd pack update` followed by `pyocd pack install <target_name>` to install the required pack.

When using an external debugger, like the ST-Link/V2, automatic recognition of the device will often fail. Therefore the target id can be manually given by providing the `--target` parameter.  For example when using the `cmd` command of PyOCD, the target can be given as follows:

``` bash
$ pyocd cmd --target <target_name>
```

The `cmd` command provides an interactive shell that can be used to interact with the microcontroller. This is command is very usefull to test if the communication with the microcontroller works correctly.

This `target_name` will also be used by CycleSpy to identify the correct microcontroller.

### LibOpenCM3
CycleSpy uses the project LibOpenCm3 to create executable *.elf* files for a broad range of microcontrollers.  In the world of microcontrollers, it is often not possible to compile a single binary that will run on many microcontroller. This has (often) to do with small differences like memory-layout.

LibOpenCM3 simplifies the process of compiling for different microcontrollers by generating the necessary device specific files and Linker files (*.ld*). The Linker files indicate to the compiler/flasher to place the data in the correct places in memory.

> Note that not every microcontroller is supported by LibOpenCM3. The supported models can be found on the [Github page of LibOpenCM3](https://github.com/libopencm3/libopencm3?tab=readme-ov-file#readme).

### FAQ
**Q: I get the following error:**
``` diff
- pyocd.core.exceptions.TargetSupportError: Target type <target> not recognized. Use 'pyocd list --targets' to see currently available target types. See <https://pyocd.io/docs/target_support.html> for how to install additional target support.
```

A: The target is automatically recognised, but PyOCD doesn't have the correct 'pack' installed that has the required information in it to start a session with this target. To solve this, open a terminal and type:

```bash
$ pyocd pack update
# If the command doesn't work, prefix it with 'python3 -m <command>'
```

Followed by the target you want to install:

``` bash
$ pyocd pack install <target_name> 
# <target_name> is the identifier of the microcontroller, like stm32f103rb
```

For more info see:
https://pyocd.io/docs/target_support.html

**Q: I get the following error:**

``` diff
- ./cyclespy_start/cyclespy_files/libopencm3/mk/genlink-config.mk:65: ./cyclespy_start/cyclespy_files/libopencm3/lib/libopencm3_stm32f1.a library variant for the selected device does not exist.

```

A:
You either didn't run Make on the `./cyclespy_files/libopencm3` directory or the microcontroller you connected is not [supported by LibOpenCM3](https://github.com/libopencm3/libopencm3?tab=readme-ov-file#readme).

