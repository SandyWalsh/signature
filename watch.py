import json
import imp
import inspect
import os
import sys
import traceback


def find_code(target):
    """Import a named class, module, method or function.

    Accepts these formats:
        ".../file/path|path.to.namespace:Class.method"
        ".../file/path|path.to.namespace:function"
    """

    filename, sep, namespace= target.rpartition('|')
    module, sep, klass_or_function = namespace.rpartition(':')
    if filename:
        if os.path.isfile(filename):
            imp.load_source('signature_%s' % filename, filename)

    if not module:
        raise Exception("Need a module path for %s" % namespace)

    try:
        __import__(module)
    except ImportError, exc:
        raise Exception("Could not import %s\n%s" % (module,
                                        traceback.format_exc(exc)))

    klass, sep, function = klass_or_function.rpartition('.')
    if not klass:
        return getattr(sys.modules[module], function)

def function_a(a, b, c, d):
    pass

def function_b(a, b, c, d):
    pass

def function_c(a, b, c, e):
    pass

def check(config):
    mates = config['mates']

    for block in mates:
        last_mate = None
        last_sig = None
        sigs = []
        mismatch = False
        for mate in block:
            code = find_code(mate)
            sig = inspect.getargspec(code)
            if last_sig and sig != last_sig:
                mismatch = True
            last_mate = mate
            last_sig = sig

            sigs.append((mate, sig))

        if mismatch:
            print "-----Mismatch!-----"
            for mate, sig in sigs:
                print mate, sig


if __name__ == '__main__':
    with open('sample.json') as f:
        config = json.load(f)
    check(config)
