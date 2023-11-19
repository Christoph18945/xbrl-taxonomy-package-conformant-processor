#!/usr/bin/python3
# -*- coding: utf-8 -*-

import argparse

def main():
    """driver code"""
    parser = argparse.ArgumentParser(description="A simple command-line tool to fix taxonomy packages.")
    
    parser.add_argument("provider", help="provider abbreveation to identify who prvodied the taxonomy package.")
    parser.add_argument("package", help="Path tot the taxonomy pacakge (ZIP file).")
    
    args = parser.parse_args()

    result = f"Arguments received: arg1={args.provider}, arg2={args.package}"
    print(result)    

if __name__ == "__main__":
    main()
