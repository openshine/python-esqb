import os
import shutil

PACKAGE = "esqb"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOC_SOURCE = os.path.join('docs', 'source')
PACKAGE_DIR = os.path.join(BASE_DIR, PACKAGE)
MODULES_RST = os.path.join(BASE_DIR, DOC_SOURCE, 'modules.rst')
modules = []
no_docs = (
    '__pycache__',
)

print("sphinx-apidoc -f -o {}/{} {}/{}/".format(
    DOC_SOURCE, PACKAGE, PACKAGE, PACKAGE))
if os.path.exists(os.path.join(DOC_SOURCE, PACKAGE)):
    shutil.rmtree(os.path.join(DOC_SOURCE, PACKAGE))
os.system("sphinx-apidoc -f -o {}/{} {}/".format(
    DOC_SOURCE, PACKAGE, PACKAGE))
modules.append('{}/{}'.format(PACKAGE, PACKAGE))
with open(MODULES_RST, 'w+') as f:
    f.write("""
{}
========

.. toctree::
   :maxdepth: 6

   {}

""".format(PACKAGE, '\n   '.join(modules)))

print("Add 'modules' to index.rst toctree")
