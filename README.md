# tuscon

> *too-skawn*

Dead-simple web-templating intended for static site generation.

HTML files with parameters, if statements, and for loops.

Written in Python 3 using [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/).

---

## How to Install
```commandline
# Clone the repository
git clone https://github.com/NitroGuy10/tuscon

# You only need tuscon.py and requirements.txt in order to use tuscon
# But there are some example files in the repo to help you get started

# Create a virtual environment
python3 -m venv venv

# Install the requirements
pip3 install -r requirements.txt
```

---

## How to Use

### Templates

Somewhere in your HTML file (probably at the top) will be your tuscon_params tag.
This is where you define your parameter names.
```html
<tuscon_params>variable, less_than_32, digits, sentence</tuscon_params>
```

Now you can use those parameter names in your HTML surrounded by curly brackets, square brackets, and a space;
these parameter names will be filled in later by your script.
You can use parameters in attributes or "strings" (i.e. the text inside a tag).
```html
<h1 title="{[ variable ]}">Test Template!</h1>
<p>I think {[ variable ]} is a very cool value.</p>
```

The tuscon_if attribute serves as an if-statement.
If the parameter == false, then the tag and all its descendants will be removed.
```html
<p tuscon_if="less_than_32">That's so few, I can count it on one hand!</p>
```

The tuscon_for attribute will create an instance of that tag for every item of its parameter.
It follows syntax similar to your typical for-each loop.
The for-variable will become canonical to a tag's descendants.
```html
<!-- tuscon_for="[for-variable name] in [parameter]-->

<ul>
    <li tuscon_for="digit in digits" title="{[ digit ]}">{[ digit ]}</li>
</ul>

<!-- Demonstration of cannon -->

<li tuscon_for="word in sentence" title="{[ word ]}">
    <p>{[ word ]}</p>
    <ul>
        <li tuscon_for="letter in word" title="{[ letter ]}">{[ letter ]}</li>
    </ul>
</li>
```

Place your HTML template in the *tuscon.templates_dir* directory (which can and should be changed).

### Scripts
Create a Python 3 module and import tuscon.
```python
import tuscon

# These other libraries will be useful in using tuscon effectively
import os
import shutil
```

Change the output or templates directory if you feel like it.
```python
tuscon.output_dir = "docs/"
tuscon.templates_dir = "html/"
```

Create a dictionary containing the parameters to be used with your template.
```python
number = 123
dictionary = {
    "variable": number,
    "less_than_32": number < 32,
    "digits": str(number),
    "sentence": ["cool", "beans", "bro"]
}
```

Usually you would want to clear the output directory before regenerating it.
```python
if os.path.exists(tuscon.output_dir):
    shutil.rmtree(tuscon.output_dir)
```

Finally, construct your final HTML files with the tuscon.construct() function.
```python
# tuscon.construct(
#   template path (within templates directory),
#   dictionary of parameters,
#   output file path (within output directory))

tuscon.construct("test.html", dictionary, "index.html")
```

Run it!

```commandline
python3 <your_module_name>.py
```

Your newly-constructed HTML file will be eagerly awaiting in you in the output directory.

---

Data **T**o **S**tatic **CON**tent
