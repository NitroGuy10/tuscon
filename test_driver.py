import tuscon
import os

dictionary = {
    "variable": 123,
    "foo": "bar"
}
tuscon.construct("test.html", dictionary, "test.html")
tuscon.serve("style.css", "stylesheets/style.css")

# TODO function to delete contents of the output folder
