###############################################################################
###
### poc.py - A test harness that demonstrates the proof-of-concept.
###
###  gov.uk Metadata Standards are a way to increase the interoperability of
###  spreadsheets between government departments.
###
###  poc.py implements the proof-of-concept proposal described in
###  https://docs.google.com/presentation/d/1eEc8s3_eNx_b5vMxWpF-BiueDfaz6mD6zbamXbSy1Z4
###
###
###  Copyright (C) 2019, Andy Bennett, Crown Copyright (Government Digital Service).
###
###  Permission is hereby granted, free of charge, to any person obtaining a
###  copy of this software and associated documentation files (the "Software"),
###  to deal in the Software without restriction, including without limitation
###  the rights to use, copy, modify, merge, publish, distribute, sublicense,
###  and#or sell copies of the Software, and to permit persons to whom the
###  Software is furnished to do so, subject to the following conditions:
###
###  The above copyright notice and this permission notice shall be included in
###  all copies or substantial portions of the Software.
###
###  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
###  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
###  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
###  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
###  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
###  FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
###  DEALINGS IN THE SOFTWARE.
###
### Andy Bennett <andyjpb@digital.cabinet-office.gov.uk>, 2019/03/19
###
###############################################################################


import slang

################################################################################
# Configuration

METADATA     = "cols.slang"
SPREADSHEETS = ["office-supplies-order.ods", "office-supplies-order.ods"]



################################################################################
# JSON rendering logic

def render_value(cell):
    if isinstance(cell.type, slang.slang_String):
        return ("\"%s\"" % cell.value())
    else:
        return cell.value()

# Mutate the result object to affect what's returned from extract().
# Row is an array of CellValues
def render_json(result, row):
    print("  {")
    for c in row:
        print("    \"%s\":\t%s," % (c.name, render_value(c)))
    print("  },")

    return True



################################################################################
# Main program logic

print("Reading metadata from %s..." % METADATA)
metadata = slang.slang(open(METADATA))
metadata.parse()


for sheet in SPREADSHEETS:

    print("Validating spreadsheet %s against metadata..." % sheet)
    instance = metadata.validate(open(sheet))

    print("Extracting typed data from spreadsheet...")
    print("[")
    instance.extract(render_json)
    print("]")

