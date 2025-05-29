---
layout: post
title: A tiny lisp interpreter (tbh, not even close)
---

I have written a Lisp parser before, and I am thinking about writing a Lisp interpreter.

Tl;DR: it is not even close to being an interpreter, but I reviewed and learned something in Rust instead.

## Lexer/Parser part ##

I have written something like this several times before, so it isn't that hard. This time I want to try a "router" design, which I use a lot in my work.

```rust
fn read_router(
    token: &str,
) -> Result<fn(&mut VecDeque<String>) -> Result<Atom, ParserError>, ParserError> {
    match token {
        "(" => Ok(read_exp),
        "'" => Ok(read_quote),
        "\"" => Ok(read_string),
        _ => Ok(read_sym),
    }
}
```

After finishing this, the major point of this blog just revealed itself: `fn(&mut VecDeque<String>) -> Result<Atom, ParserError>` is the type. I'm pretty sure I learned it before, but I hadn't used it for a long time, and I put myself into "trait magic" too much. I even forgot that `fn` is the primary type.

## Expression ##

Then I need to write the expression evaluation logic. I want to make a `HashMap<function name, function>` inside the context.

```rust
type Lmda = fn(&mut Context, &Args) -> Result<Value, ExpressionError>;
```

I even tried to use HRTB in this type alias, but actually, I don't need it.

After all, I can run one tiny Lisp-like expression:

```rust
#[test]
fn test_eval() {
    let mut t = tokenize(Cursor::new(r#"(add 1 2 3)"#.as_bytes()));
    let atom = &read_root(&mut t).unwrap();
 //dbg!(atom);
 let mut ctx = Context {
        ..Default::default()
    };
 ctx.fnTable.insert("add".to_string(), functions::math::add);
 let exp = Expr::from_atom(atom, Rc::new(RefCell::new(ctx)));
 assert_eq!(exp.eval(), Ok(Value::Number(6)));
 //
 let mut t = tokenize(Cursor::new(r#"(add 1 2 (add 3 1))"#.as_bytes()));
    let atom = &read_root(&mut t).unwrap();
 let mut ctx = Context {
        ..Default::default()
    };
 ctx.fnTable.insert("add".to_string(), functions::math::add);
    let exp = Expr::from_atom(atom, Rc::new(RefCell::new(ctx)));
 assert_eq!(exp.eval(), Ok(Value::Number(7)));
}
```

## Wrap up ##

It is not even an interpreter; it cannot create new functions, and functions have to be written in Rust.

But the joy I got after recalling that `fn` is a primary type was good.
