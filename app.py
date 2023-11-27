#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""app.py

Main program and entryp point.
"""

import argparse
from datetime import datetime
import os
import sys
import shutil
import sys
import zipfile
from colorama import Fore, Style, init
import argparse
import os
from Checker import Checker
from Misc import gen_zip_package, print_color_msg, zip_folder
from TaxonomyPackage import EDINETTaxonomyPackage

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
        
        tp_checker = Checker()

        ZIP_FORMAT = False
        SINGLE_DIR = False
        METAINF_DIR = False

        if tp_checker.has_zip_format(args.package):
            print_color_msg(f"    DONE: Package is ZIP",Fore.GREEN)
            ZIP_FORMAT = True
        else:
            print_color_msg(f"    ERROR: Package is not ZIP",Fore.RED)
            sys.exit()

        if ZIP_FORMAT == True:
            if tp_checker.has_top_level_single_dir(args.package):
                print_color_msg(f"    DONE: Package has toplevel dir",Fore.GREEN)
                SINGLE_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has not single toplevel dir",Fore.RED)
        else:
            print_color_msg(f"    ERROR: Package is not of format ZIP",Fore.RED)

        if tp_checker.has_meta_inf_folder(args.package):
            print_color_msg(f"    DONE: Package has META-INF folder",Fore.GREEN)
            METAINF_DIR = True
        else:
            print_color_msg(f"    ERROR: Package has no META-INF folder",Fore.RED)

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

            print_color_msg(f"\nOutput result:",Fore.BLUE)
            print_color_msg(f"-"*14,Fore.BLUE)
            print_color_msg(f"    {os.path.basename(args.package)} is fixed",Fore.BLUE)

        # fix taxyonomy package provided by EDINET
        if provider_name == "EDINET":
            edinet_taxonomy_package: EDINETTaxonomyPackage = EDINETTaxonomyPackage(source_zip_path, destination_folder)

            if ZIP_FORMAT == True:
                pass
            else:
                # function goes here
                ...

            if METAINF_DIR == True:
                pass
            else:
                edinet_taxonomy_package.fix_meta_inf_folder()

            if SINGLE_DIR == True:
                pass
            else:
                edinet_taxonomy_package.fix_top_level_single_dir()

            d = source_zip.replace("input", "output")
            target_dir = source_zip.replace("input", "output").replace(".zip","")
            base_dir = d.replace(source_zip.replace(".zip",""),"")

            edinet_taxonomy_package.restructure_folder()

            edinet_taxonomy_package.fix_catalog_xml(target_dir)
            edinet_taxonomy_package.fix_taxonomy_package_xml(target_dir)

            zip_folder(target_dir, d)

            shutil.rmtree(target_dir)

            print_color_msg(f"\nOutput result:",Fore.BLUE)
            print_color_msg(f"-"*14,Fore.BLUE)
            print_color_msg(f"    {os.path.basename(args.package)} is fixed",Fore.BLUE)            

        return None

if __name__ == "__main__":
    main()
