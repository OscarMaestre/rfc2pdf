#!/usr/bin/python3

from fpdf import FPDF #If this fails maybe you will want to "pip3 install fpdf"
import sys

class PDF_RFC(object):
    def __init__(self, rfc_textual_format_filename, pdf_output_filename, ttf_file, side_margins, top_margin) -> None:
        self._pdf_object=FPDF("P", "mm", "A4")
        self._pdf_object.add_font("UserDefinedMonospacedFont", "", ttf_file, uni=True)
        self._pdf_object.set_font('UserDefinedMonospacedFont', '', 12)
        top_margin=int(top_margin)
        side_margins=int(side_margins)
        if top_margin<=20:
            print("Warning, top margins<20 usually produce bad results")
        lines=self.get_textual_lines_from_rfc(rfc_textual_format_filename)
        self.set_margins_mm(int(top_margin), int(side_margins))

        self.dump_lines_to_pdf(lines)
        self._pdf_object.output(pdf_output_filename)
        

    def set_margins_mm(self, margin_top=15, margin_left=11):
        self._margin_top=margin_top
        self._margin_left=margin_left
        self._pdf_object.set_margins(self._margin_left, self._margin_top, self._margin_left)

    def get_textual_lines_from_rfc(self, rfc_textual_format_filename):
        print(rfc_textual_format_filename)
        with open(rfc_textual_format_filename, "r", encoding="iso-8859-1") as descriptor:
            lines=descriptor.readlines()
            return lines

    def dump_lines_to_pdf(self, rfc_text_lines):
        cover_page=rfc_text_lines[0:59]
        self.add_page(cover_page)
        for line_pos in range(60, len(rfc_text_lines), 56):
            self.add_page(rfc_text_lines[line_pos:line_pos+56])

    def convert_points_to_mm(self, amount_in_points):
        #1 point is 0.35277 mm
        return amount_in_points*0.35277
    def convert_mm_to_points(self, amount_in_mm):
        return amount_in_mm/0.35277

    def add_page(self, lines):
        NO_BORDER=0
        CONTINUE_IN_NEXT_LINE=1
        ALIGNMENT_LEFT="L"
        DONT_CARE_ABOUT_WIDTH=0
        A4_HEIGHT_MM=297
        self._pdf_object.add_page()
        total_lines=len(lines)
        mm_per_line=(A4_HEIGHT_MM-(2*self._margin_top)) / total_lines
        for line in lines:
            self._pdf_object.cell(DONT_CARE_ABOUT_WIDTH, mm_per_line, line.rstrip(), border=NO_BORDER, ln=CONTINUE_IN_NEXT_LINE, align=ALIGNMENT_LEFT)


HELP="""rfc2pdf.py <rfc in plain text> <PDF output filename> <TTF filename> <side margins> <top_bottom_margin>.
    
    Example:
        ./rfc2pdf.py rfc4291.txt rfc4291.pdf LiberationMono-Bold.ttf 15 25
        
        The script will take rfc4291.txt and generate a PDF file named rfc4291.pdf 
        where the font used will be LiberationMono-Bold with a lateral margin 
        of 15 and a top and bottom margin of 25. For better results is strongly 
        adviced to used a monospaced font."""
if __name__=="__main__":
    try:

        rfc_in_textual_format_filename=sys.argv[1]
        rfc_pdf_output=sys.argv[2]
        ttf_file=sys.argv[3]
        side_margins=sys.argv[4]
        top_margin=sys.argv[5]
        pdf=PDF_RFC(rfc_in_textual_format_filename, rfc_pdf_output, ttf_file, side_margins, top_margin)
    except IndexError:
        print(HELP)
