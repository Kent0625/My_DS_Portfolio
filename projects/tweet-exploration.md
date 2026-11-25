# Exploring a corpus of labeled tweets

SQLAlchemy · SQLite · pandas

I queried 41,157 labeled tweets from SQLite with SQLAlchemy and loaded them into pandas. I standardized the date field and cleaned punctuation so that I could inspect the text alongside the supplied sentiment labels.

| Measure | Posts |
|---|---:|
| Records queried | 41,157 |
| Matching records | 1,098 |

A case-insensitive substring search of the tweet text returned 1,098 posts containing “quarantine,” about 2.67% of the corpus. This measures mentions of that string. Tweets discussing the same topic in other words fall outside the count.
