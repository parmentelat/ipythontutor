"""
A jupyter extension that supports cell magics pythontutor
and pythontutor2, for visualizing code in an iframe that
leverages pythontutor.com

Users have no way at this point to set width and height

Examples
---
%%pythontutor
# partage d'une liste
a = b = [1, 2, 3]
a[0] = 'boom'
---
ditto with %%pythontutor2 for using python2
---
"""
from urllib.parse import urlencode
from ipywidgets import HTML

# the actual magic
def _link_to_pythontutor(code, py=3, width=900, height=500):
    url = "http://pythontutor.com/visualize.html#"
    d = dict(code = code,
             cumulative = "false",
             curInstr = 0,
             heapPrimitives = "false",
             mode = "display",
             origin = "opt-frontend.js",
             py=py,
#             rawInputLstJSON = "[]",
             textReferences = "false"
    )
    url += urlencode(d)
    iframe = '''<iframe class="pythontutor" width="{width}" height="{height}"
                src="{url}">'''.format(**locals())
    return HTML(iframe)

def link_to_pythontutor(line, cell):
    return _link_to_pythontutor(cell, py=3)

def link_to_pythontutor2(line, cell):
    return _link_to_pythontutor(cell, py=2)

def load_ipython_extension(shell):
    shell.register_magic_function(link_to_pythontutor, 'cell', 'pythontutor')
    shell.register_magic_function(link_to_pythontutor2, 'cell', 'pythontutor2')

def unload_ipython_extension(shell):
    '''
    Unregister the  magic when the extension unloads.
    '''
    del shell.magics_manager.magics['cell']['pythontutor']
    del shell.magics_manager.magics['cell']['pythontutor2']

