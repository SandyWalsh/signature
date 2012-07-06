signature
=========

Signature is a simple utility for doing signature checking of Python code.

This is useful for comparing method/function signatures of mocked unit test code 
against production code. If the signatures no longer match up, you can catch
these errors early without having to resort to complicated integration tests.

(For more background on the problem, read my blog post here: http://www.sandywalsh.com/2011/08/pain-of-unit-tests-and-dynamically.html )

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

Signature takes a dict-based configuration file. The primary key is called ```mates```.
Mates contains a list of lists of matching methods or functions with matching signatures.

The format of a method/function signature is:
```
<path/to/python/file.py|>path.to.namespace:<ClassName.>method_or_function_name
```

For example, lets say we need to ensure ```./impl_1.py Impl1.method_a``` needs to match
```./drivers/impl2.py Impl2.method_b``` your configuration dict would look like:

```
{"mates": [['./impl1.py|Impl1.method_a', './drivers/impl2.py|Impl2.method_b']]}
```

It's a list of lists because you likely have lots of different Signature mates you
need to validate.

Other examples are:
```my_module.function_name
./extensions/foobar.py|Foobar.method_name
my_module:MyClass.my_method
my_file.py|my_module:MyClass.my_method
```

You can call Signature from existing Python code with:

```python
import signature
check(dict(mates=[['__main__:Foo.replace_me', '__main__:Blah.real_implementation']]),
      raise_on_error=True)
```

or, you can put this configuration in a JSON file and run Signature from the cmdline:

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
