#!/usr/bin/python3
# -*- coding: utf-8 -*-

import shutil
import sys
from colorama import Fore, Style, init
import argparse
import os
from Processor import Checker

def main() -> None:
    """driver code"""
    init(autoreset=True)
    
    parser = argparse.ArgumentParser(description="A simple command-line tool to fix taxonomy packages.")
    
    parser.add_argument("provider", help="provider abbreveation to identify who prvodied the taxonomy package.")
    parser.add_argument("package", help="Path tot the taxonomy pacakge (ZIP file).")
    
    try:
        args = parser.parse_args()
    except:
        error_message = f"""Please provide both: Abbreveation of provider and the path to the package:
{os.path.basename(__file__)} EBA '..\\inputs\\articles-49999_recurso_1a.zip'"""
        raise SystemExit(print_color_msg(f"Error: {error_message}",Fore.RED))
    
    if args.provider and args.package:

        print_color_msg(f"Input information:",Fore.BLUE)
        print_color_msg(f"-"*18,Fore.BLUE)
        print_color_msg(f"    Provider -> {args.provider}",Fore.BLUE)
        print_color_msg(f"    Package  -> {args.package}\n",Fore.BLUE)

        print_color_msg(f"Analyzis results:",Fore.BLUE)
        print_color_msg(f"-"*18,Fore.BLUE)
        # program logic goes here:
        tp_checker = Checker()

        ZIP_FORMAT = False
        if tp_checker.has_zip_format(args.package):
            print_color_msg(f"    DONE: Package is ZIP",Fore.GREEN)
            ZIP_FORMAT = True
        else:
            print_color_msg(f"    ERROR: Package is not ZIP",Fore.RED)
            sys.exit()

        SINGLE_DIR = False
        if ZIP_FORMAT == True:
            if tp_checker.has_top_level_single_dir(args.package):
                print_color_msg(f"    DONE: Package has toplevel dir",Fore.GREEN)
                SINGLE_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has not single toplevel dir",Fore.RED)
        else:
            print_color_msg(f"    ERROR: Package is not of format ZIP",Fore.RED)

        METAINF_DIR = False
        if SINGLE_DIR == True:
            if tp_checker.has_meta_inf_folder(args.package):
                print_color_msg(f"    DONE: Package has META-INF folder",Fore.GREEN)
                METAINF_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has no META-INF folder",Fore.RED)

        if METAINF_DIR == True:
            if tp_checker.has_catalog_xml(args.package):
                print_color_msg(f"    DONE: Package has catalog.xml",Fore.GREEN)
                METAINF_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has no catalog.xml",Fore.RED)

            if tp_checker.has_taxonomy_package_xml(args.package):
                print_color_msg(f"    DONE: Package has taxonomy-package.xml",Fore.GREEN)
                METAINF_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has no taxonomy-package.xml",Fore.RED)

        provider_name = args.provider.upper()

        source_zip = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..",""))
        source_zip_path = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..","")).replace(".zip","")
        destination_folder = os.path.dirname(source_zip).replace("input","output")

        # fix taxyonomy package provided by EBA
        if provider_name == "EBA":
            # move final file to output folder
            # shutil.move(source_zip, destination_folder)
            # print("We are here right now!")

            print_color_msg(f"\nOutput result:",Fore.BLUE)
            print_color_msg(f"-"*14,Fore.BLUE)
            print_color_msg(f"    {os.path.basename(args.package)} is fixed",Fore.BLUE)

        # fix taxyonomy package provided by CMF CL CI
        if provider_name == "CMF-CLCI":
            pass

        # fix taxyonomy package provided by EDINET
        if provider_name == "EDINET":
            pass

        return None

def move_in_to_out() -> None:
    """move fixed input folder to output"""
    source_zip = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..",""))
    destination_folder = os.path.dirname(source_zip).replace("input","output")
    shutil.move(source_zip, destination_folder)
    return None

def print_color_msg(msg, color=Fore.WHITE) -> None:
    """print a colorized message"""
    print(f"{color}{msg}{Style.RESET_ALL}")
    return None

if __name__ == "__main__":
    main()
