import json
import warnings
import re
from bs4 import BeautifulSoup


def about():
    print("Is it tuscon time? I think it's tuscon time!\nMade by NitroGuy10\nWill this pandemic ever end??")


# Surrounds a string with two curly brackets and a space
def surround(string):
    return "{{ " + string + " }}"


# Copies the static file to the given path
# No parsing or generation is done
def serve(static_file_name, path=""):
    pass


# Removes any mention of tuscon and sets up the given BeautifulSoup object for output of an HTML file
def cleanup(template):
    params_tags = template.find_all("tuscon_params")
    if len(params_tags) > 1:
        warnings.warn(
            "Multiple <tuscon_params> tags were found. Only one is necessary. The first tag occurring will be used.")
    template.tuscon_params = "delet_this"


def fill_param(template, name, value):
    occurrences1 = template.find_all(string=re.compile(surround(name)))
    occurrences2 = template.find_all(attrs=re.compile(surround(name)))  # This doesn't work
    print(occurrences1)
    print(occurrences2)
    # TODO implement this


# The primary function that the user will call in their code
# Handles all necessary tasks for generating finished HTML files in public/ using a given template and parameters
def generate(template_name, parameter_values, path=""):
    with open("templates/" + template_name) as file:
        template = BeautifulSoup(file, "lxml")

        if len(template.find_all("tuscon_params")) == 0:
            raise Exception(
                "<tuscon_params> tag must be present in a template. If generation is not needed, then serve() "
                "as a static file instead.")

        parameter_names = str(template.tuscon_params.string).split(",")
        if len(parameter_names) > len(parameter_values):
            raise Exception("More parameters are demanded by template than are supplied in function call.")

        for parameter_number in range(len(parameter_names)):
            fill_param(template, parameter_names[parameter_number].replace(" ", ""), parameter_values[parameter_number])

        cleanup(template)
        # print(template.prettify())
        print("Generation complete!")

