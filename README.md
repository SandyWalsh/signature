signature
=========

Signature is a simple utility for doing signature checking of Python code.

This is useful for comparing method/function signatures of mocked unit test code 
against production code. If the signatures no longer match up, you can catch
these errors early without having to resort to complicated integration tests.

For example:

Let's say we had a class that had a method with a specific signature:

```python
class Foo(object):
    def replace_me(self, a, b=1, c="hello"):
        pass
```

and another object that could take the place of Foo (like a "driver" or "plugin"
mechanism):

```python
class Blah(object):
    def real_implementation(self, a, b=1, c="hello"):
        pass
```

Everything is fine so long as the signatures for replace_me and real_implementation
are the same. Unit tests generally won't find these sorts of bugs, but Signature can.

```python
import signature
check(dict(mates=[['__main__:Foo.replace_me', '__main__:Blah.real_implementation']]),
      raise_on_error=True)
```

alternatively you can put this configuration in a JSON file and run Signature there:

```bash
 # python signature.py sample.json 
 -----Mismatch-----
 __main__:function_a ArgSpec(args=['a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 __main__:function_b ArgSpec(args=['a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 __main__:function_c ArgSpec(args=['a', 'b', 'c', 'e'], varargs=None, keywords=None, defaults=None)
 -----Mismatch-----
 __main__:Foo.method_a ArgSpec(args=['self', 'a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 __main__:Blah.method_a ArgSpec(args=['self', 'a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 __main__:Blah.method_b ArgSpec(args=['self', 'a', 'b', 'c', 'e'], varargs=None, keywords=None, defaults=None)
 -----Mismatch-----
 __main__:Foo.method_a ArgSpec(args=['self', 'a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 test_module:Blah.method_a ArgSpec(args=['self', 'a', 'b', 'c', 'd'], varargs=None, keywords=None, defaults=None)
 ./external/test_module.py|external.test_module:Blah.method_b ArgSpec(args=['self', 'a', 'b', 'c', 'e'], varargs=None, keywords=None, defaults=None)
```
