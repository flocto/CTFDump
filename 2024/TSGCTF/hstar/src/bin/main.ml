open Core

let base = "out/"

let parse_string s =
  let lexbuf = Lexing.from_string s in
  try
    (* print all tokens *)
    let rec print_all_tokens () =
      let tok = Lexer.token lexbuf in
      print_endline (Parser.string_of_token tok);
      match tok with
      | Parser.EOF -> ()
      | _ -> print_all_tokens ()
    in
    print_all_tokens ();

    Parser.prog Lexer.token lexbuf
  with
  | Lexer.Error msg -> failwith ("Lexing error: " ^ msg)
  | Parser.Error -> failwith "Parsing error"

let generate_random_string length =
  String.init length ~f:(fun _ ->
    let charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789" in
    charset.[Random.int (String.length charset)])

let write_file ~path ~content =
  Out_channel.write_all path ~data:content

let execute_command cwd cmd =
  let orig_cwd = Sys_unix.getcwd () in
  Core_unix.chdir cwd;
  let status = Sys_unix.command cmd in
  Core_unix.chdir orig_cwd;
  status = 0

let eof_marker = "__EOF__"
let read_input () =
  let buf = Buffer.create 10000 in
  let rec loop count =
    match In_channel.input_char In_channel.stdin with
    | Some c ->
        if count >= 10000 then 
          failwith "Input exceeds 10000 characters";
        Buffer.add_char buf c;
        let content = Buffer.contents buf in
        if String.is_suffix content ~suffix:eof_marker then
          String.drop_suffix content (String.length eof_marker)
        else
          loop (count + 1)
    | None -> Buffer.contents buf
  in
  loop 0
(*
-- programs -- 

let f = \x -> x - 1 in
  let g:: (x::Integer{x > 0}) -> x::Integer{x>0} = \x -> x + 1 in
  let g:: (x::Integer{x > 0}) -> (x::Integer{x>0}) -> Dv(x::Integer{true}) = \x -> \y -> if x > y then x - 2 else y - 1 in
  print 1
__EOF__

*)

let () =
  let p = read_input () in
  let e = parse_string p in

  if not (Ast.well_formedness e ["flag"]) then
    failwith "Program is not well-formed";

  Random.self_init ();
  let dir_name = base ^ generate_random_string 10 in
  Core_unix.mkdir_p dir_name;

  let write_source ~filename ~content =
    let path = Filename.concat dir_name filename in
    write_file ~path ~content;
  in
  let fstar_s = Print_fstar.print_prog e in
  write_source ~filename:"Main.fst" ~content:fstar_s;

  if execute_command dir_name "fstar.exe Main.fst > /dev/null 2>&1" then begin
    let haskell_s = Print_haskell.print_prog e in
    write_source ~filename:"main.hs" ~content:haskell_s;
    assert(execute_command dir_name "ghc main.hs > /dev/null 2>&1");
    assert(execute_command dir_name "./main")
  end


