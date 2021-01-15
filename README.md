# retweaks

This is a collection of customization tweaks for my remarkable2.
As these are personal customizations I will give no guarantees that any of these will work for you. The only guarantee I can give is that there is no ill intended code. There may, however, be bugs, you may lose data, or even brick your device (if you don't know what you're doing...).

Note that this is (more or less, depending on my need for sleep) ongoing work as of 01/2021.  
All the stuff in this repository has so far been tested with FW version `2.5.0.27`.


# Installation
## General Device Setup
Customization steps I performed after completing the rM tutorial:
* Change hostname via `/etc/hostname` (yes, I'm that nit-picky).  
  Takes affect after reboot.
* Simplify SSH access (refer to the [remarkablewiki](https://remarkablewiki.com/tech/ssh) for details and troubleshooting).
  * The password is shown on the device via `Settings > Help > Copyrights and Licenses`
  * SSH password can be changed via `~/.config/remarkable/xochitl.conf`, edit the `DeveloperPassword` setting.
  * Add your public key for passwordless login (from the host) - if you don't have a key already, use `ssh-keygen` (standard RSA should work fine):
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
  * Set up [FileZilla](https://filezilla-project.org/) to simplify transfering files from/to the device (I'm a simple guy, I like simple UIs)
* Change command aliases via `~/.bashrc`:
  ```bash
  alias ll='ls -la`
  alias ..='cd ..'
  ```
* Change time zone (to prevent some potential issues due to clock mismatch between host and device):
  * To find out your timezone, run `date +%Z` on the host. For example, this prints out `CET` for me. **TODO:** check if DST switch works (should as `/usr/share/zoneinfo/CET` contains the jump dates between `CET` and `CEST`)
  * Set the timezone on the tablet: `timedatectl set-timezone CET`

## Native Printing
Install the [remarkable-printer](https://github.com/Evidlo/remarkable_printer).  
```bash
ssh <HOSTNAME>
wget -O - http://raw.githubusercontent.com/Evidlo/remarkable_printer/master/install.sh | sh
```
Then add the device as AppSocket printer:
* `System > Printers > Add Printer`
* Add a network printer: `AppSocket/HP JetDirect` (hostname/IP and default port number 9100).
* Provide PPD file (my custom PPD defines a media size of 157x210 mm instead of [evidlo's](https://github.com/Evidlo/remarkable_printer/blob/master/remarkable.ppd) 155x205)
Caveats:
* No authentication - anyone on the network could print (if IP is known and they can find a suitable PPD).
* PDF titles aren't working in my setup - all printed files are entitled "printed" on the remarkable
* The application is active listening on the 9100 socket - should use [socket activation](https://github.com/Evidlo/remarkable_printer) instead.
* Useful extensions (TODOs):
  * [Requires Go proficiency] Specify output directory (`inbox` or similar) and save there - just requires adjusting the template.  
    **However**, the `inbox` directory must exist. Thus, we would need to parse the `.metadata` files, build the internal file structure and then check if the "folder" exists (and create if needed).
  * Include date/time string in default title.

## UI Improvements
* Install the [ddvk's binary patches](https://github.com/ddvk/remarkable-hacks) for really useful interface features.
  ```bash
  $ ssh <HOSTNAME>
  # sh -c "$(wget https://raw.githubusercontent.com/ddvk/remarkable-hacks/master/patch.sh -O-)"
  ```
* Install [funkey's low pass filter](https://github.com/funkey/recept) to fix jagged lines.
  ```bash
  $ cd tryouts
  $ git clone https://github.com/funkey/recept
  $ cd recept
  $ ./install.sh
  ```

## RM as Whiteboard
In my tests, both [reStream](https://github.com/rien/reStream) and [rmview](https://github.com/bordaigorl/rmview) worked out-of-the-box.
However, rmview already provides all features I need for a digital whiteboard - like auto rotation, reduce bandwidth via damage tracking, show pointer position, etc.
Additionally, it uses damage tracking to send only necessary updates and thus, reduces the required bandwidth.
Thus, I'll stick with (the VNC-based) `rmview`:
* Set up `rmview` on the host:
  * Prepare PyQt5-based UI on the host:
    ```bash
    $ ./host/whiteboard/install_rmview_host.sh
    ```
  * Optionally, add a launcher entry in your start menu, either via your favorite menu editor or using a `rmview.desktop` like:
    ```ini
    [Desktop Entry]
    Name=rmview
    Comment=remarkable liveview
    Exec=<PATH/TO/VIRTUALENV>/bin/python -m rmview
    Type=Application
    Terminal=false
    Icon=<PATH/TO/RETWEAKS/REPO>/host/whiteboard/launcher.svg
    Categories=Education;
    StartupWMClass=rmview
    ```  
    A simple [launcher icon](./host/whiteboard/launcher.svg) is provided.
* Then, copy the included [rM-vnc-server](https://github.com/pl-semiotics/rM-vnc-server) to the device and ensure it is executable:
  ```bash
  $ scp host/whiteboard/rmview-2.1/bin/rM2-vnc-server-standalone <HOSTNAME>:rM-vnc-server-standalone

  $ ssh <HOSTNAME>
  # chmod +x ./rM-vnc-server-standalone
  ```


# Backup Important Locations
Important locations and files for backing up:
* All personal content (notebooks, books/PDFs, etc.) are located at `~/.local/share/remarkable/xochitl/`.  
  Backing up could take a while:  
  `$ scp -r root@<HOSTNAME>:~/.local/share/remarkable/xochitl/ rm2-backup/xochitl-files/`
* The configuration file is located at `~/.config/remarkable/xochitl.conf`.  
  To back up:  
  `$ scp root@<HOSTNAME>:~/.config/remarkable/xochitl.conf rm2-backup/`

# Customization
## Splash Screens
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


## Templates
Templates are located at `/usr/share/remarkable/templates`. To back them up (as of firmware version 2.5):  
`scp -r root@<HOSTNAME>:/usr/share/remarkable/templates rm2-backup/templates/`

A template consists of:
* A PNG file which is shown as the first layer of your notebook/sheet.
* An SVG file which is used whenever you export your notebook/sheet.
* A configuration entry to properly load the template. These are stored on the device at `/usr/share/remarkable/templates/templates.json`.

My [custom templates](./host/template-scripting):
* A [5mm grid](./host/template-scripting/Grid5mm.png). The squares are 5x5 mm on the e-ink display. However, printing an exported notebook is slightly smaller (the exported PDF shows the correct size of 157x210 mm, but the printouts are smaller - **TODO:** I can't print any exported document at the correct size (need to investigate page/image scaling options of the printer).
* A [5mm grid with horizontal & vertical rulers](./host/template-scripting/GridRuler.png) - Same caveats (5x5 mm on the e-ink, but smaller when printed).

To automatically install these custom templates on the device:
* (Optionally) Rebuild the templates via `./host/template-scripting/build_templates.sh`
* Run the install script (requires SSH access):
  ```bash
  $ cd ./host/template-scripting
  $ python3 install_templates.py --host <HOSTNAME>
  ```
* The install script is also able to remove templates from the device's configuration. For this, check the available options via the command line help:  
  `python3 install_templates.py -h`
* **Do not** use the `install_templates.sh` (shell script, unless you know what you're doing). It just wraps the invocation of the python script and adds my personal parametrization.

To manually install the templates on the device:
* Copy the `.png` and `.svg` files to `/usr/share/remarkable/templates`.
* Edit `/usr/share/remarkable/templates/templates.json`: add the corresponding entry from `.inc.json`.
* Finally, reload the templates via restarting the UI: `systemctl restart xochitl`

Notes:
* For a list of available icon codes, check the [remarkablewiki](https://remarkablewiki.com/tips/templates).


# TODOs
Ideas, apps and tweaks I'd like to try:
* [ ] Grid templates: PNG with utility markers, SVG without (for export)
* [ ] Gardening calendar template
* [ ] Update readme w/ templates caveat: not exported to the cloud - "unable to load document background" within the cloud app
* [ ] Investigate print issues
  * On Ubuntu 18.04 exported PDFs print at smaller sizes (width of 145 to 152 instead of 157mm), although the PDF dimensions/properties are set up correctly (157x210 mm).
  * Printing from Windows worked nicely
* cross compilation  
  https://unix.stackexchange.com/questions/510031/how-to-install-cross-compiler-on-ubuntu-18-04  
  rm toolchain: https://remarkablewiki.com/devel/qt_creator
* pagination via [foot pedal](https://www.reddit.com/r/RemarkableTablet/comments/kg9ira/made_a_foot_pedal_for_my_rm2/?utm_source=share&utm_medium=web2x&context=3)
* low priority: config UI (pyqt5)
  * replace splash screens
  * upload templates
  * replace suspend screen service by UI (?)
* low priority: wacom input device
* lowest priority: reprint
  * ipp print server (cpp tcp)
  * pdf support (size conversion ??)
  https://github.com/alexivkin/CUPS-PDF-to-PDF/blob/master/CUPS-PDF_noopt.ppd)
  * maybe support images
  * related projects:  
    [printing via CUPS and rmapi](https://ofosos.org/2018/10/22/printing-to-remarkable-cloud-from-cups/) (requires sync via cloud)  
    [go-based native AppSocket/HP JetDirect printer](https://github.com/Evidlo/remarkable_printer)  
    [python minimal ipp server](https://github.com/h2g2bob/ipp-server)
* [ ] Pointer position (rmview/rm-vnc-server) could be used to implement a wacom input device?
* [ ] Measure bandwidth rmview (restream took approx. 11.5G per 3 minutes of whiteboarding)

