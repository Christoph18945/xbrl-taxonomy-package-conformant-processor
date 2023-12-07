#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Misc.py

The module provides generic helper functions to the
XBRL Taxonomy Package checking and fixing process.
"""

import os
import shutil
import zipfile
from colorama import Fore, Style

def gen_zip_archive(folder_path: str, zip_filename: str) -> None:
    """Generate a zip archive out of a root input folder."""
    zip_file: zipfile.ZipFile
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path: str = os.path.join(root, file)
                relative_path: str = os.path.relpath(file_path, folder_path)
                zip_file.write(file_path, arcname=os.path.join(os.path.basename(folder_path), relative_path))
    print_color_msg("    Final zip generated",Fore.YELLOW)
    return None

def move_folder_recursively(source_folder: str, destination_folder: str) -> None:
    """Move folder recursively from one destination to another one."""
    os.makedirs(destination_folder, exist_ok = True)
    for item in os.listdir(source_folder):
        source_item_path: str = os.path.join(source_folder, item)
        destination_item_path: str = os.path.join(destination_folder, item)
        if os.path.isdir(source_item_path):
            move_folder_recursively(source_item_path, destination_item_path)
        else:
            shutil.move(source_item_path, destination_item_path)
    os.rmdir(source_folder)
    return None

def extract_zip_in_same_folder(zip_path: str) -> None:
    """Extract zip file to destination path."""
    zip_dir: str = os.path.dirname(os.path.abspath(zip_path))
    zip_ref: zipfile.ZipFile
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(zip_dir)
    return None

def print_color_msg(msg: str, color: str = Fore.WHITE) -> None:
    """Print a colorized message."""
    print(f"{color}{msg}{Style.RESET_ALL}")
    return None
