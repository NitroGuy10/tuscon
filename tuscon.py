import json
import warnings
from bs4 import BeautifulSoup


def about():
    print("Is it tuscon time? I think it's tuscon time!\nMade by NitroGuy10\nWill this pandemic ever end??")


# Surrounds a string with two curly brackets and a space
def surround(string):
    return "{[ " + string + " ]}"


# Copies the static file to the given path
# No parsing or generation is done
def serve(static_file_name, path=""):
    pass


# Deletes the contents of the public/ folder
def empty_public_folder():
    pass


# Removes any mention of tuscon and sets up the given BeautifulSoup object for output of an HTML file
def cleanup(template):
    params_tags = template.find_all("tuscon_params")
    if len(params_tags) > 1:
        warnings.warn(
            "Multiple <tuscon_params> tags were found. Only one is necessary. The first tag occurrence will be used.")
    for params_tag in params_tags:
        params_tag.decompose()


# Replace any occurrence of the parameter name in a tag's string or attribute with the parameter value
def fill_param(template, name, value):
    surrounded_name = surround(name)
    string_matches = set()
    attribute_matches = set()

    for tag in template.find_all():
        if surrounded_name in str(tag.string):
            string_matches.add(tag)
        for attribute_value in tag.attrs.values():
            if surrounded_name in str(attribute_value):
                attribute_matches.add(tag)

    for tag in string_matches:
        tag.string.replace_with(str(tag.string).replace(surrounded_name, str(value)))
    for tag in attribute_matches:
        for key in tag.attrs.keys():
            if surrounded_name in tag[key]:
                tag[key] = tag[key].replace(surrounded_name, str(value))


# The primary function that the user will call in their code
# Handles all necessary tasks for generating finished HTML files in public/ using a given template and parameters
def generate(template_name, parameter_dict, path=""):
    with open("templates/" + template_name) as template_file:
        template = BeautifulSoup(template_file, "lxml")

        if len(template.find_all("tuscon_params")) == 0:
            raise Exception(
                "<tuscon_params> tag must be present in a template. If generation is not needed, then serve() "
                "as a static file instead.")

        parameter_names = str(template.tuscon_params.string).split(",")

        for p in range(len(parameter_names)):
            parameter_names[p] = parameter_names[p].replace(" ", "")
            if parameter_names[p] not in parameter_dict:
                raise Exception("Parameter \"" + parameter_names[p] + "\" demanded by template not found in dictionary")

        for parameter_name in parameter_names:
            fill_param(template, parameter_name, parameter_dict[parameter_name])

        cleanup(template)

        if path == "":
            path = template_name
        with open("public/" + path, "w") as output_file:
            output_file.write(template.prettify())

        # print(template.prettify())
    print("Successfully generated " + path + " using template" + template_name)
