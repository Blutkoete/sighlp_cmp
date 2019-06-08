#!/usr/bin/env python3
import argparse
import hashlib
import os
import shutil
import sys
import tempfile
import urllib.request


def _cond_print(what, condition):
    """
    Conditional print().
    :param what: What to print.
    :param condition: Condition to check.
    """
    if condition:
        print(what)


if __name__ == '__main__':
    content_is_equal = False
    parser = argparse.ArgumentParser('downloads a Github release archive and compares it to a local folder')
    parser.add_argument('--silent', dest='silent', action='store_const', const=True, default=False,
                        help='Do not print any output')
    parser.add_argument('--verbose', dest='verbose', action='store_const', const=True, default=False,
                        help='Print a lot of output')
    parser.add_argument('url', metavar='url', type=str, help='download URL')
    parser.add_argument('path', metavar='path', type=str, help='path to local folder')
    args = parser.parse_args()
    if args.silent and args.verbose:
        print('--silent and --verbose are mutually exclusive')
        sys.exit(1)
    temp_dir = tempfile.mkdtemp(prefix='sigit_')
    temp_file = os.path.join(temp_dir, args.url.rsplit('/', 1)[-1])
    temp_unarchived_dir = None
    try:
        # Download the given file
        _cond_print('Downloading "{}" ...'.format(args.url), not args.silent)
        urllib.request.urlretrieve(args.url, temp_file)
        _cond_print('Download completed!', not args.silent)
        # Unarchive it
        _cond_print('Unpacking ...', not args.silent)
        shutil.unpack_archive(temp_file, temp_dir)
        _cond_print('Unpacking complete!', not args.silent)
        temp_dir_list = os.listdir(temp_dir)
        if len(temp_dir_list) != 2:
            raise RuntimeError('There are more than two entries in temp directory after unpacking. Aborting.')
        if os.path.basename(temp_file) not in temp_dir_list:
            raise RuntimeError('Originally downloaded file not longer in temp directory. Aborting.')
        for dir_entry in temp_dir_list:
            if dir_entry == os.path.basename(temp_file):
                continue
            archive_root_dir = os.path.join(temp_dir, dir_entry)
            if not archive_root_dir.endswith('/'):
                archive_root_dir = archive_root_dir + '/'
            archive_dir_list = []
            archive_file_list = []
            local_root_dir = args.path
            if not local_root_dir.endswith('/'):
                local_root_dir = local_root_dir + '/'
            local_dir_list = []
            local_file_list = []
            _cond_print('Comparing "{}" to "{}" ...'.format(archive_root_dir, local_root_dir), not args.silent)
            # Get all directories & files as lists for the archive
            for root, dirs, files in os.walk(archive_root_dir):
                for dir_ in dirs:
                    full_dir_path = os.path.join(root, dir_)
                    clean_dir_path = full_dir_path.replace(archive_root_dir, '', 1)
                    archive_dir_list.append(clean_dir_path)
                for file_ in files:
                    full_file_path = os.path.join(root, file_)
                    clean_file_path = full_file_path.replace(archive_root_dir, '', 1)
                    archive_file_list.append(clean_file_path)
            # Get all directories & files as lists for the local path
            for root, dirs, files in os.walk(local_root_dir):
                for dir_ in dirs:
                    full_dir_path = os.path.join(root, dir_)
                    clean_dir_path = full_dir_path.replace(local_root_dir, '', 1)
                    local_dir_list.append(clean_dir_path)
                for file_ in files:
                    full_file_path = os.path.join(root, file_)
                    clean_file_path = full_file_path.replace(local_root_dir, '', 1)
                    local_file_list.append(clean_file_path)
            archive_dir_list.sort()
            archive_file_list.sort()
            local_dir_list.sort()
            local_file_list.sort()
            # Compare dirs
            if len(archive_dir_list) != len(local_dir_list):
                for archive_dir in archive_dir_list:
                    if archive_dir not in local_dir_list:
                        print('Archive directory "{}" has no match on local.'.format(archive_dir))
                for local_dir in local_dir_list:
                    if local_file not in archive_file_list:
                        print('Local directory "{}" has no match in archive.'.format(local_dir))
                raise RuntimeError('Directory structure is not equal. Aborting.')
            for archive_dir, local_dir in zip(archive_dir_list, local_dir_list):
                if archive_dir != local_dir:
                    raise RuntimeError('Directory name not equal: "{}" in archive, "{}" on local. Aborting'.format(archive_dir, local_dir))
                _cond_print('Comparison passed: "{}" and "{}".'.format(archive_dir, local_dir), args.verbose)
            # Compare files via name & hash
            if len(archive_file_list) != len(local_file_list):
                for archive_file in archive_file_list:
                    if archive_file not in local_file_list:
                        print('Archive file "{}" has no match on local.'.format(archive_file))
                for local_file in local_file_list:
                    if local_file not in archive_file_list:
                        print('Local file "{}" has no match in archive.'.format(local_file))
                raise RuntimeError('File count different. Aborting.')
            for archive_file, local_file in zip(archive_file_list, local_file_list):
                if archive_file != local_file:
                    raise RuntimeError('File name not equal: "{}" in archive, "{}" on local. Aborting'.format(archive_file, local_file))
                archive_hash = hashlib.sha512()
                with open(os.path.join(archive_root_dir, archive_file), 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        archive_hash.update(data)
                local_hash = hashlib.sha512()
                with open(os.path.join(local_root_dir, local_file), 'rb') as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        local_hash.update(data)
                if archive_hash.hexdigest() != local_hash.hexdigest():
                    raise RuntimeError('Hash mismatch: "{}" for archive file "{}", "{}" for local file "{}".'.format(archive_hash.hexdigest(), archive_file, local_hash.hexdigest(), local_file))
                _cond_print('Comparison passed: "{}" [{}] and "{}" [{}].'.format(archive_file, archive_hash.hexdigest(), local_file, local_hash.hexdigest()), args.verbose)
            content_is_equal = True
    except Exception as err:
        print(err)
    finally:
        for root, dirs, files in os.walk(archive_root_dir, topdown=False):
            for file_ in files:
                os.remove(os.path.join(root, file_))
            for dir_ in dirs:
                os.rmdir(os.path.join(root, dir_))
        os.rmdir(archive_root_dir)
        os.remove(temp_file)
        os.rmdir(temp_dir)
    if content_is_equal:
        _cond_print('Comparison passed!', not args.silent)
        sys.exit(0)
    else:
        _cond_print('Comparision failed.', not args.silent)
        sys.exit(1)