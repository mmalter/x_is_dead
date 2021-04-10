"""X is dead.

Usage:
  x_is_dead [--website-list=<path>] [<framework>]
  x_is_dead (-h | --help)
  x_is_dead --version

Options:
  -h --help              Show this screen.
  --version              Show version.
  --website-list=<path>  Inspect a text file containing URLs

"""

from docopt import docopt
from importlib.resources import files, as_file
import sys
from selenium import webdriver

#Helpers

def args_with_defaults(arguments):
    if arguments["--website-list"] == None:
        t = files("x_is_dead.resources")
        arguments["--website-list"] = t.joinpath("websites")
    if arguments["<framework>"] == None:
        arguments["<framework>"] = "JQuery"
    return arguments

def website_list_from_path(path):
    with open(path) as f:
        websites = [line for line in f]
    return websites

def framework_name_to_fun(name):
    if name == "JQuery":
        fun = jquery
    else:
        raise LookupError
    return fun

def is_it_dead(d, website, wait_time, framework_fun):
    d.get(website)
    d.implicitly_wait(wait_time)
    return framework_fun(d)

def format_results(rs, framework):
    fail = 0
    using = 0
    not_using = 0
    for r in rs:
        website, result = r
        if result == True:
            using += 1
        if result == False:
            not_using += 1
        if result == "Failed":
            fail += 1
    total = using + not_using
    o = f"Over {total} websites, {using} use {framework}."
    return o
    

# Check functions

def jquery(d):
    script = """
    if(!!window.jQuery)
    {
        return true;
    } else {
        return false;
    }
    """
    o = d.execute_script(script)
    d.implicitly_wait(1)
    return o

# Main

def main(arguments):
    arguments = args_with_defaults(arguments)
    websites = website_list_from_path(arguments["--website-list"])
    f = framework_name_to_fun(arguments["<framework>"])
    d = webdriver.Chrome()
    d.set_page_load_timeout(20)
    d.implicitly_wait(2)
    results = []
    for w in websites:
        try:
            r = is_it_dead(d, w, 10, f)
        except:
            r = "Failed"
        results.append((w,r))
    print(format_results(results, arguments["<framework>"]))

# Entry point
if __name__ == '__main__':
    arguments = docopt(__doc__, version='x_is_dead 0.1')
    sys.exit(main(arguments))
