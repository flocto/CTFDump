type effect =
  | Dv
  | Tot
  | St

type expr =
  | Var of string
  | BinOp of string * expr * expr
  | Int of int
  | Print of expr 
  | Let of bool * string * type_expr option * expr * expr
  | If of expr * expr * expr
  | App of expr * expr
  | Fun of string * expr
and type_expr = 
  | Arrow of type_expr * type_expr * effect
  | TInt of int_ty 
and int_ty = string * expr

let ban_words = ["admit"; "magic"; "assume"; "requires"; "unsafe";]
let check_ban v = let open Core in List.for_all ~f:(fun x -> Option.is_none (String.substr_index ~pattern:x v)) ban_words 

let rec well_formedness e vars = match e with
  | Var x -> List.mem x vars
  | BinOp (_, e1, e2) -> well_formedness e1 vars && well_formedness e2 vars
  | Int _ -> true
  | Print e -> well_formedness e vars
  | Let (rec_flag, x, ty, e1, e2) -> 
    (if rec_flag then 
      well_formedness e1 (x::vars)
    else well_formedness e1 vars)
     && well_formedness e2 (x::vars) && check_ban x && begin match ty with
    | Some t -> well_formedness_type t vars
    | None -> true
      end
  | If (e1, e2, e3) -> well_formedness e1 vars && well_formedness e2 vars && well_formedness e3 vars
  | App (e1, e2) -> well_formedness e1 vars && well_formedness e2 vars
  | Fun (x, e) -> check_ban x && well_formedness e (x::vars)
and well_formedness_type t vars = match t with
  | Arrow (t1, t2, _) -> well_formedness_type t1 vars && well_formedness_type t2 vars
  | TInt e -> well_formedness_int_ty e vars
and well_formedness_int_ty (x, e) vars = well_formedness e (x::vars) && check_ban x
