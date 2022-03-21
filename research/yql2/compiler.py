import os
import re
import sys
from copy import deepcopy
from parsy import ParseError

from .parser import proto
from .utils import logger

################################################################################
# Engine Logic
# ============
# So this is how the compiler are supposed to work:
# 1. Parse the proto file so we get all the tokens
# 2. Parse the tokens into a tree
# 3. Walk the tree and generate the code
# 
# messages get converted to BaseModels
################################################################################

_BASE_MODEL = '''
class {% name %}(BaseModel):
{% fields %}
'''

_





################################################################################
# Compiler Method
# ===============
# Function called by the CLI and rest of the package
################################################################################

VALID_SCHEMA = ["fastapi"]


def _get_error(s: str, lno: int, col: int, e: str, margin: int = 4, fp: str = "") -> str:
    # return substring string from s for margin lines above and below
    # and error
    _lines = s.split("\n")
    sno = max(0, lno - margin)
    eno = min(len(_lines), lno + margin)
    elist = []
    for l,i in zip(_lines[sno+1:lno+1], range(sno+1, lno+1)):
        elist.append(f"{i:03d} {l}")

    # print the error shifted by coloumns
    elist.append(" "*(4+col) + "^"*len(e))
    elist.append(f" "*(4+col) + f"\033[31m{e}\033[39m")
    for l,i in zip(_lines[lno+1:eno], range(lno+1, eno)):
        elist.append(f"{i:03d} {l}")
    l0 = f"==== PARSE ERROR ({fp}) ===="
    return f"\033[31m{l0}\033[39m\n" + "\n".join(elist) + "\n" + "\033[31m" + "="*(len(l0)) + "\033[39m"


def compiler(
  f: str,
  O: str = ".",
  s: str = "fastapi",
  verbose: bool = True,
  *,
  _unittest: bool = True
):
  """Compile a proto file to FastAPI code.

  Args:
    f (str): Path to the proto file
    O (str, optional): Output folder to put. Defaults to current directory.
    s (str, optional): The schema to use. Defaults to "fastapi".
    verbose (bool, optional): Log everything
  """
  # checks
  if not os.path.isfile(f):
    raise ValueError(f"{f} is not a file")
  if s not in VALID_SCHEMA:
    raise ValueError(f"{s} is not a valid schema not one of '{VALID_SCHEMA}'")
  os.makedirs(O, exist_ok=_unittest)

  # read and parse proto
  with open(f, 'r') as _f:
    data = _f.read()
    code = re.sub(r'//.*?\n|/\*.*?\*/', '', data, flags=re.S)

  try:
    parsed_proto = proto.parse(code)    
  except ParseError as excp:
      e = str(deepcopy(excp))
      lno, col = e.split()[-1].split(":")
      error = _get_error(code, int(lno), int(col), e, fp = f)
      print(error)
      sys.exit(1)
  except Exception as excp:
      raise excp

  statements = parsed_proto.statements
  
  if verbose:
    logger.debug(f"syntax: {parsed_proto.syntax}")
    for s in statements:
      logger.debug(s)

  # we are primarily looking at services and messages