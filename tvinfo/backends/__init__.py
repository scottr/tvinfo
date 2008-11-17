""" Backends, yadaada.

Foo bar
"""

import imp
import os

# Load the backend modules
__mod_prefix = ""
__mod_suffix = ".py"
__module_search_dir = __path__ 

__modules = os.listdir(__module_search_dir[0])
_backends = {}
for m in __modules:
        fd = 0
        if m.startswith(__mod_prefix) and \
                m.endswith(__mod_suffix) and  \
                not m.startswith("__init__"):
                modname = m[:len(m)-len(__mod_suffix)]
                try:
                        (fd,path,desc) = imp.find_module(modname, __path__)
                        m = imp.load_module(modname, fd, path, desc)
                        _backends[modname[len(__mod_prefix):]] = m
                finally:
                        if isinstance(fd,file):
                                fd.close()

def get_backends():
        """ Returns a list of dictionaries describing the available backends. """
        ret = []
        for x in _backends.keys():
                b = {}
                b["name"] = _backends[x].module_name
                b["desc"] = _backends[x].module_description
                b["api"] = _backends[x].module_api_desc
                ret.append(b)
        return ret
        
def get_backend(backend):
        """ Return a named backend module. 

        Raises an Exception if the named backend module does not exist.
        """
        if backend not in _backends.keys():
                raise Exception("Unknown backend: "+ str(backend))
        return _backends[backend]



