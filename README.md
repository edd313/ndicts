# Description
Nested dictionary structures emerge every time there is some sort hierarchy in the data. 
Trees, archives, the chapters and sections in a book, these are all examples where you will likely find nested loops of data.

Python does not have a built-in data type for nested mappings. Dictionaries can be used, however there many inconveniences and limitations.
Two above all: getting items requires to open and close several square brackets (eg. `di[level1][level2]...[levelN]`), and iterating will only access the first layer, so nested for loops are needed to iterate through all the values.

The ndicts package aims to tackle the main issues of nested dictionaries, exposing an interface with minimum differences from dictionaries themselves.
NestedDict is a MutableMapping at its core, therefore all familiar dictionary methods are available and the overall behaviour similar.

If you need to perform simple mathematical operations with your nested data, use DataDict. 
In addition to allowing arithmetics, DataDicts borrow some methods that you would expect from a pandas DataFrame. 

Finally, this is a simple project for simple needs. Consider MultiIndex pandas DataFrames for more functionality!

# Installation

Ndicts is on PyPi, so you can use `pip` to install it

```bash
pip install ndicts
```

# Examples
Import NestedDict and DataDict in your script:

```bash
from ndicts.ndicts import DataDict, NestedDict
```

Create a NestedDict from a dictionary:

```bash
book = {
	"Book 1": {
		"Section 1": "The Eve of the War",
		"Section 2": "The Falling Star"
	},
	"Book 2": {
		"Section 1": "Under Foot", 
		"Section 2": {"Paragraph 1": "After eating we crept back to the scullery"}
	}
}

nd = NestedDict(book)
```

Get an item (NestedDict vs dictionary): 

```bash
# NestedDict
nd["Book 2", "Section 2"] 

# dictionary
book["Book 2"]["Section 2"]
```

Other ways to initialize:

```bash
# Add items to an empty NestedDict
nd = NestedDict()
nd["a", "a"] = None
nd["a", "b"] = None

# From cartesian product
nd = NestedDict.from_product("a", "ab")

# From tuples
nd = NestedDict.from_tuples(("a", "a"), ("a", "b"))
```

Iterate:
```bash
# over keys
for key in nd:
	...
	
for key in nd.keys():
	...
	
# over values
for value in nd.values():
	...

# over key, value pairs
for key, value in nd.items():
	...
```

See the tutorials folder for a complete guide.

# Licence
Ndicts is licensed under the MIT license.



