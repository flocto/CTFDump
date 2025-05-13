%{
open Ast
%}

%token <string> IDENT
%token <int> INT
%token LET REC IN IF THEN ELSE BACKSLASH PRINT
%token TINT
%token COLONCOLON EQUAL
%token LPAREN RPAREN LBRACE RBRACE
%token ARROW
%token GT LT PLUS MINUS SLASH
%token EOF
%token DV TOT ST

%right IN
%right ARROW
%nonassoc ELSE
%left GT LT EQUAL
%left PLUS MINUS
%left SLASH

%start <expr> prog
%%

prog:
  | e = expr EOF { e }
;

expr:
  | app_expr { $1 }
  | LET r = REC? x = IDENT t = type_annot? EQUAL e1 = expr IN e2 = expr
    { Let(r <> None, x, t, e1, e2) }
  | IF e1 = expr THEN e2 = expr ELSE e3 = expr
    { If(e1, e2, e3) }
  | BACKSLASH x = IDENT ARROW e = expr 
    { Fun (x, e) }
  | e1 = expr op = binop e2 = expr 
    { BinOp(op, e1, e2) }
  | PRINT e = expr 
    { Print e}
;

app_expr:
  | simple_expr { $1 }
  | e1 = app_expr e2 = simple_expr { App(e1, e2) }
;

simple_expr:
  | x = IDENT { Var x }
  | n = INT { Int n }
  | LPAREN e = expr RPAREN { e }
;

%inline binop:
  | GT { ">" }
  | LT { "<" }
  | EQUAL { "=" }
  | PLUS { "+" }
  | MINUS { "-" }
  | SLASH { "/" }
;

type_annot:
  | COLONCOLON t = type_expr { t }
;

type_expr:
  | atomic_type { $1 }
  | t1 = type_expr ARROW eff = effect_section t2 = type_expr 
    { Arrow(t1, t2, eff) }
;

atomic_type:
  | int_type { $1 }
  | LPAREN t = type_expr RPAREN { t }
;

int_type:
  | name = IDENT COLONCOLON TINT LBRACE pred = expr RBRACE
    { TInt(name, pred) }
;

effect_section:
  | e = effect { e }
  | { Tot }  (* デフォルト値 *)
;

effect:
  | DV { Dv }
  | TOT { Tot }
  | ST { St }
;