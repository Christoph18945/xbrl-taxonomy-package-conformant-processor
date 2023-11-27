#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""Fixer.py"""

from abc import ABC, abstractmethod

class TaxonomyPackageFixerInterface(ABC):
    """The fix is very specifc to the 
    """
    @abstractmethod
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
    def restructure_folder(self):
        """"""

    @abstractmethod
    def fix_taxonomy_package_xml(self):
        """The top-level directory MUST contain a taxonomyPackage.xml file"""
    
    @abstractmethod
    def fix_catalog_xml(self):
        """The top-level directory MUST ontain a catalog.xml file
        
        A Taxonomy Package MUST NOT include a catalog file which includes more than one rewriteURI element with the same value (after performing URI Normalization, as prescribed by the XML Catalog Specification) for the @uriStartString attribute (tpe:multipleRewriteURIsForStartString). 
        """
