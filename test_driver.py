import tuscon

dictionary = {
    "variable": 123,
    "foo": "bar"
}
tuscon.construct("test.html", dictionary, "test.html")
tuscon.serve("style.css", "style.css")

# TODO function to delete contents of the output folder
# TODO ability to use directories (which will be created) in path name  (e.g. "test_folder/test.html")
