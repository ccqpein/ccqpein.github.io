---
layout: post
title: Make Common Lisp format function into Rust
---

One day, I wanted to use the format function inside my Rust. I considered writing it on my own, so that others could potentially use it and experience a bit of Lisp (just a tiny bit). 

After reading some articles and doing a bit of studying, I usually just used it rather than looking closely enough to attempt to replicate it. I identified two major components that I needed to create separately. One was the control string, and the other was the input arguments. I decided to reveal them after everything was done. 

I must admit, I originally thought this task would be easy. However, nothing is easy when I make my hands dirty and dive into the details. So, let the journey begin.

## Control String ##

When I began with the control string, there were several things in mind. First, the control string should be created once and used multiple times. Consequently, it is the structure instance that encompasses all matters. Second, it should retain all symbols (like `~a`) and their corresponding types (which I should define) as well.


### Define Types ###

Let me define the type first. I am grateful for Rust's generous type system. I defined the `TildeKind` enum type as follows:

```rust
pub enum TildeKind {
    /// ~a
    Va,
    /// there are more kinds too
}
```

I chose this method as it allows me to easily add new enum members and focus on a specific member while developing its MVP.

The common Lisp standard has a lot of "TildeKind", honestly, I was unaware there were so many. Until this post, I've only implemented the necessary ones along with the ones I frequently use.

### Parser ###

As part of the control string component, there needs to be a parsing function that converts a string into a list of `TildeKind`. This allows the control string struct to contain the TildeKind and reveal it alongside the arguments.

Initially, I created a parse function to serve as the start point for all parser determinations.

```rust
pub fn parse(c: &mut Cursor<&'_ str>) -> Result<Self, TildeError> {
    let parser = Self::scan_for_kind(c)?;
    parser(c)
}
```

This function takes a `Cursor` type, which is often used in many parsing and scanning string operations. Then, `scan_for_kind` will yield a function to determine which parser function should perform the task. This is what `scan_for_kind` looks like:

```rust
fn scan_for_kind(
    c: &mut Cursor<&'_ str>,
) -> Result<
    Box<dyn for<'a, 'b> Fn(&'a mut std::io::Cursor<&'b str>) -> Result<Tilde, TildeError>>,
    TildeError,
> {
    //
    // some check 
    //

    match buf {
        [b'a', ..] | [b'A', ..] => {
            c.seek(SeekFrom::Current(-buf_offset))
                .map_err(|e| TildeError::new(ErrorKind::ParseError, e.to_string()))?; // back to start
            return Ok(
                #[rustc_box]
                Box::new(Self::parse_value),
            );
        },
		...
}
```

It returns the function of the parser and boxes them for an external call. Yes, I could directly call them within this function, but since the control string is only generated once, I don't believe optimization is paramount here.

## Wait, let's think a bit ##

After coding numerous parser functions, I started to think about the design of the traits that I wanted. I was envisaging something similar to Lisp - flexible enough to change behavior at runtime. This would involve some `Box<T>` magic, due to the need to decide on behavior at runtime. For instance, if `~a` is in the control string, the type it reveals when used in functions is unknown. It could be a `string`, an `i32`, or just about anything. 

Inaddition, these types had to be linked with the `TildeKind` I had defined. It was a fun challenge thinking about this design.

## Traits ##

I was thinking make every memebers inside the `TildeKind` enum has its own trait to reveal. Which means I give the ability of fine control that which types implenment which trait. 

For example, `TildeKind::Va` will pair with the trait `TildeKindVa`, then every types which implenmented the `TildeKindVa` can be reveal as `~a`. This design make same type can be reveal as multiple `TildeKind`. Like `String` can be `~a` and `~S`, just implenment `String` with `TildeKindVa` and `TildeKindStandard`. 

Then the quesion is: how can I make sure the type is implenment the speciafic trait? I was thinking type impenment the reveal trait, like `TildeKindVa`, should also implenment the `Tildeable` trait to check if this type has implenmented the reveal trait.

Like

```rust
// has to derive to Debug
#[derive(Debug)]
struct MyStruct {
    a: usize,
    b: String,
}

trait TildeAble {
	fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa> {
        Some(self)
    }
}

impl TildeAble for MyStruct {
	// ~a is good enough
	fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa> {
        Some(self)
    }
}
```

Then when I reveal it, I check the `into_tildekind_va` first, and reveal it as the `TildeKindVa`.

After this design, I actully also make the feature automaticlly that custom structure can be reveal by `cl-format`.

## Macros ##

After finish the design, `TildeKind` have connected with the `TildeAble` and there definatly a lot hard code to generate the connections. Wait, did I just say generate? Sounds like use macro is the good way to do this job. 

I am thinking to make a derive macro and generate the reveal macros and implenment tildeable to some types.

