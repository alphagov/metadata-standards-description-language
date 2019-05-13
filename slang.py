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
import re



###############################################################################
# Internal Representations of the Spreadsheet Language Domain Objects.

cell_re = re.compile(r"([A-Z]+)([1-9][0-9]*)")

# A reference to a specific cell in a spreadsheet.
class CellReference:

    def __init__(self, spec):

        cell = cell_re.match(spec)
        assert (cell != None), ("CellReference:.__init__ Invalid cell specifier %s." % spec)

        column = cell.group(1)
        row    = cell.group(2)

        n = 0
        for c in range(len(column)):
            n = (n * 26) + (ord(column) - ord('A') + 1)

        self.column = n - 1
        self.row    = int(row) - 1

        self.cell = spec


    def __str__(self):
        return ("%s" % self.cell)



# A reference to a range of cells in a spreadsheet.
class RangeReference:

    def __init__(self, start, end):

        assert isinstance(start, CellReference), ("RangeReference.__init__: Expected start argument to be of type 'CellReference' but we got %s." % start)
        assert isinstance(end,   CellReference), ("RangeReference.__init__: Expected end argument to be of type 'CellReference' but we got %s." % end)

        self.start = start
        self.end   = end
        self.width = (end.column   - start.column) + 1
        self.height= (end.row      - start.row)    + 1


    def __str__(self):
        return ("RangeReference(%s:%s)" % (self.start, self.end))



###############################################################################
# Handlers for the Datatypes that can be declared in Spreadsheet Metadata.

# The base class for all the types.
class Type:
    None


# Any old string.
class slang_String(Type):

    def __str__(self):
        return "slang::String"


# Currency in Sterling, excluding VAT.
class slang_GBPxVAT(Type):

    def __str__(self):
        return "slang::GBPxVAT"


# Any old number.
class slang_Number(Type):

    def __str__(self):
        return "slang::Number"


# Any old formula.
class slang_Formula(Type):

    def __str__(self):
        return "slang::Formula"



###############################################################################
# Internal Representation of a Spreadsheet Metadata Language description

class state:

    def __init__(self):
        True


    # declare-type Price GBPxVAT
    def declare_type(self, name, type):

        assert isinstance(name, str),  ("state.declare_type: Expected name argument to be of type 'str' but we got %s." % name)
        assert isinstance(type, Type), ("state.declare_type: Expected type argument to be of type 'Type' but we got %s." % type)
        assert (name not in self.keys),  ("state.delatre_type: Conflicting declaration for name %s as %s. %s has already been declared as %s." % (name, type, name, self.keys[name]))

        self.keys[name] = type

        print("  declare_type: name = %s, type = %s" % (name, type))


    # declare-header A3:D3
    def declare_header(self, range):

        assert isinstance(range, RangeReference),           ("state.declare_header: Expected range argument to be of type 'RangeReference' but we got %s." % range)
        assert ((range.height == 1) or (range.width) == 1), ("state.declare_header: range argument must describe either a single row or a single column. We got %s." % range)

        self.header = range

        print("  declare_header: range = %s" % (range))


    # declare-data A4:D8
    def declare_data(self, range):

        assert isinstance(range, RangeReference), ("state.declare_data: Expected range argument to be of type 'RangeReference' but we got %s." % range)

        self.data = range

        print("  declare_data: range = %s" % (range))


    # Check that we have most of what we need to extract some data from a spreadsheet
    def validate(self):

        assert isinstance(self.keys,   dict),           ("state.validate: keys is no longer a dictionary! We got %s." % self.keys)
        assert isinstance(self.header, RangeReference), ("state.validate: Please provide a valid header reference with the 'declare_header' directive. We got %s." % self.header)
        assert isinstance(self.data,   RangeReference), ("state.validate: Please provide a valid data reference with the 'declare_data' directive. We got %s." % self.data)

        if (self.header.height == 1):
            assert (self.data.width == self.header.width),   ("state.validate: header describes a row so data must have the same number of columns. We got header = %s and data = %s." % (self.header, self.data))

        if (self.header.width == 1):
            assert (self.data.height == self.header.height), ("state.validate: header describes a column so data must have the same number of rows. We got header = %s and data = %s." % (self.header, self.data))

        return True


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
# ADT for the Spreadsheet Metadata Language

