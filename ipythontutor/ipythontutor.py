"""
A ipython extension that supports Jupyter cell and line magics
%ipythontutor
for visualizing code in an iframe hosted on pythontutor.com

See README.md for examples of how to use it.
"""

# pylint: disable=broad-except,bare-except

from urllib.parse import urlencode

from IPython.core.display import HTML

from IPython.core.magic import (
    Magics as CoreMagics,
    magics_class,
    cell_magic,
)


def strtobool(val):
    """
    formerly in distutils.util
    """
    val = val.strip().lower()
    if val in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    return False


####################
@magics_class
class Magics(CoreMagics):
    """
    The ipythontutor magic
    """

    counter = 0

    def newid(self):
        """
        for generating ids
        """
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
        """
        parse the line and return a dictionary
        """
        env = self.defaults.copy()
        assigns = line.split()
        for assign in assigns:
            try:
                var, value = assign.split('=')
                if var in self.defaults:
                    env[var] = value
                else:
                    print(f"ipythontutor unknown parameter >{var}< - ignored")
            except Exception as exc:
                print(f"ipythontutor - cannot understand {assign} - ignored")
                print(f"{type(exc)} - {exc}")

        # because the ratio applies on the iframe as a whole
        # there is a need to adjust the size so that width and height
        # are significant in the notebook space, not the iframe space
        try:
            env['_ratio'] = fratio = float(env['ratio'])
            try:
                env['_ptwidth'] = float(env['width']) / fratio
            except:
                pass
            try:
                env['_ptheight'] = float(env['height']) / fratio
            except:
                pass
        except Exception as exc:
            print("ipythontutor could not adjust sizes")
            print(f"{type(exc)} - {exc}")
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
        """
        The ipythontutor magic
        """
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

        frameid = self.newid()
        # the attempt of inserting a container is so that we can set
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
        html = fstyle + cstyle + container

        # ----------------linkButton------------------------
        if strtobool(env['linkButton']):
            button = f'''
                <div class="link-button">
                <button onclick="window.open('{url}', '_blank');">
                Ouvrir dans un onglet
                </button>
                </div>
            '''
            # pylint: disable=fstring-without-interpolation
            button_style = f'''
                <style>
                .link-button {{
                    display: flex;
                    justify-content: center;
                    button {{
                        border-radius: 4px;
                        padding: 5px;
                        background-color: #4CAF50;
                        color: white;
                        margin-bottom: 5px;
                    }}
                }}
                </style>
            '''
            html = button_style + button + html

        return HTML(html)


#################### make it an extension
def load_ipython_extension(ipython):
    """
    required by IPython
    """
    ipython.register_magics(Magics)


def unload_ipython_extension(_ipython):
    """
    required by IPython
    """
