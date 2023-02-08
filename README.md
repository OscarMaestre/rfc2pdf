# rfc2pdf
A small utility to convert RFCs to PDF

Use with a single file
-----------------------    

Run this:

        ./rfc2pdf.py rfc4291.txt rfc4291.pdf LiberationMono-Bold.ttf 15 20
        
The script will take rfc4291.txt and generate a PDF file named rfc4291.pdf
where the font used will be LiberationMono-Bold with a lateral margin 
of 15 and a top and bottom margin of 20. For better results is strongly 
adviced to use a monospaced font.


Bulk converting files
----------------------

Put all your RFCs in a folder (for example RFC-all) and run this:

    ./bulk_convert RFC-all PDF-Liberation-Mono LiberationMono-Bold.ttf 15 20
