"""
File handling helpers for American Iron Giant
"""
import os
import shutil
import tarfile


def move_files(source: str, destination: str) -> None:
    """
    Move all files from a source directory to a destination directory

    :param source: The directory we'll move files from
    :param destination: The directory we're moving files to. We'll create it if it doesnt' exist.
    """
    if not os.path.exists(destination):
        os.mkdir(destination)

    for filename in os.listdir(source):
        current_full_path = os.path.join(source, filename)
        if not os.path.isfile(current_full_path):
            continue

        shutil.move(current_full_path, os.path.join(destination, filename))


def tar_up(directory: str, name: str) -> str:
    """
    Tar and gzip up all the files in directory and call it filename.tar.gz

    :param directory: Directory/folder to pull all files from
    :param name: Name of the resultant archive without any file type (i.e., .tar, .gz)
    :return: The name of the tarred up file
    """

    # TODO: assert that there's no filetype for filename

    filename = name + ".tar.gz"

    tar = tarfile.open(filename, "w:gz")

    # TODO: get the first part of the filename and use that as the archive name
    tar.add(directory, arcname="Images")
    tar.close()

    return filename
