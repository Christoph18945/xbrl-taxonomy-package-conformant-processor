#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Fixer.py

The module contains classes with relevant methods to fix
xbrl taxonomy packages based by certain providers.
"""

from abc import ABC, abstractmethod
import os
from xml.dom.minidom import parseString
import xml.etree.ElementTree as ET
import zipfile
from io import TextIOWrapper
import shutil
import zipfile
import os
from colorama import Fore
from TPChecker import TPChecker
from TPMisc import print_color_msg

class TaxonomyPackageFixerInterface(ABC):
    """The Interface provides methods to fix an
    XBRL Taxonomy Package by a certain provider.
    """
    def __init__(self, full_path_to_zip: str, destination_folder: str) -> None:
        """Initialize XBRL Taxonomy Package class. By initializing the class
        the input package is copied over to the ouptut folder and extracted there
        to comfortably work with the data."""
        # set initial variables
        self.full_path_to_zip = full_path_to_zip
        self.destination_folder = destination_folder
        # create destination folder
        os.makedirs(self.destination_folder, exist_ok=True)
        # move taxonomy package to destination folder
        shutil.move(f"{self.full_path_to_zip}.zip", self.destination_folder)
        # extract at destination
        with zipfile.ZipFile(os.path.join(self.destination_folder, os.path.basename(full_path_to_zip)+".zip"), 'r') as zip_ref:
            zip_ref.extractall(self.destination_folder)
        return None

    @abstractmethod
    def convert_to_zip_archive(self):
        """Returns an xbrl taxonomy package in zip format."""

    @abstractmethod
    def fix_top_level_single_dir(self):
        """Generates a single toplevel directory for
        the provided xbrl taxonomy package."""

    @abstractmethod
    def fix_meta_inf_folder(self):
        """Generates a META-INF folder for the
        provided xbrl taxonomy package."""

    @abstractmethod
    def restructure_folder(self):
        """Perform restructuring of folders in the
        XBRL Taxonomy Package."""

    @abstractmethod
    def fix_taxonomy_package_xml(self):
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
    
    @abstractmethod
    def fix_catalog_xml(self):
        """'A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element
        with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification)
        for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString).'"""

