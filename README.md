# retweaks

This is a collection of personalization stuff (tweaks, apps, workarounds, templates, etc.) for my rm2.

TODO add fw version

TODO add disclaimer (obviously, these are my personal tweaks and there are no guarantees that any of these tipps will work...)

# Installation
## General Device Setup
* Change hostname via `/etc/hostname`
* SSH access (refer to the [remarkablewiki](https://remarkablewiki.com/tech/ssh) for details and troubleshooting).
  * The password is shown on the device via `Settings > Help > Copyrights and Licenses`
  * SSH password can be changed via `~/.config/remarkable/xochitl.conf`, edit the `DeveloperPassword` setting.
  * Add your private key for passwordless login (from the host):
    ```bash
    $ cat ~/.ssh/<KEYNAME>.pub | ssh root@<IP-ADDRESS> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
    ```
  * Edit `~/.ssh/config` on the host to use the key and prefer the Ethernet-over-USB connection over WIFI:
    ```bash
    Match host <HOSTNAME> exec "nc -z 10.11.99.1 -w 1 %p"
        HostName 10.11.99.1
    Match host <HOSTNAME>
        HostName <WIFI-IP-ADDRESS>
    Host <HOSTNAME>
      User root
      IdentityFile ~/.ssh/<KEYNAME>
    ```
  * Set up SFTP (e.g. FileZilla)
* Change command aliases via `~/.bashrc`:
  ```bash
  alias ll='ls -la`
  alias ..='cd ..'
  ```
* Set time zone
  * On the host: `date +%Z` (prints CET for me, obviously)
  * On the tablet: `timedatectl set-timezone CET`

## Personalization
* TODO scp `~/custom`, install services


# Important Locations
Important locations and files for backing up:
* All personal content (notebooks, books/PDFs, etc.) are located at `~/.local/share/remarkable/xochitl/`.  
  Backing up could take a while:  
  `$ scp -r root@<HOSTNAME>:~/.local/share/remarkable/xochitl/ rm2-backup/xochitl-files/`
* The configuration file is located at `~/.config/remarkable/xochitl.conf`.  
  To back up:  
  `$ scp root@<HOSTNAME>:~/.config/remarkable/xochitl.conf rm2-backup/`


# Splash Screens
Splash screens are located at `/usr/share/remarkable`.  
Information about the initial files (as of firmware version 2.5) via `file`:
* `batteryempty.png`: PNG image data, 1404 x 1872, 8-bit grayscale, non-interlaced
* `lowbattery.png`: PNG image data, 512 x 512, 8-bit/color RGBA, non-interlaced
* `overheating.png`: PNG image data, 1404 x 1872, 8-bit/color RGBA, non-interlaced
* `poweroff.png`: PNG image data, 1404 x 1872, 8-bit grayscale, non-interlaced
* `rebooting.png`: PNG image data, 1404 x 1872, 8-bit grayscale, non-interlaced
* `splash.png`: PNG image data, 1404 x 1872, 8-bit/color RGBA, non-interlaced
* `starting.png`: PNG image data, 1404 x 1872, 8-bit grayscale, non-interlaced
* `suspended.png`: PNG image data, 1404 x 1872, 8-bit grayscale, non-interlaced

To back up these files (as of firmware version 2.5):  
`$ scp root@<HOSTNAME>:/usr/share/remarkable/\{batteryempty.png,overheating.png,rebooting.png,starting.png,lowbattery.png,poweroff.png,splash.png,suspended.png\} rm2-backup/splash-screens/`

My [suspend-screen-cycler](./custom/suspend-screen-cycler) service automatically changes the sleep/suspended screen upon each reboot (actually, every (re)start of `xochitl.service`):
* Copy the [`./custom`](./custom) directory to the remarkable2 (e.g. to `~/custom`), then install the service via:
  ```bash
  # cd ~/custom/suspend-screen-cycler
  # ./01-install.sh
  ```
* To uninstall this service, run `./99-uninstall.sh` - **Note:** this will not restore the original suspend screen.


# Templates
Templates are located at `/usr/share/remarkable/templates`. To back them up (as of firmware version 2.5):  
`scp -r root@<HOSTNAME>:/usr/share/remarkable/templates rm2-backup/templates/`

My [custom templates](./host/template-scripting):
* A [5mm grid](./host/template-scripting/Grid5mm.png). The squares are 5x5 mm on the e-ink display. However, printing an exported notebook is slightly smaller (the exported PDF shows the correct size of 157x210 mm, but the printouts are smaller - **TODO:** I have to investigate the printing options (page/image scaling) in the future).
* A [5mm grid with ruler](./host/template-scripting/GridRuler.png) - Same caveats (5x5 on the e-ink, but smaller when printed).

To automatically install these on the device:
* (Optionally) Rebuild the templates via `./host/template-scripting/build_templates.sh`
* Run the install script (requires SSH access to the remarkable):
  ```bash
  $ cd ./host/template-scripting
  $ python3 install_templates.py --host <HOSTNAME>
  ```
* The install script is also able to remove unused templates (to reduce the clutter) - check the available options via the command line help: `python3 install_templates.py -h`
* **Do not** use the `install_templates.sh` (shell script, unless you know what you're doing). It just wraps the invocation of the python script and adds my personal parametrization.

To manually install the templates on the device:
* Copy the `.png` and `.svg` files to `/usr/share/remarkable/templates`.
* Edit `/usr/share/remarkable/templates/templates.json`: add the corresponding entry from `.json.inc`. **Note:** if the template supports portrait **and** landscape, there must be two entries in `templates.json`.
* Finally, reload the templates via restarting the UI: `systemctl restart xochitl`

Notes:
* For a list of available icon codes, check the [remarkablewiki](https://remarkablewiki.com/tips/templates).

# TODOs
Ideas/stuff I'd like to try:
* [ ] add custom templates
  * [x] ruler
  * [x] 5mm grid
  * [x] check if svg (export from remarkable!) really works (inkscape exports to plain v1.2 but not tiny...)
  * [ ] investigate print issues - exported PDFs print at smaller sizes (width: 145 to 152 instead of 157mm), although the PDF properties are set up correctly (157x210 mm).
* add custom splash screens
  * [ ] boot - footsteps
  * [x] powered off - 42
  * [x] suspend bricks
  * [x] suspend vehicle drawings
  * etc.
* live viewer
  * restream seems to work now
  * whiteboard for lectures - full screen app, toggle bg/window transparency
    * first, get streaming done
    * second, toggle portrait/landscape
    * third: toggle transparency (might not be possible https://stackoverflow.com/questions/18316710/frameless-and-transparent-window-qt5), alternatively: make a screenshot to draw on
* rprint
  * ipp print server (cpp tcp, requires basic pdf, likely stripped down from https://github.com/alexivkin/CUPS-PDF-to-PDF/blob/master/CUPS-PDF_noopt.ppd)
  * maybe support images
* cross compilation  
  https://unix.stackexchange.com/questions/510031/how-to-install-cross-compiler-on-ubuntu-18-04  
  rm toolchain: https://remarkablewiki.com/devel/qt_creator
* framebuffer extraction
* lz4 compression
* config UI (pyqt5)
* low priority: wacom input device

