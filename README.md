
<span style="float:left;">Licence CC BY-NC-ND</span>

# Embedding `pythontutor.com` illustrations in Jupyter  

## Installation

```
$ pip3 install ipythontutor
```

## Screeshot

As github won't render iframes embedded in a `ipynb`, here's a screenshot

![](screenshot.gif)

## Basic Usage


```python
# required to load the extension
%load_ext ipythontutor
```

In its simplest form, the code in the cell is handed over (as python3) to the excellent http://pythontutor.com/


```python
%%ipythontutor
original = reference = [1, 2]
original[0] = 'boom'
print(reference)
```

## Setting sizes


```python
%%ipythontutor height=400 width=850
def fact(n):
    return 1 if n <= 1 else n * fact(n-1)
original = [fact(3), fact(4)]
reference = original[:]
original[0] = 'boom'
print(reference)
```

## Link button to pythontutor (open in a new tab)


```python
%%ipythontutor height=400 width=850 linkButton=true
def fact(n):
    return 1 if n <= 1 else n * fact(n-1)
original = [fact(3), fact(4)]
reference = original[:]
original[0] = 'boom'
print(reference)
```

## Scaling

If your page is smaller than what pythontutor can reasonably work with, you can specify a scaling ratio.


```python
%%ipythontutor width=600 height=200 ratio=0.7
import copy
original = [1, [2, 3]]
reference = copy.deepcopy(original)
original[1][0] = 'boom'
print(reference)
```

## Using python2


```python
%%ipythontutor py=2
print "Hey"
original = [1, 2]
copy = original[:]
original[0] = 'boom'
```

## Other settings

The following list shows the settings that can be tweaked on the magic line. See also [this page about embedding pythontutor](http://pythontutor.com/pytutor-embed-demo.html) for more details on these settings:


```python
from ipythontutor import Magics
for var, default in Magics.defaults.items():
    print(f"{var:>20} - defaults to - {default:<}")
```

#### Note on `proto`

The default is to use `https` to reach `pythontutor`, as this is exepcted to work in most cases. If that's not working for you, instead of setting `proto=http` on each magic cell, you can change this globally - like any other default btw - this way:


```python
from ipythontutor import Magics
Magics.defaults['proto'] = 'http'
```

## See also

Check out another pure approach, that does not rely on pythontutor, [at the `nbtutor` project](https://github.com/lgpage/nbtutor).
