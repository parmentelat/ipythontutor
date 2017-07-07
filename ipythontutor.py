# -*- coding: utf-8 -*-

"""
A ipython extension that supports cell magics:
 * pythontutor, and
 * pythontutor2
for visualizing code in an iframe that leverages pythontutor.com

See README.ipynb for examples of how to use it.
"""

import copy

from urllib.parse import urlencode
from ipywidgets import HTML

from IPython.core.magic import (
    Magics as CoreMagics,
    magics_class,
    cell_magic,
    line_magic,
)


####################
@magics_class
class Magics(CoreMagics):

    defaults = {
        'width' : '750',
        'height' : 300,
        'proto' : 'https',
        'py' : 3,
        'verticalStack' : '',
        'curInstr' : 0,
        'cumulative' : 'false',
        'heapPrimitives' : 'false',
    }
        

    def parse_line(self, line):
        env = self.defaults.copy()
        assigns = line.split()
        for assign in assigns:
            try:
                var, value = assign.split('=')
                if var in self.defaults:
                    env[var] = value
                else:
                    print("ipythontutor unknown parameter {} - ignored"
                          .format(var))
            except:
                print("ipythontutor - cannot make out {} - ignored".format(assign))
        return env
                
    @cell_magic
    def ipythontutor(self, line, cell):
        env = self.parse_line(line)
        pt_env = dict(code = cell,
                      mode = "display",
                      origin = "opt-frontend.js",
                      textReferences = "false"
        )
        for pass_through in ('py', 'curInstr', 'verticalStack', 'heapPrimitives'):
            pt_env[pass_through] = env[pass_through]

        request = urlencode(pt_env)
        url = "{proto}://pythontutor.com/iframe-embed.html#{request}"\
              .format(request=request, **env)
        iframe = '<iframe class="pythontutor" width="{width}" height="{height}"'\
                 ' src="{url}">'.format(url=url, **env)
        #print(iframe)
        return HTML(iframe)


#################### make it an extension    
def load_ipython_extension(ipython):
    ipython.register_magics(Magics)


def unload_ipython_extension(ipython):
    pass
