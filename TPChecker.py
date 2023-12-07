#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Checker.py

Provides all sorts of classes and functions to
analyze an XBRL Taxonomy Package.
"""

import os
import xml.etree.ElementTree as ET
from colorama import Fore
from lxml import etree
from zipfile import ZipFile
from urllib.parse import urljoin
from TPMisc import print_color_msg

class TPChecker:
    """The class provides methods to check an xbrl taxonomy package based on the standard here:
    https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html.
    """
    def __init__(self) -> None:
        """class constructor"""
        return None

    def check_case_sensitivity(self) -> None:
        """Standard description: 'A Conformant Processor MUST treat all filenames prescribed by this
        specification as being case-sensitive.'"""
        # NOTE: Python treats uppercase and lowercase letters as distinct characters.
        # This means that variable and Variable are different identifiers. There is
        # no need for a separate function, to check case sensitivity.
        return None

    def has_zip_format(self, archive: str) -> bool:
        """Standard description: 'A Taxonomy Package MUST conform to the .ZIP File Format
        Specification [ZIP]'"""
        if archive.endswith(".zip"):
            return True
        else:
            return False

    def has_top_level_single_dir(self, archive: str) -> bool:
        """Standard description: 'A Taxonomy Package MUST contain a single top-level directory, with all other files being
        contained within that directory or descendant subdirectories (tpe:invalidDirectoryStructure).'"""
        archive_res: str = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        zip_file: ZipFile
        with ZipFile(archive_res, "r") as zip_file:
            top_dir: set = {item.split('/')[0] for item in zip_file.namelist()}
            if len(top_dir) == 1:
                return True
            else:
                return False

    def validate_xml(self, schemafile: str, example: ET.ElementTree) -> bool:
        """Standard description: 'The taxonomyPackage.xml MUST conform to the taxonomy-package.xsd
        schema (Appendix B.1) (tpe:invalidMetaDataFile).
        
        If present, the catalog.xml file MUST be a valid XML Catalog file, as defined by the XML Catalog specification
        [XML Catalogs] and MUST also conform to the restricted schema defined by this specification (see Appendix B.2)
        (tpe:invalidCatalogFile).'"""
        try:
            xml_document: ET.ElementTree = etree.parse(example)
            xml_schema = etree.XMLSchema(file = schemafile)
            if xml_schema.assertValid(xml_document):
                return True
        except etree.XMLSchemaError as schema_error:
            print_color_msg(f"    XML Schema Error: {schema_error}",Fore.YELLOW)
        except etree.DocumentInvalid as document_invalid:
            print_color_msg(f"    Document Invalid: {document_invalid}",Fore.YELLOW)
        except Exception as e:
            print_color_msg(f"    An error occurred: {e}",Fore.YELLOW)
        return False         

    def has_meta_inf_folder(self, archive: str, folder_name: str = "META-INF") -> bool:
        """Standard description: 'The top-level directory MUST contain a sub directory named META-INF.'"""
        zipfilepath: str = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(str(archive).replace("\\", "/").replace("..",""))
        zip_file: ZipFile
        with ZipFile(zipfilepath, 'r') as zip_file:
            archive_contents = zip_file.namelist()
            for folder in archive_contents:
                if folder_name in folder:
                    return True
                else:
                    continue
            return False

    def has_taxonomy_package_xml(self, archive: str, tp_file: str = "taxonomyPackage.xml") -> bool:
        """Standard description: 'The top-level directory MUST contain a taxonomyPackage.xml file.'"""
        zip_file_path: str = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        zip_file: ZipFile
        with ZipFile(zip_file_path, 'r') as zip_file:
            archive_contents: object = zip_file.namelist()
            for folder in archive_contents:
                if tp_file in folder:
                    return True
                else:
                    continue
            return False

    def has_catalog_xml(self, archive, catalog_file: str = "catalog.xml") -> bool:
        """Standard description: 'The top-level directory MUST ontain a catalog.xml file
        
        A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element
        with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification)
        for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString).'"""
        zipfilepath: str = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        zip_file: ZipFile
        with ZipFile(zipfilepath, 'r') as zip_file:
            archive_contents = zip_file.namelist()
            for folder in archive_contents:
                if catalog_file in folder:
                    return True
                else:
                    continue
            return False

    # TODO: Further development and testing needed. It is assumed though that the
    # xml base resolution is valid, because providers test the package as well.
    def check_rel_url_base_resolution(self, file: str, base_url: str) -> bool:
        """Standard description: 'Relative URLs MUST undergo XML Base resolution [XML Base].
        More info here: https://www.w3.org/TR/xmlbase/#syntax
        
        Example:

        <?xml version="1.0"?>
        <doc xml:base="http://example.org/today/" xmlns:xlink="http://www.w3.org/1999/xlink">
            <head>
                <title>Virtual Library</title>
            </head>
            <body>
                <paragraph>See <link xlink:type="simple" xlink:href="new.xml">what's
                new</link>!</paragraph>
                <paragraph>Check out the hot picks of the day!</paragraph>
                <olist xml:base="/hotpicks/">
                    <item>
                        <link xlink:type="simple" xlink:href="pick1.xml">Hot Pick #1</link>
                    </item>
                    <item>
                        <link xlink:type="simple" xlink:href="pick2.xml">Hot Pick #2</link>
                    </item>
                    <item>
                        <link xlink:type="simple" xlink:href="pick3.xml">Hot Pick #3</link>
                    </item>
                </olist>
            </body>
        </doc>

        The URIs in this example resolve to full URIs as follows:
        "what's new" resolves to the URI "http://example.org/today/new.xml"
        "Hot Pick #1" resolves to the URI "http://example.org/hotpicks/pick1.xml"
        "Hot Pick #2" resolves to the URI "http://example.org/hotpicks/pick2.xml"
        "Hot Pick #3" resolves to the URI "http://example.org/hotpicks/pick3.xml"
        '"""
        def resolve_xml_base(file, base_url):
            root: ET.Element = ET.fromstring(file)
            elements_to_resolve: list[ET.Element] = root.findall('.//*[@xlink:href or @xml:base]')
            for element in elements_to_resolve:
                if 'xlink:href' in element.attrib:
                    element.attrib['xlink:href'] = urljoin(base_url, element.attrib['xlink:href'])
                if 'xml:base' in element.attrib:
                    element.attrib['xml:base'] = urljoin(base_url, element.attrib['xml:base'])
            return ET.tostring(root).decode()

        if resolve_xml_base(file, base_url):
            return True
        else:
            return False

    # TODO: Further development and testing needed. It is assumed though that the
    # entry point check is valid, because providers test the package as well.
    def check_entry_point_location(self, input_document: str) -> bool:
        """Standard description: 'A Conformant Processor MUST refuse to open any entry point where one or more of
        its <tp:entryPointDocument> URLs resolve to anything other than a taxonomy schema or linkbase document.'"""
        def is_taxonomy_schema(input_document: str) -> bool:
            try:
                root: ET.Element = ET.fromstring(input_document)
                app_info_elems: list[ET.Element] = root.findall(".//{http://www.w3.org/2001/XMLSchema}appinfo")
                if app_info_elems:
                    return True
                else:
                    return False
            except ET.ParseError as e:
                print_color_msg(f"ERROR: Parsing XML file {e} went wrong!",Fore.RED)
                return False

        def is_linkbase_document(input_document: str) -> bool:
            try:
                root: ET.Element = ET.fromstring(input_document)
                linkbase_elements: list[ET.Element] = root.findall(".//{http://www.xbrl.org/2003/linkbase}linkbase")
                if linkbase_elements:
                    return True
                else:
                    return False
            except ET.ParseError as e:
                print(f"Error parsing XML: {e}")
                return False

        if is_taxonomy_schema(input_document) or is_linkbase_document(input_document):
            print(f"{input_document} is a taxonomy document.")
            return True
        else:
            print(f"{input_document} is not a taxonomy document.")
            return False
