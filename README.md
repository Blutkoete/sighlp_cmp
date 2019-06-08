# sighlp_cmp
Little helper to ease the process of providing signatures for GitHub release archives. It downloads an archive from a given URL and compares its contents to a local folder.

*Tested on Arch Linux*.

**Usage**: Downloads a (GitHub) release archive and compares it to a local folder.

       python3 sighlp_cmp.py [-v {0,1,2}] url path

**Positional arguments:**

       url             download URL
       path            path to local folder

**Optional arguments:**

       -h, --help      show this help message and exit
       -v  --verbose   set the verbosity level (0 - silent, 1 - normal, 2 - ultra)

Returns **0** if the downloaded archive contents are the same as the local folders' contents, **1** if not.
