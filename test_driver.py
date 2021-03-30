import tuscon
import json

number = 123
dictionary = {
    "variable": number,
    "less_than_32": number < 32,
    "digits": str(number),
    "sentence": ["cool", "beans", "bro"]
}
tuscon.empty_output_folder(True)
tuscon.construct("test.html", dictionary, "test.html")
tuscon.serve("style.css", "stylesheets/style.css")
