# sigit
Little helper to ease the process of providing signatures for GitHub release archives.

**Usage**: Downloads a (GitHub) release archive and compares it to a local folder.

       python3 sigit.py [-h] [--silent] [--verbose] url path

**Positional arguments:**

       url         download URL
       path        path to local folder

**Optional arguments:**

       -h, --help  show this help message and exit
       --silent    Do not print any output
       --verbose   Print a lot of output

Returns **0** if the downloaded archive contents are the same as the local folders' contents, **1** if not.