class EDINETTaxonomyPackage(TaxonomyPackageFixerInterface):
    """Use this class to fix an EDINET XBRL Taxonomy Package.
    
    The package in input/* folder as well as newer and older versions
    can be found here: https://disclosure2.edinet-fsa.go.jp/weee0020.aspx
    """
    def convert_to_zip_archive(self) -> None:
        shutil.make_archive(self.full_path_to_zip, 'zip', self.destination_folder)    
        return None

    def fix_top_level_single_dir(self) -> None:
        os.makedirs(os.path.join(self.destination_folder, os.path.basename(self.full_path_to_zip).replace(".zip","")), exist_ok = True)
        print_color_msg(f"    Top level directory generated",Fore.YELLOW)
        return None
    
    def fix_meta_inf_folder(self) -> None:
        os.makedirs(os.path.join(self.destination_folder, "META-INF"))
        print_color_msg(f"    META-INF directory generated",Fore.YELLOW)
        return None

    def restructure_folder(self) -> None:
        for filename in os.listdir(self.destination_folder):
            if filename.endswith(".zip"):
                zip_path = os.path.join(self.destination_folder, filename)
                os.remove(zip_path)
                break
        for filename in os.listdir(self.destination_folder):
            if not os.path.basename(self.full_path_to_zip).replace(".zip","") in filename:
                folder_name = os.path.join(self.destination_folder, filename)
                des_folder = os.path.join(self.destination_folder, os.path.basename(self.full_path_to_zip).replace(".zip",""))
                shutil.move(folder_name, des_folder)
        print_color_msg(f"    Package content restructured",Fore.YELLOW)
        return None

    def fix_taxonomy_package_xml(self, source_folder: str) -> None:
        # set relevant elements and its content for the taxonomyPackage.xml file
        taxonomy_package_xml_settings: ET.Element = ET.Element('taxonomyPackage')
        taxonomy_package_xml_settings.set('xml:lang', 'en')
        taxonomy_package_xml_settings.set('xmlns', 'http://xbrl.org/2016/taxonomy-package')
        taxonomy_package_xml_settings.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        taxonomy_package_xml_settings.set('xsi:schemaLocation', 'http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd')
        taxonomy_package_xml_settings.append(ET.Comment('This file and its content has been generated and is not part of the original ZIP.'))
        # TODO: all strings in variable taxonomy_package_xml_metadata.text shoul dbe created dynamically
        taxonomy_package_xml_metadata: ET.Element
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'identifier')
        taxonomy_package_xml_metadata.text = "full/official/path/to/the/packge.zip"
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'name')
        taxonomy_package_xml_metadata.text = "ALL_2022-11-01.zip"
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'description')
        taxonomy_package_xml_metadata.text = "The ALL-2022-11-01 Taxonomy Package provided by the JFSA."
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'version')
        taxonomy_package_xml_metadata.text = "2023"
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publisher')
        taxonomy_package_xml_metadata.text = "Japanese Financial Service Agency"
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publisherURL')
        taxonomy_package_xml_metadata.text = "https://www.fsa.go.jp/en/"
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publicationDate')
        taxonomy_package_xml_metadata.text = "2022-11-01"
        # entrypoint list is almost generated dynamically
        entrypoints = ET.SubElement(taxonomy_package_xml_settings, 'entryPoints')
        file: str
        # TODO: yyyy-mm-dd should be generated dynamically
        for file in os.listdir(source_folder + "/samples/2022-11-01"):
            if file.endswith(".xsd"):
                taxonomy: ET.Element = ET.SubElement(entrypoints, 'entryPoint')
                # TODO: if necessary add relevant folder to generate entrypoint list
                elem: ET.Element = ET.SubElement(taxonomy, 'name')
                if "all" in os.path.abspath(file):
                    elem.text = "ALL : All Entry Points"
                elif "ifrs" in os.path.abspath(file):
                    elem.text = "IFRS : International Financial Reporting Standards"
                elif "jpcrp" in os.path.abspath(file):
                    elem.text = "JPCRP : Disclosure of Corporate Information"
                elif "jpctl" in os.path.abspath(file):
                    elem.text = "JPCTL : Internal Control Form No.1 Internal Control Report"
                elif "jpdei" in os.path.abspath(file):
                    elem.text = "JPDEI : Document and Entity information"
                elif "jpigp" in os.path.abspath(file):
                    elem.text = "JPIGP : Designed International Accounting Standards"
                elif "jplvh" in os.path.abspath(file):
                    elem.text = "JPLVH : Large Volume Holding"
                elif "jppfs" in os.path.abspath(file):
                    elem.text = "JPPFS : Primary Financial Statments"
                elif "jpsps" in os.path.abspath(file):
                    elem.text = "JPSPS : Disclosure of Information, etc. on Specified Securities"
                elif "jptoi" in os.path.abspath(file):
                    elem.text = "JPTOI : Tender Offer by Issuer"
                elif "jptoo" in os.path.abspath(file):
                    elem.text = "JPTOO : Tender Offer by Those Other than Issuer Form"
                else:
                    print("Please integrate new entry point group in script and in template!")
                    elem.text = "<missingEntry>"
                    break
                    
                elem = ET.SubElement(taxonomy, 'version')
                elem.text = "2023"
                ET.SubElement(taxonomy, 'entryPointDocument', { 'href': 'http://disclosure.edinet-fsa.go.jp/samples/' + "self.__get_tp_publication_date()" + '/' + file })

        taxonomy_package_content: str = parseString(ET.tostring(taxonomy_package_xml_settings, 'utf-8')).toprettyxml(indent='    ')
        taxonomy_package_xml_file: TextIOWrapper
        with open(os.path.join(source_folder, "META-INF", "taxonomyPackage.xml"), "w", encoding='utf-8') as taxonomy_package_xml_file:
            taxonomy_package_xml_file.write(taxonomy_package_content)
        print_color_msg(f"    taxonomyPackage.xml file generated",Fore.YELLOW)
        # check if taxonomyPackage.xml is an xml file
        if os.path.join(source_folder, "META-INF", "taxonomyPackage.xml").endswith(".xml"):
            print_color_msg(f"    taxonomyPackage.xml is xml file",Fore.YELLOW)
        else:
            print_color_msg(f'    ERROR: {os.path.join(source_folder, "META-INF", "taxonomyPackage.xml")} is not an xml file')
        
        # validate taxonomyPackage.xml file
        check_taxonomy_pkg_xml: TPChecker = TPChecker()
        check_taxonomy_pkg_xml.validate_xml("http://www.xbrl.org/2016/taxonomy-package.xsd",os.path.join(source_folder, "META-INF", "taxonomyPackage.xml"))
        return None

    def fix_catalog_xml(self, source_folder: str) -> None:
        # set relevant elements and its content for the catalog.xml file        
        catalog_xml_file: ET.Element = ET.Element("catalog")
        catalog_xml_file.set('xmlns', 'urn:oasis:names:tc:entity:xmlns:xml:catalog')
        catalog_xml_file.set('xmlns:spy', 'http://www.altova.com/catalog_ext')
        catalog_xml_file.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        catalog_xml_file.set('xsi:schemaLocation', 'urn:oasis:names:tc:entity:xmlns:xml:catalog Catalog.xsd')
        # write a path for each entry in "samples"
        samples_directory: str = f"{ source_folder }/samples"
        folder_paths: list[str] = [samples_directory.name for samples_directory in os.scandir(samples_directory) if samples_directory.is_dir()]
        samples_directory: str
        for samples_directory in folder_paths:
            ET.SubElement(catalog_xml_file, 'rewriteURI', { 'uriStartString': 'http://disclosure.edinet-fsa.go.jp/samples/' + samples_directory + '/', 'rewritePrefix': '../samples/' + samples_directory + '/' })
        # write a path for each entry in "taxonomy"
        taxonomy_directory: str = f"{ source_folder }/taxonomy"
        list_taxonomy_subdirs: list[str] = [taxonomy_directory.name for taxonomy_directory in os.scandir(taxonomy_directory) if taxonomy_directory.is_dir()]
        # iterate each folder, located in 'C:\\tmp\\taxonomy'
        str_taxonomy_subdir: str
        for str_taxonomy_subdir in list_taxonomy_subdirs:
            str_taxonomy_ep_shortname_subdir: str = f"{ source_folder }/taxonomy/{ str_taxonomy_subdir }"
            list_taxonomy_dir_ep_shortname_dir: list[str] = [str_taxonomy_ep_shortname_subdir.name for str_taxonomy_ep_shortname_subdir in os.scandir(str_taxonomy_ep_shortname_subdir) if str_taxonomy_ep_shortname_subdir.is_dir()]
            ep_shortname_dir_entry: str
            for ep_shortname_dir_entry in list_taxonomy_dir_ep_shortname_dir:
                new_path_to_directories: str = f"{ str_taxonomy_subdir }/{ ep_shortname_dir_entry }"
            # write corresponding path in "catalog.xml"
            ET.SubElement(catalog_xml_file, 'rewriteURI', { 'uriStartString': 'http://disclosure.edinet-fsa.go.jp/taxonomy/' + new_path_to_directories + '/', 'rewritePrefix': '../taxonomy/' + new_path_to_directories + '/' })
        catalog_file_content = parseString(ET.tostring(catalog_xml_file, 'utf-8')).toprettyxml(indent='    ')
        catalog_file: TextIOWrapper
        with open(os.path.join(source_folder, "META-INF", "catalog.xml"), "w", encoding='utf-8') as catalog_file:
            catalog_file.write(catalog_file_content)
        print_color_msg(f"    catalog.xml file generated",Fore.YELLOW)
        # check if catalog.xml is an xml file
        if os.path.join(source_folder, "META-INF", "catalog.xml").endswith(".xml"):
            print_color_msg(f"    catalog.xml is xml file",Fore.YELLOW)
        else:
            print_color_msg(f'    ERROR: {os.path.join(source_folder, "META-INF", "catalog.xml").endswith(".xml")} is not an xml file')        
        # validate catalog.xml file
        check_catalog_xml: TPChecker = TPChecker()
        check_catalog_xml.validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd",os.path.join(source_folder, "META-INF", "catalog.xml"))
        return None

class EBATaxonomyPackage(TaxonomyPackageFixerInterface):
    """Use this class to fix an EBA XBRL Taxonomy Package.
    
    The package in input/* folder as well as newer and older versions
    can be found here: https://www.eba.europa.eu/risk-analysis-and-data/reporting-frameworks/reporting-framework-3.3
    """    
    def convert_to_zip_archive(self) -> None:
        return None

    def fix_meta_inf_folder(self) -> None:
        return None

    def fix_top_level_single_dir(self) -> None:
        return None

    def restructure_folder(self) -> None:
        return None

    def fix_taxonomy_package_xml(self) -> None:
        return None
    
    def fix_catalog_xml(self) -> None:
        return None
