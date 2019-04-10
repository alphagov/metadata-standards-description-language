

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

