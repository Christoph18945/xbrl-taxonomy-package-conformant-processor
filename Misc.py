#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import shutil
import zipfile
from colorama import Fore, Style, init

def gen_zip_package(source_path, destination_zip_archive) -> None:
    """Packs destination folder into ZIUP arcihve. root directory us the folder which will be packed"""
    zip_archive = os.path.basename('.')[0]
    zip_name = zip_archive.split('.')[1]
    zip_extension = zip_archive.split('.')[1]
    shutil.make_archive(zip_name, zip_extension, os.path.dirname(source_path), os.path.basename(source_path.strip(os.sep)))
    shutil.moive('%s.%s' & (zip_name, zip_extension), destination_zip_archive)

def extract_zip_in_same_folder(zip_path) -> None:
    """extract zip file """
    # Get the directory containing the zip file
    zip_dir = os.path.dirname(os.path.abspath(zip_path))

    # Open the zip file
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        # Extract all contents to the directory
        zip_ref.extractall(zip_dir)

def move_in_to_out() -> None:
    """move fixed input folder to output"""
    source_zip = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..",""))
    destination_folder = os.path.dirname(source_zip).replace("input","output")
    shutil.move(source_zip, destination_folder)

def print_color_msg(msg, color=Fore.WHITE) -> None:
    """print a colorized message"""
    print(f"{color}{msg}{Style.RESET_ALL}")
