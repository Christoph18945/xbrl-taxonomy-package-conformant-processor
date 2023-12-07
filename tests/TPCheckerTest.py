#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import unittest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from TPChecker import TPChecker

"""CheckerTest.py

The class contains relevant functions to test all methods in the
TPChecker.py class.
"""

class CheckerTest(unittest.TestCase):
    """Methods for testing the class Checker.py"""
    # has_zip_format()
    def test_has_zip_format(self) -> None:
        """Test has_zip_format() function."""
        self.assertTrue(TPChecker().has_zip_format("data/example_0.zip"))
        self.assertFalse(TPChecker().has_zip_format("data/no_zip_0.txt"))
        self.assertFalse(TPChecker().has_zip_format("data/no_zip_1.tar.gz"))
        self.assertFalse(TPChecker().has_zip_format("data/no_extension"))
        return None

    # has_top_level_single_dir()
    def test_has_top_level_single_dir(self) -> None:
        """Test has_top_level_single_dir function."""
        # Positive test case with a single top-level directory.
        self.assertTrue(TPChecker().has_top_level_single_dir("../input/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata.zip"))
        # Negative test case with multiple top-level directories.
        self.assertFalse(TPChecker().has_top_level_single_dir("../input/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata.zip"))
        return None

    # validate_xml()
    def test_validate_xml(self) -> None:
        """Test validate_xml function."""
        invalid_xml_path = os.path.join("data", "catalog.xml")
        invalid_xsd_path = "http://www.xbrl.org/2017/taxonomy-package-catalog.xsd"
        # Positive test case with a valid XML document.
        self.assertTrue(TPChecker().validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path))
        # Negative test case with an invalid XML document.
        self.assertFalse(TPChecker().validate_xml("http://www.xbrl.org/2016/taxonomy-package-catalog.xsd", invalid_xml_path))
        # Negative test case with an invalid XML schema.
        self.assertFalse(TPChecker().validate_xml(invalid_xsd_path, "https://github.com/FIWARE/test.Functional/blob/master/API.test/security.PDP/8.0.1/catalog.xml"))
        return None

    # has_taxonomy_package_xml()
    def test_has_taxonomy_package_xml(self) -> None:
        """Test has_taxonomy_package_xml function."""
        archive_with_tp = "../input/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata.zip"
        archive_without_tp = "../input/ALL_20221101/ALL_20221101.zip"
        # Positive test case with a taxonomyPackage.xml file.
        self.assertTrue(TPChecker().has_taxonomy_package_xml(archive_with_tp))
        # Negative test case without a taxonomyPackage.xml file.
        self.assertFalse(TPChecker().has_taxonomy_package_xml(archive_without_tp))
        return None

    # has_catalog_xml()
    def test_has_catalog_xml(self) -> None:
        """Test has_catalog_xml function."""
        # Create a temporary directory and sample ZIP archives for testing
        archive_with_catalog = "../input/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata/EBA_CRD_XBRL_3.3_Reporting_Frameworks_3.3.0.0_errata.zip"
        archive_without_catalog = "../input/ALL_20221101/ALL_20221101.zip"
        # Test has_catalog_xml function:
        # Positive test case with a catalog.xml file.
        self.assertTrue(TPChecker().has_catalog_xml(archive_with_catalog))
        # Negative test case without a catalog.xml file.
        self.assertFalse(TPChecker().has_catalog_xml(archive_without_catalog))
        return None

if __name__ == '__main__':
    unittest.main()
