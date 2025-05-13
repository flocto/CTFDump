open Ast

let string_of_effect = function
  | Dv -> "Dv"
  | Tot -> "Tot"
  | St -> "St"

(* Add parentheses around expressions based on context *)
let paren s = "(" ^ s ^ ")"

let rec string_of_expr = function
  | Var x -> x
  | BinOp (op, e1, e2) -> 
      Printf.sprintf "(%s %s %s)"
      (string_of_expr e1)
      op
      (string_of_expr e2)
  | Int n -> string_of_int n
  | Let (flag, x, t_opt, e1, e2) ->
      let type_annot = match t_opt with
        | None -> ""
        | Some t -> ": " ^ paren (string_of_type_expr t)
      in
      Printf.sprintf "(let %s %s%s = %s in\n%s)"
        (if flag then "rec" else "")
        x
        type_annot
        (string_of_expr e1)
        (string_of_expr e2)
  | If (cond, then_expr, else_expr) ->
      Printf.sprintf "(if %s then\n  %s\nelse\n  %s)"
        (string_of_expr cond)
        (string_of_expr then_expr)
        (string_of_expr else_expr)
  | App (e1, e2) ->
      Printf.sprintf "(%s %s)"
        (string_of_expr e1)
        (string_of_expr e2)
  | Fun (x, body) ->
      Printf.sprintf "(fun %s -> %s)"
        x
        (string_of_expr body)
  | Print body -> 
      Printf.sprintf "(print_any %s)"
        (string_of_expr body)

and string_of_type_expr = function
  | Arrow (t1, t2, eff) ->
      Printf.sprintf "(%s -> %s(%s))"
        (string_of_type_expr t1)
        (string_of_effect eff)
        (string_of_type_expr t2)
  | TInt (name, expr) ->
      Printf.sprintf "(%s:int{%s})"
      name 
      (string_of_expr expr)

let prologue = {|
module Main

open FStar.IO
open FStar.All

val flag: x:int{false} -> ML unit
let flag _ = print_string "flag{hello}\n"
val main: unit -> ML unit
let main () =|}

let print_prog expr = 
  Printf.sprintf "%s(%s)\n" prologue (string_of_expr expr)

