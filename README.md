# retweaks

This is a collection of simple tweaks I find useful for remarkable2 tablets.

# Recurrent Customizations
Required after each firmware upgrade unless noted otherwise:
* Change hostname via `/etc/hostname`. Takes effect after reboot.
* Change time zone (to prevent some potential issues due to clock mismatch between host and device):
  * To find out your timezone, run `date +%Z` on the host. For example, this prints out `CET` (or `CEST` during DST) for me.
  * Set the timezone on the tablet: `timedatectl set-timezone CET`  
    During DST you also need to set the standard timezone (i.e. `CET`, not `CEST`).

# One-time Customizations
The following tweaks seem to remain intact during firmware upgrades:
* Simplify SSH access (for more details refer to the [remarkablewiki](https://remarkablewiki.com/tech/ssh)).  
  * The SSH password is shown on the device via `Settings > Help > Copyrights and Licenses`
  * The SSH password can be changed via `~/.config/remarkable/xochitl.conf`, editing the `DeveloperPassword` setting.
  * Add public key for passwordless login - use `ssh-keygen` if no public key is available (standard RSA should work fine):
    ```bash
    $ cat ~/.ssh/<KEYNAME>.pub | ssh root@<IP-ADDRESS> 'mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys'
    ```
  * Edit `~/.ssh/config` on the **host** to use the key and prefer the Ethernet-over-USB connection over WIFI:
    ```bash
    Match host <HOSTNAME> exec "nc -z 10.11.99.1 -w 1 %p"
        HostName 10.11.99.1
        ConnectTimeout 1
    Match host <HOSTNAME>
        HostName <WIFI-IP-ADDRESS>
        ConnectTimeout 3
    Host <HOSTNAME>
        User root
        IdentityFile ~/.ssh/<KEYNAME>
    ```
* Set up [FileZilla](https://filezilla-project.org/) on the **host** to simplify transfering files from/to the device.

# Install Custom Templates
Each upgrade overwrites the custom templates.  
In order to reinstall them:
```bash
cd host/template-scripting
# If templates haven't been build so far:
./build_templates.sh

# This downloads the template configuration from the tablet, modifies it and re-syncs it with the tablet:
./install_templates.sh
```

# External Tweaks
* [ddvk's binary patches](https://github.com/ddvk/remarkable-hacks) add useful gestures & settings (pen styles, recently opened doc list, etc.)  
  Check the patch availability before firmware upgrade if you got used to these features!
* [bordaigorl's rmview](https://github.com/bordaigorl/rmview) is an easy to use & efficient screen share possibility.  
  **Note:** firmware 2.6+ includes a system library incompatible with rmview, see [this issue on the rmview github](https://github.com/bordaigorl/rmview/issues/57)  
  **Note:** firmware 2.10 leverages the official ScreenShare functionality on the tablet
  * Set up a virtualenv, then `pip install https://github.com/bordaigorl/rmview/archive/refs/heads/vnc.zip`
  * Add a launcher item on the host `venv/.../python -m rmview`  
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
  * Edit `~/.config/rmview.json` if needed, see [exemplary config](https://github.com/bordaigorl/rmview/blob/vnc/example.json)


## Native Printing
* Install the [remarkable-printer](https://github.com/Evidlo/remarkable_printer) to be able to print directly to the device, without accessing the rM cloud.  
  ```bash
  ssh <HOSTNAME>
  wget -O - http://raw.githubusercontent.com/Evidlo/remarkable_printer/master/install.sh | sh
  ```
  * This step is also needed after upgrading the firmware from 2.5 to 2.6.
* Then add the device as AppSocket printer:
  * `System > Printers > Add Printer`
  * Add a network printer: `AppSocket/HP JetDirect` (hostname/IP and default port number 9100).
  * Provide PPD file (my custom PPD defines a media size of 157x210 mm instead of [evidlo's](https://github.com/Evidlo/remarkable_printer/blob/master/remarkable.ppd) 155x205)
* Caveats:
  * No authentication - anyone on the network could print (if IP/hostname is known and they can find a suitable PPD).
  * PDF titles aren't working in my setup - all printed files are entitled "printed" on the remarkable
  * The application is active listening on the 9100 socket - should use [socket activation](https://github.com/Evidlo/remarkable_printer) instead.
  * Useful extensions (TODOs):
    * (Requires Go proficiency) Specify output directory (`inbox` or similar) and save there - just requires adjusting the template.  
      **However**, the `inbox` directory must exist. Thus, we would need to parse the `.metadata` files, build the internal file structure and then check if the "folder" exists (and create if needed).
    * Include date/time string in default title.

## Obsolete UI Improvements
* Install [funkey's low pass filter](https://github.com/funkey/recept) to fix jagged lines.
  * **Note:** Firmware version 2.6 reduced the jagged lines issue by a lot. Currently, I don't need the funkey fix any longer.
  * For firmware version 2.5 and below, follow these installation steps:
    ```bash
    $ # On host computer
    $ git clone https://github.com/funkey/recept
    $ cd recept
    $ ./install.sh
    ```

# Backup Important Locations
Important locations and files for backing up:
* All personal content (notebooks, books/PDFs, etc.) are located at `~/.local/share/remarkable/xochitl/`.  
  Backing up could take a while:  
  `$ scp -r root@<HOSTNAME>:~/.local/share/remarkable/xochitl/ rm2-backup/xochitl-files/`
* The configuration file is located at `~/.config/remarkable/xochitl.conf`.  
  To back up:  
  `$ scp root@<HOSTNAME>:~/.config/remarkable/xochitl.conf rm2-backup/`

# Personalization
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
*Caveat:* custom templates are not available on the rm cloud, you will see a `unable to load document background` watermark on the synchronized PDFs.

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
* [x] Investigate print issues
  * On Ubuntu 18.04 exported PDFs print at smaller sizes (width of 145 to 152 instead of 157mm), although the PDF dimensions/properties are set up correctly (157x210 mm).
  * Printing from Ubuntu 20.04 worked nicely (157x210 mm)
  * Printing from Windows worked nicely (157x210 mm)
* pagination via [foot pedal](https://www.reddit.com/r/RemarkableTablet/comments/kg9ira/made_a_foot_pedal_for_my_rm2/?utm_source=share&utm_medium=web2x&context=3)
* low priority: wacom input device --> try remouse instead
* [x] Measure bandwidth rmview (restream took approx. 11.5G per 3 minutes of whiteboarding)

