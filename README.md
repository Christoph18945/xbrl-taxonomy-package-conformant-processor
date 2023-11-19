## :newspaper: About the project

A small command line program that checks whether an XBRL Taxonomy Package complies with the Standard Taxonomy Package 1.0 and adjusts it if necessary.

### How it works

How it works is very simple: By calling the ```app.py``` file the provider abbreveation and the path to the ZIP archive must be passed do it. There are test packages located in the ```test``` folder, but the location of the package does not matter, as long as a path is accesible. The ```Processor.py``` class checks and fixes the package, and moves the fixed result over to the ```output``` folder.

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
    * xml format check
    * case sensitivity check
    * archive format ceck
    * top-level directory check
    * META-INF folder
    * taxonomyPackage.xml check
    * catalog.xml check
    * URL resolution check
    * Entrypoint localiazation

## :runner: Getting started

### Prerequisites

```py
pip3 install -r requirements.txt
```

### Example usage

```py
python3 app.py [PROVIDER] [PATH/TO/PKG]
```

```py
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