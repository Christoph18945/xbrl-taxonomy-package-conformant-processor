## :newspaper: About the project

A small command line program that checks whether an XBRL Taxonomy Package complies with the Standard Taxonomy Package 1.0 and adjusts it if necessary.

### How it works

1. Run for example ```app.py EDINET "full/path/to/input/archive.zip"```. The ```app.py``` file is the starting point of the application. In this case ```EDINET``` is the abbreveation of the taxonomy package provider and ```full/path/to/archive.zip``` is the path to the zip archive. Packages to test/to experiment with the application are located in the ```input```-folder.

2. The class ```Checker```-class in ```Checker.py``` analyzes the package according to the [Taxonomy Package 1.0 standard](https://www.xbrl.org/Specification/taxonomy-package/REC-2016-04-19/taxonomy-package-REC-2016-04-19.html). The result of the analyzation is printed on the commandline.

3. Based on the result calculated by the ```Checker```-class, the next step is to fix the package. ```Fixer.py``` contains the an Interface with relevant abstract methods. Each class represents a package by a specific provider. When the class is initialized, the package to fix, will be copied over to the ```output```-folder. The definied methods from the Interface are responsible for fixing the package now located in the ```output```-folder.

4. The result of the fixed package will be a fixed ```zip``` archive containing all relevant data.

### Content overview

    .
    ├── input/ - contains xbrl taxonomy packages
    ├── logs/ - folder contains logfiles produced by program
    ├── output/ - contains the fixed taxonomy packages
    ├── schemas/ - contains XML schemas to validate against
    ├── tests/ - contains tests
    ├── app.py - program entry point
    ├── Procesor.py - The conformant processor
    ├── README.md - contains project information
    ├── requirements.txt - requirements to run the project
    └── TaxonomyPackage.py - Contains code to fix specific xbrl taxonoy pacakges

## :notebook: Features

* Check and fix...
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

### Prerequisites

```{python}
pip3 install -r requirements.txt
```

### Example usage

```{python}
python3 app.py [PROVIDER] [PATH/TO/PKG]
```

```{python}
python3 app.py EDINET "input/ALL_20221101.zip"
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