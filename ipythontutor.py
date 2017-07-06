# -*- coding: utf-8 -*-

"""
A ipython extension that supports cell magics:
 * pythontutor, and
 * pythontutor2
for visualizing code in an iframe that leverages pythontutor.com

See README.ipynb for examples of how to use it.
"""


from urllib.parse import urlencode
from ipywidgets import HTML

from IPython.core.magic import (
    Magics,
    magics_class,
    cell_magic,
    line_magic,
)


####################
# it seems like magics can't be called with arguments...

# if not for python2, could be set_sice(*, width=None, height=None)
def set_size(width=None, height=None):
    if width:
        PythontutorMagics.width = width
    if height:
        PythontutorMagics.height = height

        
@magics_class
class PythontutorMagics(Magics):

    # tunable variables
    width = 750
    height = 350

    # the actual magic
    def _iframe_to_pythontutor(self, code, py=3, width=width, height=height):
        url = "http://pythontutor.com/iframe-embed.html#"
        d = dict(code = code,
                 cumulative = "false",
                 curInstr = 0,
                 heapPrimitives = "false",
                 mode = "display",
                 origin = "opt-frontend.js",
                 py=py,
                 # rawInputLstJSON = "[]",
                 textReferences = "false"
        )
        url += urlencode(d)
        iframe = '''<iframe class="pythontutor" width="{self.width}" height="{self.height}"
                    src="{url}">'''.format(**locals())
        return HTML(iframe)

    @cell_magic
    def pythontutor(self, line, cell):
        return self._iframe_to_pythontutor(cell, py=3)


    @cell_magic
    def pythontutor2(self, line, cell):
        return self._iframe_to_pythontutor(cell, py=2)


    # aliases just in case the naming would be confusing
    @cell_magic
    def ipythontutor(self, *args):
        return self.pythontutor(*args)
    @cell_magic
    def ipythontutor2(self, *args):
        return self.pythontutor2(*args)



#################### make it an extension    
def load_ipython_extension(ipython):
    ipython.register_magics(PythontutorMagics)


def unload_ipython_extension(ipython):
    pass
