signature
=========

Signature is a simple utility for doing signature checking of Python code.

This is useful for comparing method/function signatures of mocked unit test code 
against production code. If the signatures no longer match up, you can catch
these errors early without having to resort to complicated integration tests.

For example:

Let's say we had a class that had a method with a specific signature:

class Foo(object):
    def replace_me(self, a, b=1, c="hello"):
        pass

and another object that could take the place of Foo (like a "driver" or "plugin"
mechanism):

class Blah(object):
    def real_implementation(self, a, b=1, c="hello"):
        pass

Everything is fine so long as the signatures for replace_me and real_implementation
are the same. Unit tests generally won't find these sorts of bugs, but Signature can.

import signature
check(dict(mates=[['__main__:Foo.replace_me', '__main__:Blah.real_implementation']]),
      raise_on_error=True)
