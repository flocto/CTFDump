{
open Parser
exception Error of string
}

let space = [' ' '\t' '\n' '\r']
let digit = ['0'-'9']
let lower = ['a'-'z']
let upper = ['A'-'Z']
let alpha = lower | upper
let ident = (lower | upper) (alpha | digit | '_')*

rule token = parse
  | space+      { token lexbuf }
  | "let"       { LET }
  | "rec"       { REC }
  | "in"        { IN }
  | "if"        { IF }
  | "then"      { THEN }
  | "else"      { ELSE }
  | "print"     { PRINT }
  | "Integer"   { TINT }
  | "Dv"        { DV }
  | "Tot"       { TOT }
  | "St"        { ST }
  | "::"        { COLONCOLON }
  | "="         { EQUAL }
  | "("         { LPAREN }
  | ")"         { RPAREN }
  | "{"         { LBRACE }
  | "}"         { RBRACE }
  | "->"        { ARROW }
  | ">"         { GT }
  | "<"         { LT }
  | "+"         { PLUS }
  | "-"         { MINUS }
  | "/"         { SLASH }
  | "\\"        { BACKSLASH }
  | ident as id { IDENT id }
  | digit+ as n { INT (int_of_string n) }
  | eof         { EOF }
  | _          { raise (Error ("Unexpected char: " ^ Lexing.lexeme lexbuf)) }
