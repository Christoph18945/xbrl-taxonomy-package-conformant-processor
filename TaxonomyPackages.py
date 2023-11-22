#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse
from email import message
from pathlib import Path
import pprint
import re
import os
import sys
import json
from tkinter import N
from tracemalloc import stop
from typing import Match
from xml.dom.minidom import Element, parseString
import xml.etree.ElementTree as ET
import zipfile
import subprocess
import xml.dom.minidom
import datetime
from io import BufferedReader, TextIOWrapper
from multiprocessing.dummy import Namespace
import logging
from lxml import etree
import shutil
import collections
import time
import PyPDF2
from bs4 import BeautifulSoup
from numpy import iterable
import pandas as pd
import requests
from termcolor import colored
from collections import OrderedDict
import packaging.version
from Data.AltovaSoftwareData import Raptor
from XMLData.XMLDataException import XMLDataException
from XMLData.RawBB import RawBB
import shutil
import sys
import zipfile
from colorama import Fore, Style, init
import argparse
import os
from Processor import Checker
from Processor import TaxonomyPackageFixerInterface
from Misc import extract_zip_in_same_folder, gen_zip_package

class CMFCLCITaxonomyPackage(TaxonomyPackageFixerInterface):
    """
    Use this class to fix the CMF CL-CI raw building block. Example download can be found here:
    https://www.cmfchile.cl/portal/principal/613/w3-propertyvalue-43598.html#especial_taxonomias
    NOTE: Make sure, that no other file, etc is located in source folder!
    """

    def __init__(self, source_zip: str, destination_folder: str) -> None:
        """class constructor"""
        # copy file to output folder
        shutil.move(source_zip, destination_folder)
        # self.source_zip = source_zip
        # self.source_zip_path = source_zip
        # self.destination_folder = destination_folder
        # set the path to the zip archive in output folder
        self.zip_output_folder = destination_folder + os.path.basename(source_zip)

    def fix_meta_inf_folder(self):
        """create a META-INF folder for the package"""
        zip_file_path = self.zip_output_folder
        extract_zip_in_same_folder(zip_file_path)

        # iterate over folder to find root folder of package:
        for root, dirs, files in os.walk(self.zip_output_folder):
            for file_name in files:
                if  not ".zip" in file_name:
                    full_path_to_root_folder = os.path.join(root, file_name)
                    # Process each file path as needed
                    # print(full_path_to_meta_inf)
                    break

        # create META-INF in root folder
        m_inf_f = os.path.join(full_path_to_root_folder, "META-INF")
        try:
            os.makedirs(m_inf_f)
            print(f"Folder '{m_inf_f}' created successfully.")
        except FileExistsError:
            print(f"Folder '{m_inf_f}' already exists.")

        # get source file to meta-inf folder
        full_path_meta_inf_folder = os.path.join(full_path_to_root_folder, "META-INF")

    def fix_taxonomy_package_xml():
        """Design and generate the 'taxonomyPackage.xml' file."""
        # Version Pattern for year and/or months and/or day
        yearMonthDaySearchPattern: Match[str] = re.search(r'\d{4}-\d{2}-\d{2}', self.__get_new_zip_archive_name())
        yearMonthSearchPattern: Match[str] = re.search(r'\d{4}-\d{2}', self.__get_new_zip_archive_name())
        yearSearchPattern: Match[str] = re.search(r'\d{4}', self.__get_new_zip_archive_name())
        # tp:version
        tpVersion: str = ""
        if yearMonthDaySearchPattern != None:
            tpVersion = str(yearMonthDaySearchPattern.group()) 
        elif yearMonthSearchPattern != None:
            tpVersion = str(yearMonthSearchPattern.group()) 
        elif yearSearchPattern != None:
            tpVersion = str(yearSearchPattern.group()) 
        else:
            print(colored(f"Search Pattern not defined for : { self.__get_new_zip_archive_name() }", "red"))

        xmlP: ET.Element = ET.Element("tp:taxonomyPackage")
        xmlP.set('xml:lang', 'en')
        xmlP.set('xmlns:tp', 'http://xbrl.org/2016/taxonomy-package')
        xmlP.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xmlP.set('xsi:schemaLocation', 'http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd')
        xmlP.append(ET.Comment('This file and its content has been generated and is not part of the original ZIP.')) 

        elem: Element
        elem = ET.SubElement(xmlP, 'tp:identifier')
        elem.text = self.__get_new_zip_archive_name()

        elem = ET.SubElement(xmlP, 'tp:name')
        elem.text = self.__get_new_zip_archive_name().replace(".zip", "").replace("-" +tpVersion, "") + " XBRL Taxonomy"

        elem = ET.SubElement(xmlP, 'tp:description')
        if "CMF" in str(self.__get_new_path_to_package()):
            elem.text = "Expanded IFRS " + str(datetime.date.today().year) + " taxonomy with additional Chilean regulations added"

        elem = ET.SubElement(xmlP, 'tp:version')
        elem.text = tpVersion

        elem = ET.SubElement(xmlP, 'tp:publisher')
        if "CMF" in str(self.__get_new_path_to_package()):
            elem.text = "Comision para el Mercado Financiero"

        elem = ET.SubElement(xmlP, 'tp:publisherURL')
        if "CMF" in str(self.__get_new_path_to_package()):
            elem.text = "https://www.cmfchile.cl/portal/principal/613/w3-channel.html"

        elem = ET.SubElement(xmlP, 'tp:publicationDate')
        elem.text = tpVersion

        xmlEPs: ET.Element
        xmlEPs = ET.SubElement(xmlP, 'tp:entryPoints')
        for schemaName in self.__extract_entry_points():
            xmlEP = ET.SubElement(xmlEPs, 'tp:entryPoint')

            elemName = ET.SubElement(xmlEP, 'tp:name')
            elemName.text = os.path.basename(schemaName).replace("_", "-").replace(".xsd", "")

            epFileName: str = os.path.basename(schemaName)
            fullEPDate: Match[str] = re.search(r'\d{4}-\d{2}-\d{2}', epFileName)
            if fullEPDate != None:
                epVersion = str(fullEPDate.group()) 

                elemVersion: ET.Element = ET.SubElement(xmlEP, 'tp:version')
                elemVersion.text = epVersion

            if "CMF" in self.__get_new_path_to_package():
                x = "http://www.cmfchile.cl/cl/fr/ci/" + tpVersion + "/" + schemaName.replace("CL_CI_2023", "").replace("CMF-CL-CI-" +tpVersion, "")
                ET.SubElement(xmlEP, 'tp:entryPointDocument', { 'href': x})

        str_xml_pkg = parseString(ET.tostring(xmlP, 'utf-8')) .toprettyxml(indent='    ')

        if os.path.isfile(self.source_folder + '/' + 'taxonomyPackage.xml') is False:
            tp_xml_file: TextIOWrapper
            with open(os.path.join(self.source_folder, 'taxonomyPackage.xml').replace("\\", "/"), "w", encoding='utf-8') as tp_xml_file:
                tp_xml_file.write(str_xml_pkg)
            tp_xml_file.close()
        else:
            pass

    def fix_catalog_xml(self):
        """Design and generate the 'catalog.xml'"""
        # Design the file:
        xml_catalog_elements: ET.Element = ET.Element("catalog")
        xml_catalog_elements.set('xmlns', 'urn:oasis:names:tc:entity:xmlns:xml:catalog')
        xml_catalog_elements.set('xmlns:spy', 'http://www.altova.com/catalog_ext')
        xml_catalog_elements.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        xml_catalog_elements.set('xsi:schemaLocation', 'urn:oasis:names:tc:entity:xmlns:xml:catalog Catalog.xsd')

        archive_name_year = re.search(r'\d{4}', PKG_VERSION)
        if archive_name_year is not None:
            cat_entry_version = str(archive_name_year.group())
        else:
            print("ERROR: Pattern for year not found!")

        ET.SubElement(xml_catalog_elements, 'rewriteURI', { 'uriStartString': 'http://www.cmfchile.cl/cl/fr/ci/' + str(PKG_VERSION) + '/', 'rewritePrefix': '../CL-CI-' + cat_entry_version + '/' })

        str_xml_c = parseString(ET.tostring(xml_catalog_elements, 'utf-8' )).toprettyxml(indent='    ')

        # Generate the file.
        if os.path.isfile(self.source_folder + '/' + 'catalog.xml') is False:
            with open(os.path.join(self.source_folder, "catalog.xml").replace("\\", "/"), "w", encoding='utf-8') as catalog_xml_file:
                catalog_xml_file.write(str_xml_c)
            catalog_xml_file.close()
        else:
            print(colored("WARNING: 'catalog.xml' file already exists!", "yellow"))        
        
        # this is relevant for the files here!
        gen_zip_package()

