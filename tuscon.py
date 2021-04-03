"""It's tuscon time!

Construct webpages using HTML with parameters, if statements, and for loops.

Intended for static site generation.

Made by NitroGuy10"""
import copy
import warnings
import os
import shutil
from bs4 import BeautifulSoup


output_dir = "public/"
"""The directory in which filled templates will be created and static files will be copied.

The contents of this folder should represent the root of your site."""

static_dir = "static/"
"""The directory from which unchanging static files will be copied into the output directory.

This is where your CSS files, JavaScript files, unchanging HTML pages, images, and other media would go."""

templates_dir = "templates/"
"""The directory where your HTML templates will go."""


def about():
    """Prints out an extremely useful and astonishingly well-written summary of what tuscon is."""
    print("Is it tuscon time? I think it's tuscon time!\nMade by NitroGuy10\nWill this pandemic ever end??")


def surround(string):
    """Surrounds a string with curly brackets, square brackets, and a space.

    :param string: String to be surrounded
    :type string: str
    :return: Surrounded string
    :rtype: str"""
    return "{[ " + string + " ]}"


def check_path(path, make_dirs=False):
    """Normalizes the given path name.

    :param path: Path string to be checked
    :type path: str
    :param make_dirs: Whether or not to create the directories that constitute the path if they do not exist
    :type make_dirs: bool
    :return: The normalized path name
    :rtype: str
    :raises Exception: If it thinks files will be created outside of the output directory"""
    path = os.path.normpath(path).replace("\\", "/")
    if make_dirs:
        if path[:7] != output_dir:
            raise Exception(path + " does not appear to be in the " + output_dir +
                            " directory. Creating files outside the " + output_dir +
                            " directory probably isn't a good idea.")
        os.makedirs(os.path.dirname(path), exist_ok=True)
    return path


def serve(name, path):
    """Copies the static file to the given path.

    No parsing or generation is done.
    Certain file metadata is not preserved; if you want that metadata then copy it yourself lol.

    :param name: Path and name of the static file
    :type name: str
    :param path: Path and name of the new copy
    :type path: str"""
    name = check_path(static_dir + name)
    path = check_path(output_dir + path, True)
    shutil.copyfile(name, path)
    print("Successfully served " + path + " from source " + name)


def empty_output_folder():
    """Deletes the contents of the output folder.

    Friendly reminder to be absolutely certain you won't delete anything important by calling this function."""
    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)
        print("Output directory cleared!!!")
    else:
        print("Output directory doesn't exist. It will be created now.")
    os.makedirs(output_dir)


def cleanup(template):
    """Removes any mention of tuscon and sets up the given BeautifulSoup object for output of an HTML file.

    :param template: Template from which any mention of tuscon will be removed
    :type template: BeautifulSoup"""
    params_tags = template.find_all("tuscon_params")
    if len(params_tags) > 1:
        warnings.warn(
            "Multiple <tuscon_params> tags were found. Only one is necessary. The first tag occurrence will be used.")
    for params_tag in params_tags:
        params_tag.decompose()
    for temp_div in template.find_all(tuscon_temp_div=True):
        temp_div.unwrap()


def do_if(tag, dictionary):
    """Removes a tag if its condition is False.

    :param tag: Tag to be evaluated
    :type tag: BeautifulSoup
    :param dictionary: Canonical dictionary of parameters
    :type dictionary: dict
    :return: Whether or not the tag was deleted
    :rtype: bool"""
    if tag.get("tuscon_if"):
        if not dictionary[tag["tuscon_if"]]:
            tag.decompose()
            return True
        else:
            del tag["tuscon_if"]


def do_for(tag, dictionary, template):
    """For-each functionality.

    Creates on instance of the tag for each item of a certain variable.
    The for-variable name will become canonical to any statements inside the tag and its descendants.
    Returns True if for-each operations were done (which is also an indicator that the tag parse()'d itself).

    :param tag: Tag to be evaluated
    :type tag: BeautifulSoup
    :param dictionary: Canonical dictionary of parameters
    :type dictionary: dict
    :param template: Original template to whom the tag belongs
    :type template: BeautifulSoup"""
    if tag.get("tuscon_for"):
        for_var = tag["tuscon_for"].split(" in ")[0]
        for_in = tag["tuscon_for"].split(" in ")[1]
        del tag["tuscon_for"]

        temp_div = template.new_tag("div", tuscon_temp_div="")
        tag.insert_after(temp_div)
        for item in dictionary[for_in]:
            new_element = copy.copy(tag)

            canonical_dictionary = copy.copy(dictionary)
            canonical_dictionary[for_var] = item
            parse(new_element, canonical_dictionary, template)
            parse_children(new_element, canonical_dictionary, template)

            temp_div.append(new_element)

        tag.decompose()


