### Script that allows to play the audio of a video from Youtube in VLC player app on iOS.
This scrip will only work with [Pythonista 3](http://omz-software.com/pythonista/) or [Pyto](https://pyto.app
) and [VLC player app](https://www.videolan.org/vlc/download-ios.html) installed on you iOS device.

**Caution: Pythonista 2 is not supported!**

This script uses [youtube-dl](https://ytdl-org.github.io/youtube-dl/index.html) to get the needed data from the Youtube.
Thus, it must be installed first.

If you use Pythonista3 you need to use [stash](https://github.com/ywangd/stash) to install the "youtube-dl" package.
Please, follow instructions on [stash page](https://github.com/ywangd/stash) to have a working pip in
Pythonista3. 
 
If you use Pyto, please use its PyPi interface and install the latest version of "youtube-dl"

After you have the "youtube-dl" package installed, just download the script from [here](https://foo_change_me) and
 open it in Pythonista3 or Pyto.

**Usage:**
1. Copy a video URL to clipboard. If you use Pythonista3 you also can run the script from the share sheet.
2. Run the script.

After the script will finish, it will open the VLC app and will ask for confirmation in order to stream the audio.
Note: the audio will continue to play even if the VLC is in the background. 

For more convenience you can run the script using actions in the Shortcuts app or by using [Pythonista3 url scheme
](http://omz-software.com/pythonista/docs/ios/urlscheme.html) or [Pyto url scheme](https://pyto.readthedocs.io/en/latest/automation.html).
