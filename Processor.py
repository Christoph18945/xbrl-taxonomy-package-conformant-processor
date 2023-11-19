#!/usr/bin/python3
# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class Checker:
    """"""
    def __init__(self):
        """class constructor"""

    def check_case_sensitivity(self):
        """A Conformant Processor MUST treat all filenames prescribed by this
        specification as being case-sensitive."""
    
    def is_xml(self):
        """The taxonomyPackage.xml file MUST be an XML file [XML]"""

    def validate_xml(self):
        """The taxonomyPackage.xml MUST conform to the taxonomy-package.xsd
        schema (Appendix B.1) (tpe:invalidMetaDataFile).
        
        If present, the catalog.xml file MUST be a valid XML Catalog file, as defined by the XML Catalog specification [XML Catalogs] and MUST also conform to the restricted schema defined by this specification (see Appendix B.2) (tpe:invalidCatalogFile). 
        """

    def has_zip_format(self):
        """A Taxonomy Package MUST conform to the .ZIP File Format
        Specification [ZIP]"""

    def has_top_level_single_dir(self):
        """A Taxonomy Package MUST contain a single top-level directory, with all other files being
        contained within that directory or descendant subdirectories (tpe:invalidDirectoryStructure)."""
    
    def has_meta_inf_folder(self):
        """The top-level directory MUST contain a sub directory named META-INF """

    def has_taxonomy_package_xml(self):
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
    
    def has_catalog_xml(self):
        """The top-level directory MUST ontain a catalog.xml file
        
        A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification) for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString). 
        """

    def check_rel_url_base_resolution(self):
        """Relative URLs MUST undergo XML Base resolution [XML Base]."""

    def check_entry_point_location(self):
        """A Conformant Processor MUST refuse to open any entry point where one or more of its <tp:entryPointDocument> URLs resolve to anything other than a taxonomy schema or linkbase document."""

    # multilingual element checks

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
