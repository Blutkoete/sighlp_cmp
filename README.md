# sighlp_cmp
Little helper to ease the process of providing signatures for GitHub release archives. It downloads an archive from a given URL and compares its contents to a local folder.

*Tested on Arch Linux*.

**Usage**: Downloads a (GitHub) release archive and compares it to a local folder.

       python3 sighlp_cmp.py [-h] [-v {0,1,2}] [-d dir_name_to_ignore] [-f file_name_to_ignore] url path


**Positional arguments:**

       url             download URL
       path            path to local folder

**Optional arguments:**

       -h, --help      show this help message and exit
       -v {0,1,2}, --verbosity {0,1,2}
                       set the verbosity level (0 - silent, 1 - normal, 2 - ultra)
       -d dir_name_to_ignore, --ignore-dir dir_name_to_ignore
                       directory name to ignore, e.g. ".git" - may be specified multiple times
       -f file_name_to_ignore, --ignore-file file_name_to_ignore
                       file name to ignore, e.g. ".gitignore" - may be specified multiple times


Returns **0** if the downloaded archive contents are the same as the local folders' contents, **1** if not.
