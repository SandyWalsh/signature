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
        if not module in sys.modules:
            if os.path.isfile(filename):
                imp.load_source(module, filename)

    if not module:
        raise Exception("Need a module path for %s" % namespace)

    if not module in sys.modules:
        __import__(module)

    klass, sep, function = klass_or_function.rpartition('.')
    if not klass:
        return getattr(sys.modules[module], function)

    klass_object = getattr(sys.modules[module], klass)
    return getattr(klass_object, function)


class DifferentSignatures(Exception):
    def __init__(self, this_code, this_sig, that_code, that_sig):
        super(DifferentSignatures, self).__init__()
        self.this_code = this_code
        self.this_sig = this_sig
        self.that_code = that_code
        self.that_sig = that_sig

    def __str__(self):
        return """
%s %s
%s %s""" % (self.this_code, self.this_sig, self.that_code, self.that_sig)


def check(config, raise_on_error=False):
    mates = config['mates']
    results = []
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
                if raise_on_error:
                    raise DifferentSignatures(mate, sig, last_mate, last_sig)
            last_mate = mate
            last_sig = sig
            sigs.append((mate, sig))
        results.append((mismatch, sigs))
    return results


#--------------------------
# Sample functions/methods for testing

class Foo(object):
    def method_a(self, a, b, c, d):
        pass


class Blah(object):
    def method_a(self, a, b, c, d):
        pass

    def method_b(self, a, b, c, e):
        pass


def function_a(a, b, c, d):
    pass


def function_b(a, b, c, d):
    pass


def function_c(a, b, c, e):
    pass

#--------------------------


if __name__ == '__main__':
    filename = 'sample.json'
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    with open(filename) as f:
        config = json.load(f)
    results = check(config)  #, raise_on_error=True)

    for mismatch, sigs in results:
        if mismatch:
           print "-----Mismatch-----"
           for mate, sig in sigs:
                print mate, sig
