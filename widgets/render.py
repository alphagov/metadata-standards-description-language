
# TODO:
#   + Write Javascript to detect when a rectangular range is selected in the spreadsheet
#       It should be able to recognise single cells, single lines, single
#       columns and rectangular areas where all the cells are selected.
#   + Translate a valid spreadsheet range into a excel style range specifier.
#   + Put the Excel range specifier in the title of the radio buttons.
#       Including correctly calculating the number of rows / columns in parentheses.
#   + Substitute the spreadsheet widgets for one that takes a filename and loads the table from that ODS file.
#       Must return a properly escaped bit of HTML.
#   + When the "Save and continue" button is pressed, add a dummy "declare-range <RANGE> <SELECTED RADIO ITEM>" line to a textarea underneath the button
#   + Extend the "Save and continue" logic to be able to change the "Select the area that contains your spending data" prompt, clear the spreadsheet and radio button selections, and walk the user thru
#       + Selecting the headings (individual cells only) and adding an appropraite "declare-type" directive to the textarea.
#       + Selecting the data area and adding an adding an appropraite "declare-data" directive to the textarea.
#       + Selecting the header area (single columns or single rows only) and adding an appropriate "declare-header" directive to the textarea. Alternatively, remember the locations of the declare-type cells and deduce an appropraite range (must be contiguous tho').

def read_widget(filename):
    widget = open(filename, "r")
    return widget.read()

def render(widget, dictionary):
    return widget % dictionary

def load_widget(filename):
    widget = read_widget(filename)
    return lambda d : render(widget, d)

def cat(*args):
    return "".join(args)

def contents_only(widget):
    return lambda c : widget({"contents": c})


page                 = load_widget("page.html")
two_thirds_one_third = load_widget("two-thirds-one-third.html")
button               = contents_only(load_widget("button.html"))
spreadsheet          = load_widget("spreadsheet.html")
heading_l            = contents_only(load_widget("heading-l.html"))
heading_s            = contents_only(load_widget("heading-s.html"))
radio_buttons        = contents_only(load_widget("radio-buttons.html"))
radio_item           = contents_only(load_widget("radio-item.html"))


print \
page({"title"   : "Submit Your Spreadsheet To Treasury",
    "contents": two_thirds_one_third ({
        "heading"       : "Submit Your Spreadsheet To Treasury",
        "first_column"  : cat(
            heading_s("Select the area that contains your spending data"),
            spreadsheet({}),
            button("Save and continue")),
        "second_column" : cat(
            radio_buttons(cat(
                radio_item("Number"),
                radio_item("Number Of Laptops"),
                radio_item("Currency"),
                radio_item("GBP ex. VAT"),
                radio_item("GBP inc. VAT"),
                radio_item("Product Code"),
                radio_item("Text")
                )))
        })
    })

