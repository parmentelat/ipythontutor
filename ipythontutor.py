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

    # for generating ids
    counter = 0
    def newid(self):
        Magics.counter += 1
        return "ipythontutor{}".format(Magics.counter)
    

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
        'ratio': 1,
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
                    print("ipythontutor unknown parameter >{}< - ignored"
                          .format(var))
            except:
                print("ipythontutor - cannot understand {} - ignored".format(assign))
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
        transform = "translate(-{offset_x}px, -{offset_y}px) scale({ratio})"\
                    .format(ratio=env['ratio'], offset_x=offset_x, offset_y=offset_y)
        return (  "{{transform: {transform};}}")\
                .format(transform=transform)
        

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
        frameid = self.newid()
        # xxx the attempt of inserting a container is so that we can set
        # max-width and max-height, but in this version it's still not quite right
        # and some real estate gets lots in the mix...
        containerid = self.newid()
        fstyle = "<style>#{id} {style}</style>"\
                .format(id=frameid, style=self.ratio_style(env))
        iframe = ('<iframe id="{id}" class="pythontutor"'
                  + ' width="{_ptwidth}" height="{_ptheight}"'
                  + ' src="{url}">' )\
                  .format(id=frameid, url=url, **env)
        cstyle="<style>#{id} {{ max-width:{width}px; max-height:{height}px; box-sizing:border-box; }}</style>"\
                .format(id=containerid, **env)
        container = '<div id={id}>{iframe}</div>'\
                              .format(id=containerid, iframe=iframe)
        #print(fstyle); print(cstyle); print(container)
        return HTML(fstyle + cstyle + container)


#################### make it an extension    
def load_ipython_extension(ipython):
    ipython.register_magics(Magics)


def unload_ipython_extension(ipython):
    pass
