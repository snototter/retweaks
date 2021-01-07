# retweaks

This is a collection of stuff (tweaks, apps, workarounds, ideas, etc.) for my rm2.

https://remarkablewiki.com/start


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
To back up these files (as of firmware version 2.5):  
`scp -r root@<HOSTNAME>:/usr/share/remarkable/templates rm2-backup/templates/`


# TODOs
Ideas/stuff I'd like to try:
* add custom templates (ruler + finer grid)
* add custom splash screens
* live viewer (whiteboard for lectures)
* cross compilation  
  https://unix.stackexchange.com/questions/510031/how-to-install-cross-compiler-on-ubuntu-18-04  
  rm toolchain: https://remarkablewiki.com/devel/qt_creator
* framebuffer extraction
* lz4 compression
* config UI (pyqt5)
* wacom input device

