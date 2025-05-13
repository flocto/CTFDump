open Ast


let indent n s =
  String.make n ' ' ^ s

let newline n = 
  Printf.sprintf "\n%s" (String.make n ' ')

let rec string_of_expr_indent n = function
  | Var x -> x
  | BinOp (op, e1, e2) -> 
      Printf.sprintf "(%s %s %s)"
        (string_of_expr_indent n e1)
        op
        (string_of_expr_indent n e2)
  | Int n -> string_of_int n
  | Let (_, x, _, e1, e2) ->
      let next_indent = n + 2 in
      Printf.sprintf "%slet %s = %s%sin %s"
        (newline n)
        x
        (string_of_expr_indent next_indent e1)
        (newline n)
        (string_of_expr_indent n e2)
  | If (cond, then_expr, else_expr) ->
      Printf.sprintf "(if %s then %s else %s)"
        (string_of_expr_indent n cond) 
        (string_of_expr_indent n then_expr)
        (string_of_expr_indent n else_expr)
  | App (e1, e2) ->
      Printf.sprintf "(%s %s)"
        (string_of_expr_indent n e1)
        (string_of_expr_indent n e2)
  | Fun (x, body) ->
      Printf.sprintf "(\\%s -> %s)"
        x
        (string_of_expr_indent n body)
  | Print body -> 
      Printf.sprintf "(print %s)"
        (string_of_expr_indent n body)

let string_of_expr expr = string_of_expr_indent 2 expr


(* get env[FLAG] if not, flag{hello}*)
let flag = Sys.getenv_opt "FLAG" |> function
  | Some s -> s
  | None -> "flag{hello}"

let prologue = Printf.sprintf {|
flag :: Integer -> IO ()
flag x = putStrLn "%s"

main :: IO ()
main =|} flag


let print_prog expr = 
    Printf.sprintf "%s%s\n" prologue (string_of_expr expr)