class slang:

    # input is a file descriptor for the metadata
    def __init__(self, input = sys.stdin):

        assert isinstance(input, file), ("slang.__init__: Expected input argument to be of type 'file' but we got %s." % input)

        # User supplied parameters
        self.input = input
        self.state = None

        # Internal Initialisation
        self.string_extract_re        = re.compile(r"^\"(.*)\"$")
        self.string_invalid_escape_re = re.compile(r"[^\\]\"")
        self.string_unescape_re       = re.compile(r"\\\"")
        self.cell_re                  = re.compile(r"[A-Z]+[1-9][0-9]*")
        self.range_literal_re         = re.compile(r"([A-Z]+[1-9][0-9]*):([A-Z]+[1-9][0-9]*)")
        self.range_named_re           = re.compile(r"([^!]*)!([^!]*)")


    # Unescapes TAB, BACKSLASH and the C0 and C1 Control Characters.
    def unescape(self, arg):
        # TODO
        return arg


    # Deserialises a string and returns it.
    def string(self, arg):

        # Check for " as first and last character
        string = self.string_extract_re.match(arg)
        assert (string != None), ("slang.string: Could not find delimiters for %s." % arg)
        string = string.group(1)

        # Unescape double quotes
        invalid_quotes = self.string_invalid_escape_re.match(string)
        assert (invalid_quotes == None), ("slang.string: Unescaped double quote in %s." % arg)
        string = self.string_unescape_re.sub("\"", string)

        return string


    # Built-in types
    types = {
            "String"  : slang_String,
            "GBPxVAT" : slang_GBPxVAT,
            "Number"  : slang_Number,
            "Formula" : slang_Formula,
            }


    # Deserialises something that specifies a Type and returns a String that
    # describes the type.
    def type(self, arg):
        assert (arg in self.types), ("slang.type: Unknown type %s." % arg)

        return self.types[arg]()


    # Deserialises something that specifies a single cell and returns a
    # CellReference object that describes it.
    def cell(self, arg):

        cell = self.cell_re.match(arg)
        assert (cell != None), ("slang.cell: Invalid cell specifier %s." % arg)

        return CellReference(arg)


    # Deserialises something that specifies a range of cells and returns a
    # RangeReference object that describes it.
    # TODO: support SheetN!A3:D4
    # TODO: Support escaped !s in sheet names and range name
    def range(self, arg):

        # Look for a literal range
        range = self.range_literal_re.match(arg)
        if (range != None):
            start = CellReference(range.group(1))
            end   = CellReference(range.group(2))
            return RangeReference(start, end)

        # Look for a named range
        range = self.range_named_re.match(arg)
        if (range != None):
            assert false, ("slang.range: Named Ranges are not yet supported. We got %s." % arg)

        assert false, ("slang.range: Invalid range specifier %s." % arg)


    # Deserialises anything and returns it as-is.
    def anything(self, arg):
        return arg


    # Applys the deserialisers to the arguments and, if successful, returns the
    # resulting deserialised arguments. If a deserialiser fails (i.e. throws an
    # exception), the exception passes through to the caller.
    def deserialise(self, deserialisers, arguments):
        last_deserialiser = len(deserialisers) - 1
        result = []

        for x in range(0,  len(arguments)):
            argument     = arguments[x]
            deserialiser = None

            # Variadic directives are denoted by the last deserialiser being a
            # tuple containing one deserialiser rather than a bare
            # deserialiser.
            if x > last_deserialiser:
                deserialiser = deserialisers[last_deserialiser]
                assert isinstance(deserialiser, tuple), ("slang.deserialise: expected a tuple for variadic deserialiser whilst deserialising %s but we got %s" % (argument, deserialiser))
            else:
                deserialiser = deserialisers[x]

            if (x >= last_deserialiser) and isinstance(deserialiser, tuple):
                deserialiser = deserialiser[0]

            result.append(deserialiser(self, argument))

        return result


    # Parses the metadata file that we've been given and internalises it into
    # the state object. This procedure can only be called once per slang
    # object.
    def parse(self):

        assert (self.state == None), ("slang.parse: parsing has already been done for this object!")

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

            proc      = self.unescape(line[0])
            arguments = self.deserialise(((slang.unescape,),), line[1:])

            assert (proc in handlers), ("slang.parse: We don't know how to handle \"%s\" on line %s." % (original, line_no))

            handler = handlers[proc]
            arguments = self.deserialise(handler[1:], arguments)
            arguments.reverse()
            arguments.append(self.state)
            arguments.reverse()
            try:
                apply(handler[0], arguments)
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
        assert self.state.validate(),   ("slang.validate: Could not validate metadata!") # Doesn't need an error message because slang.validate will make its own, more specific, assertions.

        return instance(self.state, input)



###############################################################################
# Handlers for each verb in the Spreadsheet Metadata Language

# Handler for comments in metadata files.
# Ignore them!
def comment(*args):
    None

# A list mapping directives to tuples that specify procedures to handle the
# directive and deserialise the arguments.
# The first item in the tuple specifies the procedure that handles the
# directive. This procedure expects a state object and the deserialised
# arguments specified.
# The subsequent items in the tuple specify procedures that will deserialise
# the arguments. The last item in the tuple may itself be a tuple. In that case
# it is a tuple of length 1 that specifies a procedure that deserialises any
# remaining arguments. This is useful for directives that can take a variable
# number of arguments.
handlers = {
        "declare-type"   : (state.declare_type,   slang.string, slang.type),
        "declare-header" : (state.declare_header, slang.range),
        "declare-data"   : (state.declare_data,   slang.range),
        "#"              : (comment,              (slang.anything,)),
        }

