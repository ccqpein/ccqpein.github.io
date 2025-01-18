---
layout: post
title: Some weird DB connection lost
---

I encountered a strange issue when I was writing some DB tests with [SeaOrm](https://www.sea-ql.org/SeaORM/) a few days ago. For some reason, I felt that the DB connection was being dropped. Eventually, I realized the issue was caused by a "hidden" (not exactly) problem related to Tokio.

## Issue ##

I'll post the demo code here. I initially thought it might be related to the `#[cfg(test)]` macro, so I attempted to reproduce the issue within the `mod tests` module:

```rust
#[cfg(test)]
mod tests {
    use std::sync::LazyLock;

    use sea_orm::{ConnectionTrait, Database, DatabaseBackend, DatabaseConnection, Statement};
    use tokio::runtime::Runtime;
    use tracing::{debug, error, info};

    static DB_CONNECTION: LazyLock<DatabaseConnection> = LazyLock::new(|| {
        dbg!("in db connecting"); // Reached here
        let re = Runtime::new().unwrap().block_on(async {
            Database::connect("postgres://test_user:test_password@localhost:5432/test_db")
                .await
                .expect("db connect error")
        });
        dbg!("connected"); // Reached here
        re
    });

    #[test]
    fn test() {
        tracing_subscriber::fmt()
            .with_max_level(tracing::Level::DEBUG)
            .with_test_writer()
            .init();

        LazyLock::force(&DB_CONNECTION);

        let rt = Runtime::new().unwrap();

        rt.block_on(async {
            dbg!("in here?"); // Reached here
            let re = DB_CONNECTION
                .execute(Statement::from_string(
                    DatabaseBackend::Postgres,
                    "DELETE FROM test_table;",
                ))
                .await
                .unwrap();
            dbg!(re); 
            dbg!("done");
        });
    }
}
```

When I ran the code with `env RUST_LOG="debug" cargo test`, the output showed that the program was stuck on `.execute`.

Out of habit, I started inspecting the source code. Tracing from [SeaOrm](https://docs.rs/sea-orm/latest/src/sea_orm/driver/sqlx_postgres.rs.html#143) to [sqlx](https://docs.rs/sqlx-core/0.8.3/src/sqlx_core/pool/mod.rs.html#355), I began to suspect a connection loss.

After running more tests:

```rust
    #[test]
    fn test() {
        tracing_subscriber::fmt()
            .with_max_level(tracing::Level::DEBUG)
            .with_test_writer()
            .init();

        // This also times out
        let DB_CONNECTION: LazyLock<DatabaseConnection> = LazyLock::new(|| {
            dbg!("in db connecting");
            let re = Runtime::new().unwrap().block_on(async {
                Database::connect("postgres://test_user:test_password@localhost:5432/test_db")
                    .await
                    .expect("db connect error")
            });
            dbg!("connected");
            re
        });
        LazyLock::force(&DB_CONNECTION); // Force initialization of the DB connection

        let rt = Runtime::new().unwrap();
        rt.block_on(async {
            dbg!("in here?");
            let re = DB_CONNECTION
                .execute(Statement::from_string(
                    DatabaseBackend::Postgres,
                    "DELETE FROM test_table;",
                ))
                .await
                .unwrap();
            dbg!(re);
            dbg!("done");
        });
    }
```

This still timed out. I then suspected it might be due to the `LazyLock`. Since it was only added to the standard library recently, I decided to try the older `lazy_static` approach:

```rust
#[cfg(test)]
mod tests {
    use lazy_static::lazy_static;
    use std::sync::LazyLock;

    use sea_orm::{ConnectionTrait, Database, DatabaseBackend, DatabaseConnection, Statement};
    use tokio::runtime::Runtime;
    use tracing::{debug, error, info};

    lazy_static! {
        static ref DB_CONNECTION: DatabaseConnection = {
            dbg!("in db connecting");
            let re = Runtime::new().unwrap().block_on(async {
                Database::connect("postgres://test_user:test_password@localhost:5432/test_db")
                    .await
                    .expect("db connect error")
            });
            dbg!("connected");
            re
        };
    }

    fn use_connection(db: &DatabaseConnection) {}

    #[test]
    fn test() {
        tracing_subscriber::fmt()
            .with_max_level(tracing::Level::DEBUG)
            .with_test_writer()
            .init();

        let rt = Runtime::new().unwrap();
        use_connection(&DB_CONNECTION);

        rt.block_on(async {
            dbg!("in here?");
            let re = DB_CONNECTION
                .execute(Statement::from_string(
                    DatabaseBackend::Postgres,
                    "DELETE FROM test_table;",
                ))
                .await
                .unwrap();
            dbg!(re);
            dbg!("done");
        });
    }
}
```

Unfortunately, this also timed out.

## How to Make it Work ##

If I avoid using a `LazyLock`-generated static DB connection, the code works fine:

```rust
        let rt = Runtime::new().unwrap();

        // Code below works
        let DB_CONNECTION = rt.block_on(async {
            Database::connect("postgres://test_user:test_password@localhost:5432/test_db")
                .await
                .expect("db connect error")
        });

        rt.block_on(async {
            dbg!("in here?");
            let re = DB_CONNECTION
                .execute(Statement::from_string(
                    DatabaseBackend::Postgres,
                    "DELETE FROM test_table;",
                ))
                .await
                .unwrap();
            dbg!(re);
            dbg!("done");
        });
```

## Ok, I'm Stuck. Let Me See What the Internet Says ##

I posted this question [here](https://users.rust-lang.org/t/sqlx-connection-pool-timeout-issue-with-tokio/123892).

Thanks to @ohdanek for answering my question:

> Actually, I recreated the problem and figured out that blocking occurs because you created Runtime in such way Runtime::new().unwrap().block_on()
>
> Instance of the Runtime immediatly deconstructs after the block_on invocation, it leads shutting down all Runtime resources.
>
> Because the DB_CONNECTION was created in the deconstructed Runtime, the second Runtime "loses" control because the asynchronous communication resources are no longer maintained.
