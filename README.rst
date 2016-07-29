===========================
UFL - Unified Form Language
===========================

The Unified Form Language (UFL) is a domain specific language for
declaration of finite element discretizations of variational
forms. More precisely, it defines a flexible interface for choosing
finite element spaces and defining expressions for weak forms in a
notation close to mathematical notation.

UFL is described in the paper:

Alnæs, M. S., Logg A., Ølgaard, K. B., Rognes, M. E. and Wells,
G. N. (2014).  Unified Form Language: A domain-specific language for
weak formulations of partial differential equations.  *ACM
Transactions on Mathematical Software* 40(2), Article 9, 37 pages.
<http://dx.doi.org/doi:10.1145/2566630>,
<http://arxiv.org/abs/1211.4047>


Documentation
=============

The UFL documentation can be views at
http://fenics-ufl.readthedocs.org/.

.. image:: https://readthedocs.org/projects/fenics-ufl/badge/?version=latest
   :target: http://fenics.readthedocs.io/projects/ufl/en/latest/?badge=latest
   :alt: Documentation Status


Authors
=======

Authors:
  | Martin Sandve Alnæs   <martinal@simula.no>
  | Anders Logg           <logg@chalmers.se>

Contributors:
  | Kristian B. Ølgaard   <k.b.oelgaard@gmail.com>
  | Garth N. Wells        <gnw20@cam.ac.uk>
  | Marie E. Rognes       <meg@simula.no>
  | Kent-Andre Mardal     <kent-and@simula.no>
  | Johan Hake            <hake@simula.no>
  | David Ham             <david.ham@imperial.ac.uk>
  | Florian Rathgeber     <f.rathgeber10@imperial.ac.uk>
  | Andrew McRae          <a.mcrae12@imperial.ac.uk>
  | Lawrence Mitchell     <lawrence.mitchell@imperial.ac.uk>
  | Johannes Ring         <johannr@simula.no>



Installation
============

Linux::

  sudo python setup.py install


Directories
===========

- ufl/

  All source code for the UFL implementation.

- scripts/

  Commandline utilities like "ufl-analyse", "ufl-convert" and "form2ufl".

- demo/

  Several ufl form files which demonstrates the use of the form language.

- doc/

  The UFL documentation resides here. See doc/sphinx/README for how to
  generate the documentation.

- test/

  Unit tests for the UFL implementation. Run all tests by typing
  "python test.py" inside the test/ directory.


Utilities
=========

For more information about the utilities, type::

  ufl-analyse -h
  ufl-convert -h
  form2ufl -h

after installation.


About the Python modules
========================

The global namespace of the module ufl contains the entire UFL
language::

  from ufl import *

Form compilers may want to import additional implementation details
like::

  from ufl.classes import *

and::

  from ufl.algorithms import *

Importing a .ufl file can be done easily from Python::

  from ufl.algorithms import load_ufl_file
  filedata = load_ufl_file("filename.ufl")
  forms = filedata.forms
  elements = filedata.elements

to get lists of forms and elements from the .ufl file, or::

  from ufl.algorithms import load_forms
  forms = load_forms("filename.ufl")

to get a list of forms in the .ufl file.


Contact
=======

Send feature requests and questions to

  fenics-dev@googlegroups.com

The Git source repository for UFL is located at

  https://bitbucket.org/fenics-project/ufl

and bugs can be registered at

  https://bitbucket.org/fenics-project/ufl/issues


License
=======

UFL is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

UFL is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License
along with UFL. If not, see <http://www.gnu.org/licenses/>.