Fortunately I have played around the macros before. That's the good news. The bad news is: syn package updated to version 2 (which I learn it when it version 1). And the example and turitals online mostly are outdate. After a lot try and test. I finally done the macro side.

Proc macro [code](https://github.com/ccqpein/cl-format-rs/blob/b3819555e36ea63f1042f834e6f67f4e259ce1d5/cl-format-macros/src/lib.rs#L89) get the all memebers in `TildeKind` and generate their reveal trait (like `Va -> TildeKindVa`) and give default "unimplenment" error, make the `TildeAble` trait, implenment `TildeAble` to the types in the derive arguments `implTo`.

For example, the `TildeKind` like this:

```rust
#[derive(Debug, PartialEq, TildeAble)]
pub enum TildeKind {
    /// ~a
    #[implTo(float, char, String)]
    Va,
}
```

will expand to:

```rust
trait TildeAble {
    fn len(&self) -> usize;
    fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa>{None}
}

/// impl arguments in derive macro 

impl TildeAble for char {
    fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa> {
        Some(self)
    }
}

impl TildeAble for float {
    fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa> {
        Some(self)
    }
}

impl TildeAble for String {
    fn into_tildekind_va(&self) -> Option<&dyn TildeKindVa> {
        Some(self)
    }
}

/// generate the reveal trait

trait TildeKindVa {
    fn format(&self, tkind: &TildeKind, buf: &mut String) -> Result<(), TildeError> {
        Err("un-implenmented yet".into())
    }
}
```

## Arguments ##

Having built the `TildeKind` parser and completed the trait design, the next step was to implement the reveal traits for numerous types. To summarize, after a lot of testing and coding, I realized that I needed a special "Arguments" type. Initially, Args was simply another name for `Vec<&dyn TildeAble>`. However, when implementing `Vec<&dyn TildeAble>`, `TildeKind::Cond`, and `TildeKind::Loop`, I became aware that I needed a type to pair with the control string type at the upper level, wrapping all arguments prior to their revelation.


```rust
pub struct Args<'a> {
    len: usize,
    inner: Vec<&'a dyn TildeAble>,
    ind: RefCell<usize>,
}
```

In the Args struct, I maintain the length and the index (ind) of the arguments. This allows for the handling of special loop and condition tilde kinds.

## Optimization ##

There are several things I can do to improve this repository. Firstly, I could cut down some code through writing macros. Secondly, I could look for ways to enhance its speed.

### Helper macro ###

Because the reveal trait needs to identify which type is in runtime, we will have many `&dyn TildeAbles` (like inside the `Args<'s>`).

So, I wrote a macro, `tilde!`, just to add as `&dyn TildeAble`. Unlike the proc macro `TildeAble` I mentioned earlier, it's just a regular `macro_rules!`.

Additionally, there are some other macros I would like to write because some types implement the same trait with completely identical details.

For instance, i32, i64, u32, u64, usize all call `.to_string()` in the reveal trait `TildeKindDigit`. This means I need to write a macro that implements the reveal trait for all types thought to have duplicated hardcoded details.

Lastly, I wrote a `cl_format!` for invocation in Rust like I did in Common Lisp. In this way, I can call it as follows:

```rust
let l = vec![tilde!(&1), &2, &3];
let a = cl_format!("~{~a~#[~;, and ~:;, ~]~}", &l);
assert_eq!(String::from("1, 2, and 3"), a.unwrap());
```

### Write some benchmark first ###

After releasing the first version of `cl-format`, I grew increasingly curious about how fast it could be – and whether I could make it faster. This was, undoubtedly, a valuable learning experience to optimize code in Rust.

I've run several benchmarks inside my demo repository, but given that they were quite outdated, I figured it was time to write new benchmarks. After some recollection and research, I evaluated the `criterion` library and found it satisfactory, hence shifting from [bench] to criterion.

Once I obtained the benchmark results, I considered using flamegraph. My initial attempt to use `pprof` to generate flamegraph with criterion was unsuccessful, but I then discovered the [flamegraph](https://github.com/flamegraph-rs/flamegraph). After solving the SIP issue on Apple Silicon via running `csrutil enable --without dtrace` in recovery mode, I finally managed to generate the flamegraph. I ran `cargo flamegraph -o bench0_flamegraph --bench bench0 -- --bench` to identify which parts were the most time-consuming.

### Memory allocation ###

Reading the flamegraph, I noticed that memory allocation took up a considerable amount of time. To improve this, I made some minor optimizations: I made all functions add strings to a `&mut string` buffer rather than return entirely new strings. This instantly increased the speed by almost 20% for all benchmark cases. 

Of course, this was coupled with some predictions of memory usage by `String::with_capacity(args.left_count());` to generate the string buffer.

## Something fun from making the cl-format ##

### Macro ###

+ The `&self` inside the implement trait method needs to be written directly within the macro-calling arguments.
+ Allocating memory genuinely consumes a considerable amount of time.
