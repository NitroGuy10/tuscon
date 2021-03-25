import tuscon

dictionary = {
    "variable": 123,
    "foo": "bar"
}
tuscon.generate("test.html", dictionary)

# TODO function to delete contents of the public/ folder
# TODO ability to use directories (which will be created) in path name  (e.g. "test_folder/test.html")
# TODO serve static files
