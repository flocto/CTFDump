#!/usr/bin/env python3

from lark import Lark, Transformer
from typing import Any, List, Tuple, Self
import z3, os

BITSET = {
  'x': [0, 0, 1, 1],
  'y': [0, 1, 0, 1],
}

Rule = r"""
?start: expr -> expression

?expr: coterm -> coefterm
    | expr "+" coterm -> add
    | expr "-" coterm -> sub

?coterm: term -> term
    | integer "*" term -> mul             
    | integer -> const
              
?term: "(" term ")"
    | "~" "(" term ")" -> bnot_term
    | factor "&" factor -> band
    | factor "|" factor -> bor
    | factor "^" factor -> bxor
    | factor -> single
              
?factor: "x" -> x
    | "y" -> y
    | "~" factor -> bnot

?integer: /\d{1,8}/

%import common.WS
%ignore WS           
"""

P = Lark(Rule, parser='lalr', start='start')
PT = Lark(Rule, parser='lalr', start='term')

class MBATransformer(Transformer):
  def expression(self, args):
    return MBAExpr(args[0])

  def coefterm(self, args):
    return [args[0]]

  def add(self, args):
    return args[0] + [args[1]]

  def sub(self, args):
    new_arg = (-args[1][0], args[1][1])
    return args[0] + [new_arg]

  def term(self, args):
    return (1, args[0])

  def mul(self, args):
    num = int(args[0])
    return (num, args[1])

  def const(self, args):
    num = int(args[0])
    return (-num, BoolFunction('&', ['x', '~x'], True))
  
  def bnot_term(self, args):
    return args[0].invert()

  def band(self, args):
    return BoolFunction('&', args)

  def bor(self, args):
    return BoolFunction('|', args)

  def bxor(self, args):
    return BoolFunction('^', args)
  
  def single(self, args):
    return BoolFunction(None, args)

  def x(self, args):
    return 'x'

  def y(self, args):
    return 'y'

  def bnot(self, args):
    if args[0] == 'x' or args[0] == 'y':
      return '~' + args[0]
    assert args[0][0] == '~', "Invalid expression"
    return args[0][1]   # double negation
  
  def integer(self, args):
    return args[0]

boolean = lambda x: 1 if x else 0
def _handle_uop(op: str, a: List[int] | int) -> List[int] | int:
  if op != '~':
    raise ValueError("Invalid unary operator")
  if isinstance(a, int):
    return boolean(1 if a == 0 else 0)
  return [boolean(1 if x == 0 else 0) for x in a]

def _get_bitvec(s: str, nbits: int) -> z3.BitVec:
  return z3.BitVec(s, nbits)

def _get_bitvecval(v: int, nbits: int) -> z3.BitVecVal:
  return z3.BitVecVal(v, nbits)

class BoolFunction(object):
  def __init__(self, op: str | None, args: List[str], inverted: bool = False):
    if op is not None:
      assert len(args) == 2, "Binary operator must have two arguments"
    else:
      assert len(args) == 1, "A bool function must have at least one argument"
      if inverted and args[0] == '~':   # double neg
        inverted = False
        args = [args[0][1]]
    self.op = op
    self.args = args
    self.inverted = inverted

  def __str__(self):
    if self.op is not None:
      s = "(" + self.op.join(self.args) + ")"
    else:
      s = self.args[0]  
    
    if self.inverted:
      return f"~{s}"
    return s
  
  def __repr__(self):
    return str(self)
  
  def _get_arg_symbol(self, s: str) -> str:
    if s[0] != '~':
      return s
    return s[1]
  
  def _get_bitset(self, s: str) -> List[int]:
    if s[0] != '~':
      return BITSET[s]
    return _handle_uop('~', self._get_bitset(s[1]))
  
  def _eval_arg(self, s: str, x: int, y: int) -> int:
    bitset = {'x': x, 'y': y}
    if s[0] != '~':
      return bitset[s]
    return _handle_uop('~', bitset[s[1]])
  
  def invert(self) -> Self:
    return BoolFunction(self.op, self.args, not self.inverted)
  
  def _get_arg_z3expr(self, s: str, nbits: int) -> z3.BitVecRef:
    if s[0] != '~':
      return _get_bitvec(s, nbits)
    return ~(_get_bitvec(s[1], nbits))
  
  def to_z3expr(self, nbits: int) -> Any:
    if not self.op:
      arg_expr = self._get_arg_z3expr(self.args[0], nbits)
      if self.inverted:
        return ~arg_expr
      return arg_expr
    
    a = self._get_arg_z3expr(self.args[0], nbits)
    b = self._get_arg_z3expr(self.args[1], nbits)
    if self.op == '&':
      expr = a & b
    elif self.op == '|':
      expr = a | b
    elif self.op == '^':
      expr = a ^ b
    else:
      raise ValueError("Invalid operator")

    if self.inverted:
      return ~expr
    return expr
    
class MBAExpr(object):
  def __init__(self, coterms: List[Tuple[int, BoolFunction]]):
    self._coterms = coterms

  def __len__(self):
    return len(self._coterms)
  
  def __getitem__(self, i: int) -> Tuple[int, BoolFunction]:
    return self._coterms[i]
  
  def __setitem__(self, i: int, v: Tuple[int, BoolFunction] | BoolFunction):
    coef = self._coterms[i][0]
    if isinstance(v, BoolFunction):
      self._coterms[i] = (coef, v)
    else:
      self._coterms[i] = v

  def __str__(self):
    r = ""
    for c, t in self._coterms:
      if c < 0:
        r += f"-{abs(c)}*{t}"
      else:
        r += f"+{c}*{t}"
    return r
  
  def __repr__(self):
    return str(self)
  
  def to_z3expr(self, nbits: int) -> z3.BitVecRef:
    expr = 0
    for c, t in self._coterms:
      expr += _get_bitvecval(c, nbits) * t.to_z3expr(nbits)
    return expr
  
  @property
  def coterms(self) -> List[Tuple[int, BoolFunction]]:
    return self._coterms

T = MBATransformer()
def parse(expr: str) -> MBAExpr:
  return T.transform(P.parse(expr))

def parse_term(term: str) -> BoolFunction:
  return T.transform(PT.parse(term))

def check_expression(t: z3.Tactic, e: MBAExpr) -> bool:
  expr = e.to_z3expr(64)
  s = t.solver()
  s.add(expr != expr)

  s.set('timeout', 30000)   # 30 seconds
  r = s.check()
  if r == z3.unknown:
    print("Solver timed out")
    exit(1)
  return r == z3.unsat

def serve_challenge():
  FLAG = os.environ.get('FLAG', 'aliyunctf{this_is_a_test_flag}')

  expr = input("Please enter the expression: ")
  if len(expr) > 200:
    print("Expression is too long")
    exit(1)

  try:
    mba = parse(expr)
  except Exception as e:
    print("Could not parse the expression")
    exit(1)

  if len(mba.coterms) > 15:
    print("Too many terms")
    exit(1)

  t = z3.Then(
    z3.Tactic('mba'),
    z3.Tactic('simplify'),
    z3.Tactic('smt')
  )

  if check_expression(t, mba):
    print("It works!")
  else:
    print(f"Flag: {FLAG}")
  return 

if __name__ == '__main__':
  serve_challenge()