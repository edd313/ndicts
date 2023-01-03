# Description
Nested dictionary structures emerge every time there is some sort hierarchy
in the data. Trees, archives, the chapters and sections in a book, 
these are all examples where you will likely find nested loops of data.

Python does not have a built-in data type for nested mappings. 
Dictionaries can be used, however there many inconveniences and limitations.
Two above all: getting items requires to open and close several square brackets 
(eg. `d[level1][level2]...[levelN]`), 
and iterating will only access the first layer, 
so nested for loops are needed to iterate through all the values.

The `ndicts` package aims to tackle the main issues of nested dictionaries, 
exposing an interface with minimum differences from dictionaries themselves.
`NestedDict` is a `MutableMapping` at its core, 
therefore all familiar dictionary methods are available 
and the overall behaviour similar.

If you need to perform simple mathematical operations with your nested data,
use `DataDict`. In addition to allowing arithmetics, 
`DataDicts` borrow some methods that you would expect from a `pandas` `DataFrame`. 

Finally, this is a simple project for simple needs. 
Consider using `pandas` `MultiIndex` for more functionalities!

# Installation

Install `ndicts` with `pip`.

```commandline
pip install ndicts
```

# Overview

Import `NestedDict` and `DataDict`.

```pycon
>>> from ndicts import DataDict, NestedDict
```

Create a `NestedDict` from a dictionary.

```pycon
>>> book = {
...     "Book 1": {
...         "Section 1": "The Eve of the War",
...         "Section 2": "The Falling Star"
...     },
...     "Book 2": {
...         "Section 1": "Under Foot", 
...         "Section 2": {"Paragraph 1": "After eating we crept back to the scullery"}
...     }
... }
>>> nd = NestedDict(book)
```

Get items more conveniently than with standard dictionaries.

```pycon
>>> # NestedDict
>>> nd["Book 1", "Section 1"] 
'The Eve of the War'
>>> # dict
>>> book["Book 1"]["Section 2"]
'The Falling Star'
```

Iterate over a `NestedDict`.

```pycon
>>> for key in nd:
...     print(key)
('Book 1', 'Section 1')
('Book 1', 'Section 2')
('Book 2', 'Section 1')
('Book 2', 'Section 2', 'Paragraph 1')
```

# Documentation

https://edd313.github.io/ndicts/

# Licence
`ndicts` is licensed under the MIT license.



