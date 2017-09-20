# oio-diag
CLI tool to diagnose an OpenIO platform

Installation
------------

Create a virtual env:
```ssh
virtualenv .
. bin/activate
```

install from source by running:
```sh
pip install -r requirements.txt
python setup.py install
```

Run
---
To use the command
```sh
diag.py
```

Add a new command
-----------------

Create  a file like in the sample.py in the sample folder
You just need to create a class with a method run that return the result.
```python
class Example(object):

      def run (self, **kwargs):
      	  return 'This is a example'
```

You also need to update the setup.cfg file and add
the path to the file ('.' separated) finish with ':' ClassName

```
[entry_point]
oio.tools =
    ...
    example = path.to.example:Example
```

Result returned
---------------

Currently there are two form of result:
 * A folder containing all the files
 * A tar of the preceding folder

If the run function return:
 * a `string` it is written to a file having the same `className`.
 * a `list` it will be written to `className0` `className1` `className2` ...
 * a `dictionary` it will be written to `className.key1` `className.key2` ...