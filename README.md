# XBRL Taxonomy Package Conformant Processor

## :newspaper: About the project

A small command line program that checks whether an XBRL Taxonomy Package complies with the [Standard Taxonomy Package 1.0](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html) and adjusts it if necessary.

### How it works

1. Run for example ```python3 app.py EDINET "full/path/to/input/archive.zip"```. The ```app.py``` file is the starting point of the application. ```EDINET``` represents the Electronic Disclosure System provided by the [JFSA](https://www.fsa.go.jp/en/). The path afterwards can be any path locating an XBRL Taxonomy Package (ZIP). In this case ```EDINET``` is the abbreveation of the taxonomy package provider and ```full/path/to/archive.zip``` is the path to the zip archive. Packages to test/to experiment with the application are located in the ```input```-folder.

2. The class ```Checker``` class in ```TPChecker.py``` analyzes the package according to the [Taxonomy Package 1.0 standard](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html). The result of the analyzation is displayed on the command line.

3. Based on the result calculated by the ```Checker```-class, the next step is to fix the package. ```TPFixer.py``` contains an Interface with relevant abstract methods. Each class represents a package by a specific provider. When the class is initialized, the package to fix will be copied over to the ```output```-folder. The definied methods from the Interface are responsible for fixing the package. The result of the fixed package will be a fixed ```zip``` archive containing all relevant data.

### Content overview

    .
    ├── .vscode/ - visual studio code settings
    ├── tests/ - code and data for tests
    ├── input/ - xbrl taxonomy packages
    ├── output/ - folder for fixed taxonomy packages
    ├── venv/ - data for virtual environemnt 
    ├── .gitignore - contains folders/files ignored by git
    ├── app.py - program entry point
    ├── LICENSE - license text
    ├── README.md - relevant information about the project
    ├── requirements.txt - requirements to run the project
    ├── TPChecker.py - check package according to the standard
    ├── TPFixer.py - Fix package according to standard
    └── TPMisc.py - module with helper functions

## :notebook: Features

* Checking and fixing:
  * xml format checking
  * case sensitivity checking (done by python)
  * archive format ceck
  * top-level directory checking and fixing
  * META-INF folder checking and fixing
  * taxonomyPackage.xml checkng and fixing
  * catalog.xml checking and fixing
  * URL resolution checking and fixing
  * Entrypoint localiazation

## :runner: Getting started

### Prerequisites and example usage

1. Activate virtual environment:

```bash
source venv/bin/activate
```

2. Install requirements:

```bash
pip3 install -r requirements.txt
```

3. Run script:

```bash
python3 app.py [PROVIDER] [PATH/TO/PKG]
```

```bash
python3 app.py EDINET "input/ALL_20221101/ALL_20221101.zip"
```

```bash
Input information:
------------------
    Provider -> EDINET
    Package  -> ..\input\ALL_20221101\ALL_20221101.zip

Analyzis results:
------------------
    DONE: Package is ZIP
    ERROR: Package has not single toplevel dir
    ERROR: Package has no META-INF folder
    ERROR: Package has no catalog.xml
    ERROR: Package has no taxonomy-package.xml

Fixing package...
    META-INF directory generated
    Top level directory generated
    Package content restructured
    catalog.xml file generated
    catalog.xml is xml file
    taxonomyPackage.xml file generated
    taxonomyPackage.xml is xml file
    Final zip generated

Output result:
--------------
    ..\output\ALL_20221101\ALL_20221101.zip is fixed!
```

## :books: Resources used to create this project

* Python
  * [Python 3.10.13 documentation](https://docs.python.org/3.10/)
  * [Built-in Functions](https://docs.python.org/3.10/library/functions.html)
  * [Python Module Index](https://docs.python.org/3.10/py-modindex.html)
* XBRL
  * [Extensible Business Reporting Language (XBRL) 2.1](https://www.xbrl.org/Specification/XBRL-2.1/REC-2003-12-31/XBRL-2.1-REC-2003-12-31+corrected-errata-2013-02-20.html)
  * [Taxonomy Packages 1.0](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html)
* Markdwon
  * [Basic syntax](https://www.markdownguide.org/basic-syntax/)
  * [Complete list of github markdown emofis](https://dev.to/nikolab/complete-list-of-github-markdown-emoji-markup-5aia)
  * [Awesome template](http://github.com/Human-Activity-Recognition/blob/main/README.md)
  * [.gitignore file](https://git-scm.com/docs/gitignore)
* Editor
  * [Visual Studio Code](https://code.visualstudio.com/)

## :bookmark: License

[GPL v3](https://www.gnu.org/licenses/gpl-3.0.txt) :copyright: 2023 Christoph Hartleb
