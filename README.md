# oio-diag
CLI tool to diagnose an OpenIO platform

## Installation

Create a virtual env:
```sh
virtualenv .
. bin/activate
```

install from source by running:
```sh
pip install -r requirements.txt
python setup.py install
```

## Run
Use the command to gather system information
```sh
oio-diag
```

Append an OpenIO Namespace option to collect information about its services.
The namespace must have been configured locally.
```sh
oio-diag --oio-ns OPENIO_NAMESPACE
```

## Extend
*oio-diag* can be extended with new sub-modules.
Create a Python file in a package.
You just need to create a class with a method named `run` that return the result.
```python
class Example(object):

      def run (self, **kwargs):
          return 'This is an example'
```

You also need to update the setup.cfg file and add
the path to the file ('.' separated) finish with ':' ClassName

```
[entry_point]
oio.tools =
    ...
    my_sample_output = path.to.example:Example
```

In the output, the JSON path of the output will be infered from the name of the entry point (but not from the name of its class).
That module will generate an output like this:
```json
{
...
  "my": {
    "sample": {
      "output": "This is an example"
    }
  }
}
```

If the output of the command script had been different
```python
class Example(object):

      def run (self, **kwargs):
          return ('plip', 'plop')
```

The output would hava been as follows:
```json
{
...
  "my": {
    "sample": {
      "output": [
        "plip",
        "plop"
      ]
    }
  }
}
```


## Output

Currently there are three forms of results:
 * A JSON dumped to stdout
 * A folder containing all the files, whose absolute path will be written on stdout
 * A tar of that folder, whose absolute path will be written on stdout

If the run function return:
 * a `string`, a `list`, a `tuple` or a `dict`: encoded as is as a member of the top-level JSON object (JSON output) or as a standalone JSON object dumped in a file with an exmplicit name;
 * a `oiodiag.FilePath`: only the path is stored in the JSON output, but the whole file will be copied in the target directory;
 * a `oiodiag.FileSet`: as with `oiodiag.FilePath`, but recursuvely on a directory.
