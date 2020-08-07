# -*- coding: utf-8 -*-

"""
A ipython extension that supports Jupyter cell and line magics 
%ipythontutor
for visualizing code in an iframe hosted on pythontutor.com

See README.ipynb for examples of how to use it.
"""

import copy
import webbrowser

from urllib.parse import urlencode
from distutils.util import strtobool

from ipywidgets import HTML, Button, Output

from IPython.core.magic import (
    Magics as CoreMagics,
    magics_class,
    cell_magic,
    line_magic,
)

####################
@magics_class
class Magics(CoreMagics):

    # for generating ids
    counter = 0
    def newid(self):
        Magics.counter += 1
        return f"ipythontutor{Magics.counter}"
    

    # settable attributes on the magic line
    defaults = {
        'width' : '750',
        'height' : 300,
        'proto' : 'https',
        'py' : 3,
        'verticalStack' : '',
        'curInstr' : 0,
        'cumulative' : 'false',
        'heapPrimitives' : 'false',
        'textReferences' : 'false',
        'ratio': 1,
        # view in a new tab if true
        'linkButton' : 'false',
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
                    print(f"ipythontutor unknown parameter >{var}< - ignored")
            except:
                print(f"ipythontutor - cannot understand {assign} - ignored")
        # because the ratio applies on the iframe as a whole
        # there is a need to adjust the size so that width and height
        # are significant in the notebook space, not the iframe space
        try:
            env['_ratio'] = fratio = float(env['ratio'])
            try: env['_ptwidth'] = float(env['width']) / fratio
            except: pass
            try: env['_ptheight'] = float(env['height']) / fratio
            except: pass
        except:
            print("ipythontutor could not adjust sizes")
        return env
                

    def ratio_style(self, env):
        """
        the css style to attach to the <iframe> object to 
        obtain the desired ratio
        """
        # stay safe in normal mode
        if env['ratio'] == 1:
            return ""
        # the transform allows to render a smaller iframe smaller
        # however somehow we also need to translate back to compensate
        # I have to admit I came up with this formula by looking at the output
        # but I can't really say I understood why it works
        r = env['_ratio']
        alpha = (1-r)/(2*r)
        offset_x = int(float(env['width'])*alpha)
        offset_y = int(float(env['height'])*alpha)
        transform = f"translate(-{offset_x}px, -{offset_y}px) scale({env['ratio']})"
        return f"{{transform: {transform};}}"
        

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
        
        url = f"{env['proto']}://pythontutor.com/iframe-embed.html#{request}"

        # ----------------linkButton------------------------
        if strtobool(env['linkButton']):
            button = Button(description='Ouvrir dans un onglet')
            output = Output()

            def open_in_new_tab(b):
                with output:
                    webbrowser.open_new_tab(url)

            button.on_click(open_in_new_tab)
            display(button, output)
        # ---------------------------------------------------
        
        frameid = self.newid()
        # xxx the attempt of inserting a container is so that we can set
        # max-width and max-height, but in this version it's still not quite right
        # and some real estate gets lots in the mix...
        containerid = self.newid()
        fstyle = f"<style>#{frameid} {self.ratio_style(env)}</style>"
        ptwidth, ptheight = env['_ptwidth'], env['_ptheight']
        iframe = (f'<iframe id="{frameid}" class="pythontutor"'
                  f' width="{ptwidth}" height="{ptheight}"'
                  f' src="{url}">')
        cstyle = (f"<style>#{containerid} "
                  f"{{ max-width:{env['width']}px; max-height:{env['height']}px; "
                  f"box-sizing:border-box; }}"
                  f"</style>")
        container = f'<div id={containerid}>{iframe}</div>'
        #print(fstyle); print(cstyle); print(container)
        return HTML(fstyle + cstyle + container)


#################### make it an extension    
def load_ipython_extension(ipython):
    ipython.register_magics(Magics)


def unload_ipython_extension(ipython):
    pass