def fill_param(tag, name, value):
    """Replace any occurrence of the {[ parameter name ]} in a tag's string or attribute with the parameter value.

    :param tag: Tag whose parameter occurrences will be filled
    :type tag: BeautifulSoup
    :param name: Name of the parameter
    :type name: str
    :param value: Value of the parameter"""
    surrounded_name = surround(name)
    if tag.string:
        tag.string.replace_with(str(tag.string).replace(surrounded_name, str(value)))
    if tag.attrs:
        for key in tag.attrs.keys():
            if surrounded_name in tag[key]:
                tag[key] = tag[key].replace(surrounded_name, str(value))


def fill_all_params(tag, dictionary):
    """fill_param() for every item in a dictionary.

    :param tag: Tag whose parameter occurrences will be filled
    :type tag: BeautifulSoup
    :param dictionary: Canonical dictionary of parameters
    :type dictionary: dict"""
    for name in dictionary.keys():
        fill_param(tag, name, dictionary[name])


def parse(tag, dictionary, template):
    """do_if(), do_for(), and fill_all_params() on the tag.

    :param tag: Tag to be parsed
    :type tag: BeautifulSoup
    :param dictionary: Canonical dictionary of parameters
    :type dictionary: dict
    :param template: Original template to whom the tag belongs
    :type template: BeautifulSoup"""
    if not do_if(tag, dictionary):  # If the tag was not deleted
        if not do_for(tag, dictionary, template):  # If the tag did not already parse itself
            fill_all_params(tag, dictionary)


def parse_children(tag, dictionary, template):
    """parse() and parse_children() for all of a tag's children.

    This function is called recursively for nearly all tags a template.

    :param tag: Tag whose children will be parsed recursively
    :type tag: BeautifulSoup
    :param dictionary: Canonical parameter dictionary for this point in the HTML structure
    :type dictionary: dict
    :param template: Original template to whom the tag belongs
    :type template: BeautifulSoup"""
    for child in tag.contents:
        if str(type(child)) == "<class 'bs4.element.Tag'>":  # There's probably a better way to do this
            parse(child, dictionary, template)
            parse_children(child, dictionary, template)


def construct(template_name, parameter_dict, path=""):
    """Construct an HTML file using a given template and parameters.

    Handles all necessary tasks for generating finished HTML files in output directory.
    Likely the tuscon function that the user will call most often in their code.

    :param template_name: Path and name of the template file
    :type template_name: str
    :param parameter_dict: Dictionary of parameters and their values which will be used for filling the template
    :type parameter_dict: dict
    :param path: Path and name of the newly constructed HTML file (If path == "", no file is output)
    :type path: str
    :return: Final HTML string that would go into the newly constructed HTML file
    :rtype: str
    :raises Exception: If tuscon_params HTML tag is absent in template or if a parameter demanded by tuscon_params is
    not found in dictionary"""
    template_name = check_path(templates_dir + template_name)
    final_html = ""
    if path != "":
        path = check_path(output_dir + path, True)
    with open(template_name) as template_file:
        template = BeautifulSoup(template_file, "lxml")

        if len(template.find_all("tuscon_params")) == 0:
            raise Exception(
                "<tuscon_params> tag must be present in a template. If generation is not needed, then serve() "
                "as a static file instead.")

        parameter_names = str(template.tuscon_params.string).split(",")

        # Remove spaces from parameter names and ensure they all exist within the dictionary
        for p in range(len(parameter_names)):
            parameter_names[p] = parameter_names[p].replace(" ", "")
            if parameter_names[p] not in parameter_dict:
                raise Exception("Parameter \"" + parameter_names[p] + "\" demanded by template not found in dictionary")

        parse_children(template, parameter_dict, template)

        cleanup(template)
        final_html = template.prettify()

        if path != "":
            with open(path, "w") as output_file:
                output_file.write(final_html)

    print("Successfully generated " + path + " using template " + template_name)
    return final_html
