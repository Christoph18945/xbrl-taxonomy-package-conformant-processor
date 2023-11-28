#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Misc.py

The module provides generic functions.
"""

import os
import shutil
import zipfile
from colorama import Fore, Style, init

def zip_folder(folder_path, zip_filename):
    """"""
    # Open a zip file for writing
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Iterate over all files and subdirectories in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                # Determine the relative path to the file from the root folder
                relative_path = os.path.relpath(file_path, folder_path)
                # Use arcname to specify the target folder as the root folder in the zip file
                zipf.write(file_path, arcname=os.path.join(os.path.basename(folder_path), relative_path))

def move_folder_recursive(source_folder, destination_folder):
    """"""
    # Create the destination folder if it doesn't exist
    os.makedirs(destination_folder, exist_ok=True)
    # Iterate over the contents of the source folder
    for item in os.listdir(source_folder):
        source_item_path = os.path.join(source_folder, item)
        destination_item_path = os.path.join(destination_folder, item)
        # If the item is a directory, move it recursively
        if os.path.isdir(source_item_path):
            move_folder_recursive(source_item_path, destination_item_path)
        else:
            # If the item is a file, move it
            shutil.move(source_item_path, destination_item_path)
    # Remove the empty source folder
    os.rmdir(source_folder)

def gen_zip_package(source_path, destination_zip_archive) -> None:
    """Packs destination folder into ZIUP arcihve. root directory us the folder which will be packed"""
    zip_archive: str = os.path.basename('.')[0]
    zip_name: str = zip_archive.split('.')[1]
    zip_extension: str = zip_archive.split('.')[1]
    shutil.make_archive(zip_name, zip_extension, os.path.dirname(source_path), os.path.basename(source_path.strip(os.sep)))
    shutil.move('%s.%s' & (zip_name, zip_extension), destination_zip_archive)

def extract_zip_in_same_folder(zip_path) -> None:
    """extract zip file """
    # Get the directory containing the zip file
    zip_dir = os.path.dirname(os.path.abspath(zip_path))

    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents to the directory
        zip_ref.extractall(zip_dir)

def print_color_msg(msg, color=Fore.WHITE) -> str:
    """print a colorized message"""
    return f"{color}{msg}{Style.RESET_ALL}"
