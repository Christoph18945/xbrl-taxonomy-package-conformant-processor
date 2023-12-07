#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""app.py

Main program and entryp point.
"""

import argparse
import os
import sys
import shutil
import sys
from colorama import Fore, init
import argparse
import os
from TPChecker import TPChecker
from TPMisc import gen_zip_archive, print_color_msg
from TPFixer import EBATaxonomyPackage, EDINETTaxonomyPackage

def main() -> None:
    """driver code"""
    # intialize the colorama module
    init(autoreset=True)
    
    # initialize argument parser and set arguments for the cmdl
    parser: argparse.ArgumentParser = argparse.ArgumentParser(description="A simple cmdl tool to fix XBRL Taxonomy Packages.")
    parser.add_argument("provider", help="Provide abbreveation of official provider (e.g. EBA, EDINET, etc.).")
    parser.add_argument("package", help="Full path to the taxonomy_package_name.zip.")
    
    # catch exception if there are errors in parsed arguments
    try:
        args = parser.parse_args()
    except:
        error_message = f"""Please provide both: Abbreveation of provider (str.upper()) and full path to taxonomy package (zip):
{os.path.basename(__file__)} EBA '..\\inputs\\articles-49999_recurso_1a.zip'"""
        raise SystemExit(print_color_msg(f"Error: {error_message}",Fore.RED))
    
    # start analyzation only if both arguments are parsed
    if args.provider and args.package:

        # print out provider and path to package to make
        # user aware of what was passed to the tool
        print_color_msg(f"Input information:",Fore.BLUE)
        print_color_msg(f"-"*18,Fore.BLUE)
        print_color_msg(f"    Provider -> {args.provider}",Fore.BLUE)
        print_color_msg(f"    Package  -> {args.package}\n",Fore.BLUE)

        print_color_msg(f"Analyzis results:",Fore.BLUE)
        print_color_msg(f"-"*18,Fore.BLUE)
        
        # init Checker class to analyze the provided package
        tp_checker = TPChecker()

        # set vars forstatus checker
        ZIP_FORMAT = False
        SINGLE_DIR = False
        METAINF_DIR = False

        # 1/2 analyze the package
        # -----------------------

        # check if package is zip
        if tp_checker.has_zip_format(args.package):
            print_color_msg(f"    DONE: Package is ZIP",Fore.GREEN)
            ZIP_FORMAT = True
        else:
            print_color_msg(f"    ERROR: Package is not ZIP",Fore.RED)
            sys.exit()

        # check if has toplevel single directory
        if ZIP_FORMAT == True:
            if tp_checker.has_top_level_single_dir(args.package):
                print_color_msg(f"    DONE: Package has toplevel dir",Fore.GREEN)
                SINGLE_DIR = True
            else:
                print_color_msg(f"    ERROR: Package has not single toplevel dir",Fore.RED)
        else:
            print_color_msg(f"    ERROR: Package is not of format ZIP",Fore.RED)

        # check if pacvkage has META-INF folder
        if tp_checker.has_meta_inf_folder(args.package):
            print_color_msg(f"    DONE: Package has META-INF folder",Fore.GREEN)
            METAINF_DIR = True
        else:
            print_color_msg(f"    ERROR: Package has no META-INF folder",Fore.RED)

        # check if catalog.xml file exists
        if tp_checker.has_catalog_xml(args.package):
            print_color_msg(f"    DONE: Package has catalog.xml",Fore.GREEN)
            METAINF_DIR = True
        else:
            print_color_msg(f"    ERROR: Package has no catalog.xml",Fore.RED)

        # check if taxonomyPackage.xml file exists
        if tp_checker.has_taxonomy_package_xml(args.package):
            print_color_msg(f"    DONE: Package has taxonomy-package.xml",Fore.GREEN)
            METAINF_DIR = True
        else:
            print_color_msg(f"    ERROR: Package has no taxonomy-package.xml",Fore.RED)

        # 2/2 fix package
        # ---------------

        # set certain variables for fixing the package
        provider_name = args.provider.upper()
        source_zip = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..",""))
        source_zip_path = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(args.package.replace("\\", "/").replace("..","")).replace(".zip","")
        destination_folder = os.path.dirname(source_zip).replace("input","output")

        # fix taxyonomy package provided by the European Banking Authority
        if provider_name == "EBA":
            print_color_msg(f"\nFixing package...",Fore.YELLOW)

            # initialize the EBA class
            eba_taxonomy_package: EBATaxonomyPackage = EBATaxonomyPackage(source_zip_path, destination_folder)
            
            # if all three variables are true, there is nothig to fix and
            # the package is moved as it is in the output-folder
            if ZIP_FORMAT == True:
                pass
            else:
                eba_taxonomy_package.convert_to_zip_archive()
            
            if METAINF_DIR == True:
                pass
            else:
                eba_taxonomy_package.fix_meta_inf_folder()
            
            if SINGLE_DIR == True:
                pass
            else:
                eba_taxonomy_package.fix_top_level_single_dir()

            # remove the working folder in the output folder
            target_dir = source_zip.replace("input", "output").replace(".zip","")
            shutil.rmtree(target_dir)

            print_color_msg(f"\nOutput result:",Fore.BLUE)
            print_color_msg(f"-"*14,Fore.BLUE)
            print_color_msg(f"    {os.path.basename(args.package)} is fixed",Fore.BLUE)

        # fix taxonomy package provided by the FSA (EDINET system)
        if provider_name == "EDINET":
            print_color_msg(f"\nFixing package...",Fore.YELLOW)

            # initialize the EDINET class
            edinet_taxonomy_package: EDINETTaxonomyPackage = EDINETTaxonomyPackage(source_zip_path, destination_folder)

            if ZIP_FORMAT == True:
                pass
            else:
                edinet_taxonomy_package.convert_to_zip_archive()

            if METAINF_DIR == True:
                pass
            else:
                edinet_taxonomy_package.fix_meta_inf_folder()

            if SINGLE_DIR == True:
                pass
            else:
                edinet_taxonomy_package.fix_top_level_single_dir()

            # prepare variables to work with
            full_path_to_zip: str = source_zip.replace("input", "output")
            target_output_dir: str = source_zip.replace("input", "output").replace(".zip","")

            # restructure the folder strucutre in the package
            # means moveing taxonomy/, samples/ and META-INF/ folder
            # in the root directory
            edinet_taxonomy_package.restructure_folder()

            # generate and validate the catalog.xml file
            edinet_taxonomy_package.fix_catalog_xml(target_output_dir)
            
            # generate and validate the taxonomyPackage.xml file
            edinet_taxonomy_package.fix_taxonomy_package_xml(target_output_dir)

            # compose zip archive
            gen_zip_archive(target_output_dir, full_path_to_zip)

            # remove the folder next to the fixed zip archive, because
            # not needed anymore
            shutil.rmtree(target_output_dir)

            # print output result information
            print_color_msg(f"\nOutput result:",Fore.BLUE)
            print_color_msg(f"-"*14,Fore.BLUE)
            print_color_msg(f'    {os.path.basename(args.package.replace("input","output"))} is fixed!\n',Fore.BLUE)

        # TODO: This is just a first working template version. Fixes for more packages should be implemented.
        # The following packages could be supported as well:
        #     https://www.sec.gov/edgar/information-for-filers/standard-taxonomies
        #     https://xbrl.us/xbrl-taxonomy/2021-acfr/
        #     https://xbrl.us/xbrl-taxonomy/2023-mutual-fund-riskreturn/
        #     https://www.ifrs.org/issued-standards/ifrs-taxonomy/
        #     https://esurfi-assurance.banque-france.fr/
        #     https://www.bundesbank.de/en/service/reporting-systems/banking-supervision/formats-xbrl-and-xml-/formats-xml-and-xbrl--619400
        #     https://www.bde.es/wbe/en/entidades-profesionales/supervisadas/informacion-financiera-a-remitir-entidades-supervisadas/entidades-credito/taxonomias/
        #     https://www.bportugal.pt/en/page/reporting-obligations-supervised-institutions
        #     https://www.bankofengland.co.uk/prudential-regulation/regulatory-reporting/regulatory-reporting-banking-sector/banks-building-societies-and-investment-firms
        #     https://www.centralbank.ie/regulation/industry-market-sectors/investment-firms
        #     https://www.cipc.co.za/?page_id=4400
        #     https://www.cmfchile.cl/portal/principal/613/w3-article-49999.html
        #     https://www.dnb.nl/en/login/dlr/information-and-documentation/
        #     https://www.esma.europa.eu/document/esma-esef-taxonomy-2021
        #     ...

        return None

if __name__ == "__main__":
    main()
