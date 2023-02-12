#!/usr/bin/python3

from fpdf import FPDF #If this fails maybe you will want to "pip3 install fpdf"
from fpdf import XPos, YPos
import sys
import re

class PDF_RFC(object):
    def __init__(self, rfc_textual_format_filename, pdf_output_filename, ttf_file, side_margins, top_margin, generate_bookmarks) -> None:
        self._pdf_object=FPDF("P", "mm", "A4")

        self.re_section_name=re.compile("^[1-9]\.")
        self.re_subsection_name=re.compile("^[1-9]\.[1-9].")
        self.re_subsubsection_name=re.compile("^[1-9]\.[1-9].[1-9]\.")

        self._pdf_object.add_font("UserDefinedMonospacedFont", "", ttf_file)
        self._pdf_object.set_font('UserDefinedMonospacedFont', '', 12)

        top_margin=int(top_margin)
        side_margins=int(side_margins)
        if top_margin<=20:
            print("Warning, top margins<20 usually produce bad results")
        lines=self.get_textual_lines_from_rfc(rfc_textual_format_filename)
        self.set_margins_mm(int(top_margin), int(side_margins))

        self.dump_lines_to_pdf(lines, generate_bookmarks)
        self._pdf_object.output(pdf_output_filename)
        
        

    def set_margins_mm(self, margin_top=15, margin_left=11):
        self._margin_top=margin_top
        self._margin_left=margin_left
        self._pdf_object.set_margins(self._margin_left, self._margin_top, self._margin_left)

    def get_textual_lines_from_rfc(self, rfc_textual_format_filename):
        #print(rfc_textual_format_filename)
        with open(rfc_textual_format_filename, "r", encoding="iso-8859-1") as descriptor:
            lines=descriptor.readlines()
            return lines

    def dump_lines_to_pdf(self, rfc_text_lines, generate_bookmarks):
        cover_page=rfc_text_lines[0:59]
        
        self.add_page(cover_page, is_cover_page=True, generate_bookmarks=generate_bookmarks)
        #self._pdf_object.Bookmark("Prueba", level=1, y=-1)
        for line_pos in range(60, len(rfc_text_lines), 56):
            self.add_page(rfc_text_lines[line_pos:line_pos+56])

    def convert_points_to_mm(self, amount_in_points):
        #1 point is 0.35277 mm
        return amount_in_points*0.35277
    def convert_mm_to_points(self, amount_in_mm):
        return amount_in_mm/0.35277


    def add_appendix_if_necessary(self, line_number, line:str):
        #Although RFCs' structure is quite uniform it's very
        #difficult to guess if a line must be considered an
        #appendix or even if it must be added to the PDF
        #bookmarks (Acknowledgments? Author's address)
        #Generally speaking, this script adds a line to 
        #the bookmarks if the first symbol of a line is not 
        #a space
        #There are too many different cases, so sometimes
        #the bookmarks will include something that perhaps
        #shouldn't be there

        
        if line_number<=3:
            #Most RFCs use the three first lines for headings
            return
        if line_number>=53:
            #Most RFCs use the last line for page numbers
            return
        first_char=line[0]
        if not first_char.isspace():
            #print("Appendix?:"+line)
            self._pdf_object.start_section(line.strip(), level=0)

    def add_section_if_necessary(self, line_number, line):
        match=self.re_subsubsection_name.match(line)
        if match!=None:
            self._pdf_object.start_section(line.strip(), level=2)
        else:
            match=self.re_subsection_name.match(line)
            if match!=None:
                self._pdf_object.start_section(line.strip(), level=1)
            else:
                match=self.re_section_name.match(line)
                if match!=None:
                    self._pdf_object.start_section(line.strip(), level=0)
                else:
                    self.add_appendix_if_necessary(line_number, line)
        
    def add_page(self, lines, is_cover_page=False, generate_bookmarks=True):
        NO_BORDER=0
        ALIGNMENT_LEFT="L"
        DONT_CARE_ABOUT_WIDTH=0
        A4_HEIGHT_MM=297
        self._pdf_object.add_page()
        
        total_lines=len(lines)
        mm_per_line=(A4_HEIGHT_MM-(2*self._margin_top)) / total_lines
        for line_number, line in enumerate(lines):
            if (not is_cover_page) and generate_bookmarks:
                self.add_section_if_necessary(line_number, line)            
            self._pdf_object.cell(DONT_CARE_ABOUT_WIDTH, mm_per_line, line.rstrip(), border=NO_BORDER, align=ALIGNMENT_LEFT, new_x=XPos.LMARGIN, new_y=YPos.NEXT)


HELP="""rfc2pdf.py <rfc in plain text> <PDF output filename> <TTF filename> <side margins> <top_bottom_margin> <generate_bookmarks (use True or False).
    
    Example:
        ./rfc2pdf.py rfc4291.txt rfc4291.pdf LiberationMono-Bold.ttf 15 25 True
        
        The script will take rfc4291.txt and generate a PDF file named rfc4291.pdf 
        where the font used will be LiberationMono-Bold with a lateral margin 
        of 15 and a top and bottom margin of 25. The script will try to generate a PDF
        with bookmarks. For better results is strongly adviced to use a monospaced font."""
if __name__=="__main__":
    try:

        rfc_in_textual_format_filename=sys.argv[1]
        rfc_pdf_output=sys.argv[2]
        ttf_file=sys.argv[3]
        side_margins=sys.argv[4]
        top_margin=sys.argv[5]
        generate_bookmarks=sys.argv[6]
        pdf=PDF_RFC(rfc_in_textual_format_filename, rfc_pdf_output, ttf_file, side_margins, top_margin, generate_bookmarks)
    except IndexError:
        print(HELP)
