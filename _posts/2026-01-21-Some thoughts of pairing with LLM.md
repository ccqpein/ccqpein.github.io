---
layout: post
title: Some thoughts of pairing with LLM
---

I have been using AI (LLMs) for years, ever since the release of ChatGPT 3.5. I have also built several things with AI, such as:

*   A Telegram bot (making ChatGPT API calls through the bot).
*   Contributing to open-source AI projects.

ChatGPT was 10 bucks per month, and I thought the API calls would be cheaper—and they truly are. However, I am now using the Gemini API and Gemini Pro because Gemini can use Google Search, which I find very helpful when I need up-to-date information.

I use LLMs for two major purposes: general usage and tech stuff. Both have given me ideas and thoughts on how to best utilize them.

## General Usage

General usage involves helping me read, querying information, providing summaries, and comparing ideas.

### Asking questions like on StackOverflow

As a programmer of many years, I read an article at the very beginning of my programming journey called [How-To-Ask-Questions-The-Smart-Way](https://github.com/selfteaching/How-To-Ask-Questions-The-Smart-Way/blob/master/How-To-Ask-Questions-The-Smart-Way.md). It was very helpful, especially in an age where we still needed to do tons of Google searches to find answers.

Now, the LLM is the "killer app" for this job. However, I find I still need the same guidelines on how to ask a good question. I see people complain that LLMs don't understand what they are asking, but I have never encountered this. Even when I ask questions that I think aren't very clear, the LLM still manages to understand me.

### Perfect for my reading habits

Whenever I am curious about a blog post, I usually have a lot of questions pop up while I am reading. Before LLMs, I had to Google those ideas, put them on a reading list, and often forget them for a while. I would just save the questions somewhere and search for them later to keep my reading flow.

Now, with an LLM, I put my questions into the input window as a bulleted list while I read. I send those questions once I finish the article. The LLM gives me the answers and explanations immediately. I call this habit "brainstorming reading." LLMs have turned a potential distraction into a steady flow of learning. I love it.

## For Tech Stuff

I am still a programmer, and it is still my hobby (yes, my job hasn't been replaced by AI yet). I use LLMs to help me with technical tasks, and they are quite good at it.

In the ChatGPT 3.5 era, I only asked about Python and SQL because I believed LLMs were best at languages that:
1.  Have a lot of existing content (so the LLM is well-trained).
2.  Have been standardized for a long time (lowering the possibility of the LLM providing outdated code).

Once I found that Gemini could use search, I started asking questions about documentation for newer projects, which is why I switched to Gemini entirely.

### API usage is awesome

The best part of using an LLM for coding so far is writing demo code for APIs. Usually, it would take me hours to learn, search, and read example code. For example, I used Qdrant to write a tool for myself, and I asked Gemini to write the helper function for me:

```rust
pub async fn update_file_path_by_file_id(
    &self,
    collection_name: &str,
    file_id: Uuid,
    new_file_path: &str,
) -> Result<()> {
    let filter = qdrant_client::qdrant::Filter {
        must: vec![qdrant_client::qdrant::Condition {
            condition_one_of: Some(qdrant_client::qdrant::condition::ConditionOneOf::Field(
                qdrant_client::qdrant::FieldCondition {
                    key: "file_id".to_string(),
                    r#match: Some(qdrant_client::qdrant::Match {
                        match_value: Some(qdrant_client::qdrant::r#match::MatchValue::Keyword(
                            file_id.to_string(),
                        )),
                    }),
                    ..Default::default()
                },
            )),
        }],
        ..Default::default()
    };
    
    let payload = serde_json::json!({
        "file_path": new_file_path
    });
    let payload: Payload = payload.try_into()?;
     self.client
        .set_payload(
            SetPayloadPointsBuilder::new(collection_name, payload).points_selector(filter),
        )
        .await?;
     Ok(())
}
```

Similar to the SeaORM SDK, the Qdrant query API is complex. I don’t know how much time I would have spent figuring it out, but I bet it wouldn't have been short. Gemini does it very well. I can use the generated code now and refine it later—just like copying example code from StackOverflow.

### Maybe I need more tests?

One thing I've noticed is that LLMs sometimes miss certain requirements I provide. For Gemini, it doesn't always show the full code block, which increases the chance of bugs. Because of this, I’m thinking about revisiting an old term: `Test-Driven Development (TDD)`. I can write the tests and function declarations first, mark them with TODO tags, and have Gemini fill in the logic. Then, I just need the code to pass the tests.

### More code review

A mental pattern shift I’ve noticed while pair-programming with an LLM is that I need to review code much more than I used to. I review code every day at work, but now I have to review Gemini's output every time it touches my source code. I’ve even started manually staging code in Git before letting the AI change anything (something I didn't do often before).

It’s something I need to get used to, I guess. I’m okay with it because reviewing code takes much less time than learning a complex API from scratch.

### Rust, by the way

Another thing I’ve found is that "Rust is great for LLM coding." Gemini can often fix its own errors just by looking at the output of `cargo check`. The Rust type system is incredibly helpful here. It reminds me of when I was learning Haskell; people said, "If it passes the type check, it will run." I have the same feeling with Rust. Combined with amazing error messages, Rust is a perfect match for AI-paired coding.
