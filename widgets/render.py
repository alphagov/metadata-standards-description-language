

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


print \
page({"title"   : "Submit Your Spreadsheet To Treasury",
    })

