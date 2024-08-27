---
layout: post
title: Re-write from lazy_static to LazyLock.
---

From Rust [1.80](https://blog.rust-lang.org/2024/07/25/Rust-1.80.0.html), `LazyLock` is now part of the stable channel. To be honest, it is the first time I realized the Rust team was trying to stabilize the `lazy_static` feature. This is great news because I have been using `lazy_static` in some of my projects, and I am eager to rewrite them using `LazyLock` (`LazyCell`).

## What did I do with lazy_static? ##

I use `lazy_static` similarly to how other languages use global values. Sometimes, I just want to keep a global variable. I don't understand the implementation details of `lazy_static`; I just use it like `(defparameter)` in Lisp.

## Start to rewrite it ##

The first project I am thinking of rewriting is my [code-it-later-rs](https://github.com/ccqpein/code-it-later-rs). I use `lazy_static` to generate three global static tables.

The change is:

```diff
@@ -25,19 +24,19 @@ const DICT: &'static str = r#"
 }
 "#;
 
-lazy_static! {
-    /// The table including all languages filetype and its comment symbols
-    static ref TABLE: Mutex<HashMap<String, Vec<String>>> =
-        Mutex::new(serde_json::from_str(DICT).unwrap());
+static TABLE: LazyLock<Mutex<HashMap<String, Vec<String>>>> =
+    LazyLock::new(|| Mutex::new(serde_json::from_str(DICT).unwrap()));
 
-    /// Regex table, like "rs" => "(//+):=\s+(.*)"
-    pub static ref REGEX_TABLE: Mutex<HashMap<String, Regex>> = Mutex::new({
+pub static REGEX_TABLE: LazyLock<Mutex<HashMap<String, Regex>>> = LazyLock::new(|| {
+    Mutex::new({
         let a = TABLE.lock().unwrap();
-        a.iter().map(|(k, v)| (k.clone(), Regex::new(&make_regex(v)).unwrap())).collect()
-    });
+        a.iter()
+            .map(|(k, v)| (k.clone(), Regex::new(&make_regex(v)).unwrap()))
+            .collect()
+    })
+});
 
-    pub static ref KEYWORDS_REGEX: Mutex<Option<Regex>> = Mutex::new(None);
-}
+pub static KEYWORDS_REGEX: LazyLock<Mutex<Option<Regex>>> = LazyLock::new(|| Mutex::new(None));
```

It is pretty straightforward. At the beginning, I tried to rewrite it like this:

```rust
static TABLE: LazyLock<Mutex<HashMap<String, Vec<String>>>> =
    LazyLock::new(|| serde_json::from_str(DICT).unwrap());
```

because I thought it might have a lock inside. Then I figured out that `LazyLock` doesn't have any `Sync`/`Send` constraints at all. It also doesn't have the `as_mut` method like `Mutex`. So I needed to add the `Mutex`, just as I did with `lazy_static`.

Furthermore, because `LazyLock<T>` only implements the `Deref` trait and not `Send`/`Sync`, the concurrency safety guarantee is left to `T` itself. This means `T` must implement `Sync`.

According to the `Sync` [documentation](https://doc.rust-lang.org/1.80.1/std/marker/trait.Sync.html):

> &T is Send if and only if T is Sync.

So, I think the `LazyLock` just implementing `Deref` is a good choice, making things simple.

## Wrap up ##

+ It appears that `LazyLock` ensures that the `T` inside can be initialized safely in different threads. Whether `T` is concurrency-safe or not is not a concern it addresses.
+ I tried to use the [`cfg_version`](https://github.com/rust-lang/rust/issues/64796) feature to ensure that Rust versions less than `1.80` can still use `lazy_static` when installing. However, it looks like this feature is still nightly and not included in the stable standard library yet. I might change it in the future.
