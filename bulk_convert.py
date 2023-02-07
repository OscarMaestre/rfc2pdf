#!/usr/bin/python3

from rfc2pdf import PDF_RFC

import glob, os, sys


def bulk_convert(rfcall_folder, results_folder, ttf_file, side_margin, top_margin):
    rfc_wildcard=os.path.join(rfcall_folder, "rfc*.txt")
    print(rfc_wildcard)
    try:
        os.mkdir(results_folder)
    except:
        pass
    rfc_file_list=glob.glob(rfc_wildcard)
    for rfc in rfc_file_list:
        pdf_filename=os.path.basename(rfc)[:-4]+".pdf"
        pdf_path=os.path.join(results_folder, pdf_filename)
        print(pdf_path)
        pdf=PDF_RFC(rfc, pdf_path, ttf_file, side_margins, top_margin)


HELP="""bulk_convert.py <rfcs directory> <directory for PDFs> <TTF filename> <side margins> <top_bottom_margin>.
    
    Example:
        ./bulk_convert RFC-all PDF-Liberation-Mono LiberationMono-Bold.ttf 15 25
        
        The script will take all RFCS in RFC-all and put PDFs in PDF-Liberation-Mono
        where the font used will be LiberationMono-Bold with a lateral margin 
        of 15 and a top and bottom margin of 25. For better results is strongly 
        adviced to used a monospaced font."""

if __name__=="__main__":
    try:
        rfc_all_folder = sys.argv[1]
        results_folder = sys.argv[2]
        ttf_file       = sys.argv[3]
        side_margins   = sys.argv[4]
        top_margin     = sys.argv[5]
        bulk_convert(rfc_all_folder, results_folder, ttf_file,
        side_margins, top_margin)
    except IndexError:
        print(HELP)