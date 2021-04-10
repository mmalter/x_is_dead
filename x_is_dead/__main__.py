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
from x_is_dead.frameworks import frameworks as fw

#Helpers

def args_with_defaults(arguments):
    if arguments["--website-list"] == None:
        t = files("x_is_dead.resources")
        arguments["--website-list"] = t.joinpath("websites")
    return arguments

def website_list_from_path(path):
    with open(path) as f:
        websites = [line for line in f]
    return websites

def is_it_dead(d, website, wait_time):
    d.get(website)
    d.implicitly_wait(wait_time)
    results = dict()
    for name, fun in fw.items():
        results[name] = fun(d)
    return results

def print_results(rs):
    frameworks_results = dict()
    for name, fun in fw.items():
        frameworks_results[name] = 0
    total = 0
    fail = 0
    for r in rs:
        website, result = r
        if result == "Failed":
            fail += 1
        else:
            for name, is_using in result.items():
                if is_using == True:
                    frameworks_results[name] += 1
        total += 1
    print(f"{total} websites got tested.")
    print(f"{fail} websites failed to load in selenium.")
    for name, use in frameworks_results.items():
        print(f"{use} websites use {name}.")

# Main

def main(arguments):
    arguments = args_with_defaults(arguments)
    websites = website_list_from_path(arguments["--website-list"])
    d = webdriver.Chrome()
    d.set_page_load_timeout(20)
    d.implicitly_wait(2)
    results = []
    for w in websites:
        try:
            r = is_it_dead(d, w, 10)
        except Exception as e:
            print("FAILED %s" % w)
            print(e)
            r = "Failed"
        results.append((w,r))
    print_results(results)

# Entry point
if __name__ == '__main__':
    arguments = docopt(__doc__, version='x_is_dead 0.1')
    sys.exit(main(arguments))
