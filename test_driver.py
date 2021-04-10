import tuscon
import shutil
import os

number = 123
dictionary = {
    "variable": number,
    "less_than_32": number < 32,
    "digits": str(number),
    "sentence": ["cool", "beans", "bro"]
}
if os.path.exists(tuscon.output_dir):
    shutil.rmtree(tuscon.output_dir)
tuscon.construct("test.html", dictionary, "index.html")
shutil.copyfile("static/style.css", tuscon.output_dir + "style.css")