class EBATaxonomyPackage(TaxonomyPackageFixerInterface):
    """"""
    def __init__(self):
        """"""

class EDINETTaxonomyPackage(TaxonomyPackageFixerInterface):
    """
    Use this class to fix an EDINET raw building block. The
    building block is a taxonomy package provided by the JFSA.
    """
    def __init__(self):
        """"""

    def __get_edinet_entry_point_version(self) -> str:
        """Get version of a single entry point. Version is extracted
        out of package name.
        """
        return self.zip_archive[4:8]

    def _get_package_version(self) -> str:
        return str(datetime.datetime.now().year)

    def __get_edinet_tp_name(self) -> str:
        """Get name for package
        """
        return "EDINET XBRL Taxonomy " + str(int(self._get_package_version()) + 1)

    def __get_edinet_tp_description(self) -> str:
        """Get description of the given edinet taxonomy package.
        """
        return "EDINET XBRL Taxonomy " + self.zip_archive[8:10] + "/" + self._get_package_version() + " to support detailed labelling of corporate governance-related information and international accounting standards."

    def __get_edinet_publisher(self) -> str:
        """Get name of the publisher
        """
        return "Japanese FSA"

    def __get_edinet_publisher_uri(self) -> str:
        """Get uri of edinet publisher
        """
        return "https://www.fsa.go.jp/index.html"

    def __get_tp_publication_date(self) -> str:
        """Get publication date of package.
        """
        base_date = (self.zip_archive.split('_')[1]).split('.')[0]
        publication_date: str = f"{ base_date[:4] }-{ base_date[4:6] }-{ base_date[6:] }"
        return publication_date

    def __generate_new_tp_name(self):
        """Generate new name for the package. Means replace
        'ALL' with 'EDINET'.
        """
        return self.zip_archive.replace("ALL", "EDINET")

    def __extract_edinet_archive(self) -> zipfile.ZipFile:
        """0/8. Extract content of ZIP file
        """
        print("Extract data to work with ...")
        zip_file_ref: zipfile.ZipFile = zipfile.ZipFile(os.path.join(self.source_folder, self.zip_archive))
        zip_file_ref.extractall(self.source_folder)
        zip_file_ref.close()

    def __generate_metainf_folder(self) -> None:
        """1/8. Create 'META-INF' folder.
        """
        print("Create 'META-INF' folder ...")
        try:
            return os.mkdir(os.path.join(self.source_folder, "META-INF"))
        except FileExistsError:
            print(colored("WARNING: 'META-INF' folder not created - it exists already in folder or path is wrong!", "yellow"))

    def __write_taxonomy_package_xml(self) -> None:
        """2/8. Generate "taxonomyPackage.xml" file.
        """
        print("Write the 'taxonomyPackage.xml' file ...")
        taxonomy_package_xml_settings: ET.Element = ET.Element('taxonomyPackage')
        taxonomy_package_xml_settings.set('xml:lang', 'en')
        taxonomy_package_xml_settings.set('xmlns', 'http://xbrl.org/2016/taxonomy-package')
        taxonomy_package_xml_settings.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        taxonomy_package_xml_settings.set('xsi:schemaLocation', 'http://xbrl.org/2016/taxonomy-package http://xbrl.org/2016/taxonomy-package.xsd')
        taxonomy_package_xml_settings.append(ET.Comment('This file and its content has been generated and is not part of the original ZIP.'))
        taxonomy_package_xml_metadata: ET.Element
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'identifier')
        taxonomy_package_xml_metadata.text = self.__generate_new_tp_name()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'name')
        taxonomy_package_xml_metadata.text = self.__get_edinet_tp_name()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'description')
        taxonomy_package_xml_metadata.text = self.__get_edinet_tp_description()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'version')
        taxonomy_package_xml_metadata.text = self.__get_edinet_tp_description()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publisher')
        taxonomy_package_xml_metadata.text = self.__get_edinet_publisher()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publisherURL')
        taxonomy_package_xml_metadata.text = self.__get_edinet_publisher_uri()
        taxonomy_package_xml_metadata = ET.SubElement(taxonomy_package_xml_settings, 'publicationDate')
        taxonomy_package_xml_metadata.text = self.__get_tp_publication_date()
        entrypoints = ET.SubElement(taxonomy_package_xml_settings, 'entryPoints')
        file: str
        for file in os.listdir(self.source_folder + "\\samples\\" + self.__get_tp_publication_date()):
            if file.endswith(".xsd"):
                taxonomy: ET.Element = ET.SubElement(entrypoints, 'entryPoint')
                # If necessary add relevant folder names!
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
                elem.text = self.__get_edinet_entry_point_version()
                ET.SubElement(taxonomy, 'entryPointDocument', { 'href': 'http://disclosure.edinet-fsa.go.jp/samples/' + self.__get_tp_publication_date() + '/' + file })

        taxonomy_package_content: str = parseString(ET.tostring(taxonomy_package_xml_settings, 'utf-8')).toprettyxml(indent='    ')

        taxonomy_package_xml_file: TextIOWrapper
        with open(os.path.join(self.source_folder, "taxonomyPackage.xml"), "w", encoding='utf-8') as taxonomy_package_xml_file:
            taxonomy_package_xml_file.write(taxonomy_package_content)

    def __write_catalog_xml(self):
        """3/8. Generate "catalog.xml" file for the EDINET taxonomies.
        """
        print("Write the 'catalog.xml' file ...")
        catalog_xml_file: ET.Element = ET.Element("catalog")
        catalog_xml_file.set('xmlns', 'urn:oasis:names:tc:entity:xmlns:xml:catalog')
        catalog_xml_file.set('xmlns:spy', 'http://www.altova.com/catalog_ext')
        catalog_xml_file.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        catalog_xml_file.set('xsi:schemaLocation', 'urn:oasis:names:tc:entity:xmlns:xml:catalog Catalog.xsd')

        # write a path for each entry in "samples"
        samples_directory: str = f"{ self.source_folder }\\samples"
        folder_paths: list[str] = [samples_directory.name for samples_directory in os.scandir(samples_directory) if samples_directory.is_dir()]
        samples_directory: str
        for samples_directory in folder_paths:
            ET.SubElement(catalog_xml_file, 'rewriteURI', { 'uriStartString': 'http://disclosure.edinet-fsa.go.jp/samples/' + samples_directory + '/', 'rewritePrefix': '../samples/' + samples_directory + '/' })

        # write a path for each entry in "taxonomy"
        taxonomy_directory: str = f"{ self.source_folder }\\taxonomy"
        list_taxonomy_subdirs: list[str] = [taxonomy_directory.name for taxonomy_directory in os.scandir(taxonomy_directory) if taxonomy_directory.is_dir()]
        
        # iterate each folder, located in 'C:\\tmp\\taxonomy'
        str_taxonomy_subdir: str
        for str_taxonomy_subdir in list_taxonomy_subdirs:
            str_taxonomy_ep_shortname_subdir: str = f"{ self.source_folder }\\taxonomy\\{ str_taxonomy_subdir }"
            list_taxonomy_dir_ep_shortname_dir: list[str] = [str_taxonomy_ep_shortname_subdir.name for str_taxonomy_ep_shortname_subdir in os.scandir(str_taxonomy_ep_shortname_subdir) if str_taxonomy_ep_shortname_subdir.is_dir()]
            
            # iterate over each folder, lcated in C:\\tm\\taxonomy\\<folder_with_ep_shortname>
            ep_shortname_dir_entry: str
            for ep_shortname_dir_entry in list_taxonomy_dir_ep_shortname_dir:
                new_path_to_directories: str = f"{ str_taxonomy_subdir }/{ ep_shortname_dir_entry }"
            
            # write corresponding path in "catalog.xml"
            ET.SubElement(catalog_xml_file, 'rewriteURI', { 'uriStartString': 'http://disclosure.edinet-fsa.go.jp/taxonomy/' + new_path_to_directories + '/', 'rewritePrefix': '../taxonomy/' + new_path_to_directories + '/' })

        catalog_file_content = parseString(ET.tostring(catalog_xml_file, 'utf-8')).toprettyxml(indent='    ')

        catalog_file: TextIOWrapper
        with open(os.path.join(self.source_folder, "catalog.xml"), "w", encoding='utf-8') as catalog_file:
            catalog_file.write(catalog_file_content)
        
        # 4/8. Move 'catalog.xml' and 'taxonomyPackage.xml' into META-INF directory
        if len(os.listdir(os.path.join(self.source_folder, "META-INF"))) != 0:
            filelist: list[str] = [folder_item for folder_item in os.listdir(os.path.join(self.source_folder, "META-INF")) if folder_item.endswith(".xml")]
            folder_item: str
            for folder_item in filelist:
                os.remove(os.path.join(os.path.join(self.source_folder, "META-INF"), folder_item))
            item: str
            for item in os.listdir(self.source_folder):
                if "catalog" in item:
                    print("Move 'catalog.xml' into 'META-INF' folder ...")
                    shutil.move(os.path.join(self.source_folder, item), os.path.join(self.source_folder, "META-INF"))
                if "taxonomyPackage" in item:
                    print("Move 'taxonomyPackage.xml' into 'META-INF' folder ...")
                    shutil.move(os.path.join(self.source_folder, item), os.path.join(self.source_folder, "META-INF"))
                    
        else:
            item: str
            for item in os.listdir(self.source_folder):
                if "catalog" in item:
                    print("Move 'catalog.xml' into 'META-INF' folder ...")
                    shutil.move(os.path.join(self.source_folder, item), os.path.join(self.source_folder, "META-INF"))
                    
                
                if "taxonomyPackage" in item:
                    print("Move 'taxonomyPackage.xml' into 'META-INF' folder ...")                    
                    shutil.move(os.path.join(self.source_folder, item), os.path.join(self.source_folder, "META-INF"))
  
    def __move_foders(self) -> None:
        """5/8. Move rest of the files into the root directory of the taxonomy
        """
        print("Move all needed files into root directory ...")
        new_package_name: str = self.__generate_new_tp_name()
        str_zip_file_name_for_root: str = new_package_name.replace(".zip", "") # e.g. 'EDINET_20221101'

        if os.path.isdir(os.path.join(self.source_folder, str_zip_file_name_for_root)):
            print(colored(f"WARNING: '{ str_zip_file_name_for_root }' already exists!", "yellow"))
        else:
            print(f"Create '{ str_zip_file_name_for_root }' folder ...")
            os.mkdir(os.path.join(self.source_folder, str_zip_file_name_for_root))

        all_subdirectories: list[str] = [package_folder.name for package_folder in os.scandir(self.source_folder) if package_folder.is_dir()]
        # Move files into root directory
        try:
            root_files: str
            for root_files in all_subdirectories:
                shutil.move(os.path.join(self.source_folder, root_files), os.path.join(self.source_folder, str_zip_file_name_for_root))
        except Exception as exc:
            raise XMLDataException(f"Files already in destination path ... { str(self.source_folder) }") from exc

    def __generate_ready_made_package(self):
        """6/8. Pack all the files together in a ZIP
        """
        self.__extract_edinet_archive()
        self.__generate_metainf_folder()
        self.__write_taxonomy_package_xml()
        self.__write_catalog_xml()
        self.__move_foders()
        new_tp_name: str = self.__generate_new_tp_name()
        self._gen_zip_package(os.path.join(self.source_folder, new_tp_name.replace( ".zip", "")), os.path.join(self.source_folder, new_tp_name))
        # Clean up remaining folder remaining folder
        shutil.rmtree(os.path.join(self.source_folder, new_tp_name.replace(".zip", "")))
        time.sleep(10)

    def __del_old_package(self) -> None:
        """7/8. Delete ZIP archive.
        """
        print(f"Cleaning up workspace '{ self.source_folder }' ...")
        if os.path.join('S:\\Development\\internal\\XMLData\\Downloaded\\taxonomies\\EDINET\\EDINET-Taxonomies\\EDINET-TAXONOMY\\ALL_EDINET\\', self.zip_archive):
            print(colored("WARNING: Directory that should be cleaned up, already exists at destination or does not exist in source!", "yellow"))
            os.remove(os.path.join(self.source_folder, self.zip_archive))
        else:
            shutil.move((f'{ self.source_folder }\\{ self.zip_archive }'), 'S:\\Development\\internal\\XMLData\\Downloaded\\taxonomies\\EDINET\\EDINET-Taxonomies\\EDINET-TAXONOMY\\ALL_EDINET\\')

    def fix_edinet_package(self) -> None:
        """8/8. Fix the package - should be ready-made now.
        """
        self.__generate_ready_made_package()
        self.__del_old_package()
        print(colored(f'DONE: { self.__generate_new_tp_name() } generated.', 'green'))

