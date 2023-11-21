#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod
import os
import sys
import xml.etree.ElementTree as ET
from zipfile import ZipFile

class Checker:
    """"""
    def __init__(self) -> None:
        """class constructor"""
        return None

    def check_case_sensitivity(self) -> None:
        """A Conformant Processor MUST treat all filenames prescribed by this
        specification as being case-sensitive."""
        # Python treats uppercase and lowercase letters as distinct characters.
        # This means that variable and Variable are different identifiers.
        return None

    def has_zip_format(self, archive: str) -> bool:
        """A Taxonomy Package MUST conform to the .ZIP File Format
        Specification [ZIP]"""
        if archive.endswith(".zip"):
            return True
        else:
            return False

    def has_top_level_single_dir(self, archive: str) -> bool:
        """A Taxonomy Package MUST contain a single top-level directory, with all other files being
        contained within that directory or descendant subdirectories (tpe:invalidDirectoryStructure)."""
        archive_res: str = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        with ZipFile(archive_res, "r") as zip_file:
            top_dir = {item.split('/')[0] for item in zip_file.namelist()}
            if len(top_dir) == 1:
                return True
            else:
                return False

    def is_xml(self, filename: str) -> bool:
        """The taxonomyPackage.xml file MUST be an XML file [XML]"""
        if filename.endswith(".xml"):
            return True
        else:
            return False

    def validate_xml(self, schemafile: str, example: str) -> bool:
        """The taxonomyPackage.xml MUST conform to the taxonomy-package.xsd
        schema (Appendix B.1) (tpe:invalidMetaDataFile).
        
        If present, the catalog.xml file MUST be a valid XML Catalog file, as defined by the XML Catalog specification [XML Catalogs] and MUST also conform to the restricted schema defined by this specification (see Appendix B.2) (tpe:invalidCatalogFile). 
        """
        schema = XMLSchema(schemafile)
        tree = ET.parse(example)
        if not tree.validate(schema):
            raise ValueError('The XML document is invalid.')
        else:
            print("Schema is valid!")
            return True

    def has_meta_inf_folder(self, archive: zip, folder_name: str = "META-INF") -> bool:
        """The top-level directory MUST contain a sub directory named META-INF """
        zipfilepath = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        with ZipFile(zipfilepath, 'r') as zip_file:
            archive_contents = zip_file.namelist()
            for folder in archive_contents:
                if folder_name in folder:
                    return True
                else:
                    continue
            return False

    def has_taxonomy_package_xml(self, archive, tp_file: str = "taxonomyPackage.xml") -> bool:
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
        zipfilepath = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        with ZipFile(zipfilepath, 'r') as zip_file:
            archive_contents = zip_file.namelist()
            for folder in archive_contents:
                if tp_file in folder:
                    return True
                else:
                    continue
            return False

    def has_catalog_xml(self, archive, catalog_file: str = "catalog.xml") -> bool:
        """The top-level directory MUST ontain a catalog.xml file
        
        A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element
        with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification)
        for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString). 
        """
        zipfilepath = os.path.dirname(os.path.abspath(__file__)) + os.path.abspath(archive.replace("\\", "/").replace("..",""))
        with ZipFile(zipfilepath, 'r') as zip_file:
            archive_contents = zip_file.namelist()
            for folder in archive_contents:
                if catalog_file in folder:
                    return True
                else:
                    continue
            return False    

    def check_rel_url_base_resolution(self):
        """Relative URLs MUST undergo XML Base resolution [XML Base].
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
        """
        import xml.etree.ElementTree as ET
        from urllib.parse import urljoin

        def resolve_xml_base(xml_string, base_url):
            # Parse the XML string
            root = ET.fromstring(xml_string)

            # Find all elements with attributes that need resolution (e.g., xlink:href, xml:base)
            elements_to_resolve = root.findall('.//*[@xlink:href or @xml:base]')

            for element in elements_to_resolve:
                # Resolve xlink:href attribute
                if 'xlink:href' in element.attrib:
                    element.attrib['xlink:href'] = urljoin(base_url, element.attrib['xlink:href'])

                # Resolve xml:base attribute
                if 'xml:base' in element.attrib:
                    element.attrib['xml:base'] = urljoin(base_url, element.attrib['xml:base'])

            # Return the modified XML string
            return ET.tostring(root).decode()

        # Example XML string
        xml_string = '''
        <doc xml:base="http://example.org/today/" xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <paragraph>See <link xlink:type="simple" xlink:href="new.xml">what's new</link>!</paragraph>
                <paragraph>Check out the hot picks of the day!</paragraph>
            </body>
        </doc>
        '''

        # Example base URL
        base_url = "http://example.org/today/"

        # Resolve XML Base
        resolved_xml = resolve_xml_base(xml_string, base_url)
        print(resolved_xml)

    def check_entry_point_location(self):
        """A Conformant Processor MUST refuse to open any entry point where one or more of
        its <tp:entryPointDocument> URLs resolve to anything other than a taxonomy schema or linkbase document."""
        import xml.etree.ElementTree as ET
        import requests

        def is_taxonomy_document(url):
            try:
                # Fetch the content of the URL
                response = requests.get(url)

                # Check if the content type is XML (you may need to adjust this condition)
                if response.headers['Content-Type'] == 'application/xml':
                    # Parse the XML content
                    root = ET.fromstring(response.content)

                    # Check if the document is a taxonomy schema or linkbase document
                    # You need to replace 'your_condition_here' with the actual condition based on your schema
                    if 'your_condition_here':
                        return True
            except Exception as e:
                print(f"Error checking {url}: {e}")

            # Example: Check if a URL is a taxonomy document
            entry_point_url = "http://example.com/your_entry_point_document.xml"
            if is_taxonomy_document(entry_point_url):
                print(f"{entry_point_url} is a taxonomy document.")
            else:
                print(f"{entry_point_url} is not a taxonomy document.")


                # Example: Check if a URL is a taxonomy document
                entry_point_url = "http://example.com/your_entry_point_document.xml"
                if is_taxonomy_document(entry_point_url):
                    print(f"{entry_point_url} is a taxonomy document.")
                else:
                    print(f"{entry_point_url} is not a taxonomy document.")
                    # multilingual element checks

            return False

class TaxonomyPackageFixerInterface(ABC):
    """The fix is very specifc to the 
    """
    def __init__(self):
        """"""

    @abstractmethod
    def fix_zip_format(self):
        """"""

    @abstractmethod
    def fix_top_level_single_dir(self):
        """"""

    @abstractmethod
    def fix_meta_inf_folder(self):
        """"""

    @abstractmethod
    def fix_taxonomy_package_xml(self):
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
    
    @abstractmethod
    def fix_catalog_xml(self):
        """The top-level directory MUST ontain a catalog.xml file
        
        A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification) for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString). 
        """
