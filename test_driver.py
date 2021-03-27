import tuscon

number = 123
dictionary = {
    "variable": number,
    "less_than_32": number < 32,
    "digits": str(number),
    "sentence": ["cool", "beans", "bro"]
}
tuscon.construct("test.html", dictionary, "test.html")
tuscon.serve("style.css", "stylesheets/style.css")

# TODO function to delete contents of the output folder
