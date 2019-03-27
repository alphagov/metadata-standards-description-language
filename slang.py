###############################################################################
###
### slang.py - An implementation of the Spreadsheet Description Language.
###
###  gov.uk Metadata Standards are a way to increase the interoperability of
###  spreadsheets between government departments.
###
###  slang.py implements the spreadsheet description language described in
###  https://docs.google.com/presentation/d/1eEc8s3_eNx_b5vMxWpF-BiueDfaz6mD6zbamXbSy1Z4
###
###
###  Copyright (C) 2019, Andy Bennett, Crown Copyright (Government Digital Service).
###
###  Permission is hereby granted, free of charge, to any person obtaining a
###  copy of this software and associated documentation files (the "Software"),
###  to deal in the Software without restriction, including without limitation
###  the rights to use, copy, modify, merge, publish, distribute, sublicense,
###  and or sell copies of the Software, and to permit persons to whom the
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

# language.py cannot be invoked directly. You should import it into another
# program thus:
# import slang

import sys



###############################################################################
# Internal Representation of a Spreadsheet Metadata Language description

class state:

    def __init__(self):
        True


    # declare-type Price GBPxVAT
    def declare_type(self, name, type):

        assert isinstance(name, str), ("state.declare_type: Expected name argument to be of type 'str' but e got %s." % name)
        assert isinstance(type, str), ("state.declare_type: Expected type argument to be of type 'str' but e got %s." % type)

        print("declare_type: name = %s, type = %s" % (name, type))


    # declare-header A3:D3
    def declare_header(self, range):

        assert isinstance(range, str), ("state.declare_header: Expected range argument to be of type 'str' but e got %s." % range)

        print("declare_header: range = %s" % (range))


    # declare-data A4:D8
    def declare_data(self, range):

        assert isinstance(range, str), ("state.declare_data: Expected range argument to be of type 'str' but e got %s." % range)

        print("declare_data: range = %s" % (range))


    # Internal state
    keys   = {}
    header = None
    data   = None



###############################################################################
# A spreadsheet and some metadata that might be valid for it.

class instance:

    def __init__(self, metadata, spreadsheet):

        assert isinstance(metadata,    state), ("instance.__init__: Expected metadata argument to be of type 'state' by we got %s."   % metadata)
        assert isinstance(spreadsheet, file),  ("instance.__init__: Expected spreadsheet argument to be of type 'file' by we got %s." % spreadsheet)


    # Extract the data in the spreadsheet given the metadata
    def extract(self):
        # TODO
        None



###############################################################################
# Handlers for each verb in the Spreadsheet Metadata Language

# Handler for comments in metadata files.
# Ignore them!
def comment(*args):
    None

# A list mapping verbs to procedures that expect a state object and the
# arguments specified.
handlers = {
        "declare-type"   : state.declare_type,
        "declare-header" : state.declare_header,
        "declare-data"   : state.declare_data,
        "#"              : comment,
        }



###############################################################################
# ADT for the Spreadsheet Metadata Language

class slang:

    # input is a file descriptor for the metadata
    def __init__(self, input = sys.stdin):

        assert isinstance(input, file), ("slang.__init__: Expected input argument to be of type 'file' but we got %s." % input)

        self.input = input
        self.state = None


    # Parses the metadata file that we've been given and internalises it into
    # the state object. This procedure can only be called once per slang
    # object.
    def parse(self):

        assert (self.state == None), ("slang.parse; parsing has already been done for this object!")

        self.state = state()

        line = self.input.readline()
        line_no = 1

        while line != "":
            line = line.rstrip('\n')
            original = line
            line = line.split("\t")
            if line == ['']:
                # Ignore blank lines
                line = self.input.readline()
                line_no += 1
                continue

            proc      = line[0]
            arguments = line[1:]
            arguments.reverse()
            arguments.append(self.state)
            arguments.reverse()

            assert (proc in handlers), ("slang.parse: We don't know how to handle \"%s\" on line %s." % (original, line_no))

            try:
                apply(handlers[proc], arguments)
            except:
                print("\n\nslang.parse: Error while handling \"%s\" on line %s.\n" % (original, line_no))
                raise

            line = self.input.readline()
            line_no += 1


    # Validate a spreadsheet against the metadata object
    # input is the file descriptor for a spreadsheet
    # This validates the metadata itself and then constructs an instance object
    # to return to the user.
    # The construcion of the instance object is only successful if the
    # metadata and the spreadsheet match well enough.
    # The user can call validate() multiple times with a variety of
    # spreadsheets.
    def validate(self, input):

        assert isinstance(input, file), ("slang.validate: Expected input argument to be of type 'file' but we got %s." % input)

        # TODO: Validate all the metadata itelf then pass ourselves and our spreadsheet to the instance constructor which will validate the pair together.

        return instance(self.state, input)

