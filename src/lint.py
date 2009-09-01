#! /usr/bin/env python
"""
Runs pylint on all python scripts found in a directory tree.
"""

import os
import re
import sys

# these directories are largely machine generated and tend to skew results
EXCLUDE_DIRS = ['migrations', 'evolutions', 'conf', 'configs']
MINIMUM_SCORE = 6.75
DEFAULT_FLAGS = {
    '--include-ids': 'yes',
    '--no-docstring-rgx': '__.*__\|get_absolute_url',
    '--good-names': 'i,j,k,v,qs,urlpatterns,register',
    '--generated-members': 'objects,DoesNotExist,id,pk'
}

def lint(module):
    """
    Runs ``pylint`` on the specified module and returns its rating.
    """
    
    # build-up flags for specific module
    flags = {}
    flags.update(DEFAULT_FLAGS)
    if 'urls' in module:
        # disable wildcard import errors
        flags['--disable-msg'] = 'W0614,W0401'
    elif module.endswith('admin.py'):
        # admin.ModelAdmin has 37 public methods
        flags['--max-public-methods'] = '40'
    elif 'tests' in module:
        # test classes tend to get lots of methods
        flags['--max-public-methods'] = '40'
        flags['--good-names'] += ',setUp,tearDown,r,c'
    flags_string = ''
    for key, value in flags.items():
        flags_string += '%s=%s ' % (key, value)

    # run pylint
    cmd = 'pylint %s %s'% (flags_string, module)
    pout = os.popen(cmd, 'r')
    for line in pout:
        if re.match(r'^\*{13} Module', line):
            print '\n', line[:-1] # remove newline
        if re.match(r'[C|R|W|E|F]....:.', line):
            print line[:-1] # remove newline
        if "Your code has been rated at" in line:
            print line[:-1]
            score = re.findall("-?\d{1,2}.\d\d", line)[0]
            return float(score)

    return None


def run(file_or_dir):
    """
    Calculates average ``pylint`` rating for a Python module.
    
    Takes one argument which should be the file path to a Python module
    (directory or single file).
    """
    total = 0
    file_count = 0
    if os.path.isdir(file_or_dir):
        # find all .py files within the directory
        for root, dirs, files in os.walk(file_or_dir):
            for directory in dirs:
                if directory in EXCLUDE_DIRS:
                    dirs.remove(directory) 
            for name in files:
                filepath = os.path.join(root, name)
                if filepath.endswith(".py"):
                    run_total = lint(filepath)
                    # pylint does not always return a numeric value
                    if isinstance(run_total, float):
                        total += run_total
                        file_count += 1
    elif file_or_dir.endswith(".py"):
        total = lint(file_or_dir)
        file_count = 1
    
    else:
        sys.exit("%s does not exist or is not a Python source" % file_or_dir)
            
    print "==" * 50
    print "%d modules found"% file_count
    average = total / file_count
    print "AVERAGE SCORE = %.02f"% average
    if average < MINIMUM_SCORE:
        # return error if rating is too low
        sys.exit(1)
    

if __name__ == "__main__":
    try:   
        run(sys.argv[1])
    except IndexError:
        print "no directory specified, defaulting to current working directory"
        run(os.getcwd())
    