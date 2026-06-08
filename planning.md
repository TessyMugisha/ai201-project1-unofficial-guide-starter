# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

My domain is student reviews of Oklahoma Christian University professors, collected from Rate My Professors. This knowledge is valuable because it reflects honest, firsthand student experience of what a professor's class is actually like, things like grading style, teaching approach, and workload, that the official course catalog never tells you. It's hard to find otherwise because it lives scattered across individual review pages, often contradicts itself, and requires reading through many opinions to form an accurate picture.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | Source|                     | Description|                              | URL or location |
|---|----------------------------|------------|------------------------------|------------------|
| 1 |Rate My Professors|Paul Howard (Math) review – MATH1614, rated 5.0|ratemyprofessors.com/professor/1666205
| 2 | Rate My Professors|Paul Howard (Math) review – MATH1213, rated 5.0|ratemyprofessors.com/professor/1666205
| 3 | Rate My Professors|Paul Howard (Math) review – MATH1623, rated 4.0|ratemyprofessors.com/professor/1666205
| 4 | Rate My Professors|Paul Howard (Math) review – MATH1623, rated 4.0|ratemyprofessors.com/professor/1666205
| 5 | Rate My Professors|Paul Howard (Math) review – MATH1213, rated 1.0|ratemyprofessors.com/professor/1666205
| 6 | Rate My Professors|Chris Austin (Physics) review – PHYS1114, rated 4.0|ratemyprofessors.com/professor/1629835
| 7 | Rate My Professors|Chris Austin (Physics) review – PHYS1214, rated 1.0|ratemyprofessors.com/professor/1629835
| 8 | Rate My Professors|Chris Austin (Physics) review – PHYS1214, rated 1.0|ratemyprofessors.com/professor/1629835
| 9 | Rate My Professors|Chris Austin (Physics) review – PHYS1214, rated 1.0|ratemyprofessors.com/professor/1629835
| 10 | Rate My Professors|Chris Austin (Physics) review – PHYS1214, rated 5.0|ratemyprofessors.com/professor/1629835
| 11 | Rate My Professors|Matthew McCook (History) review – HIST2213, rated 1.0|ratemyprofessors.com/professor/134785
| 12 | Rate My Professors|Matthew McCook (History) review – course 1223, rated 1.0|ratemyprofessors.com/professor/134785
| 13 | Rate My Professors|Matthew McCook (History) review – US1877, rated 5.0|ratemyprofessors.com/professor/134785
| 14 | Rate My Professors|Matthew McCook (History) review – HIST122301, rated 4.0|ratemyprofessors.com/professor/134785
| 15 | Rate My Professors|Matthew McCook (History) review – FRESHMAN geography, rated 2.0|ratemyprofessors.com/professor/134785
---

## Chunking Strategy

**Chunk size:** One review per chunk (variable length, roughly 20–120 words each). I split on the `---` separator between reviews rather than by a fixed token or character count.

**Overlap:** None. Each review is treated as an independent, self-contained unit.

**Reasoning:** My documents are individual professor reviews, which are already short, self-contained opinions. Each review expresses one student's complete take on a professor, so the natural boundary is the review itself, not an arbitrary character count. Splitting mid-review would break a single coherent opinion across two chunks and pollute retrieval, while merging multiple reviews into one chunk would blur different students' perspectives (which matters a lot here, since reviews for the same professor often contradict each other). Overlap exists to preserve context that would otherwise be cut at an arbitrary boundary, but because my boundaries fall cleanly between whole reviews, there's no context to preserve across them, so overlap would only add redundant noise. I keep each review's metadata (professor, rating, course, date) attached to its chunk so retrieval and source citation stay accurate.

---

**Chunk size:**

**Overlap:**

**Reasoning:**

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**

**Top-k:**

**Production tradeoff reflection:**

---

## Evaluation Plan

| # | Question | Expected answer |
|---|----------|-----------------|
| 1 | What do students say about Professor Howard's teaching style? | Students describe Howard as intelligent, passionate, and caring, but note he talks fast, rambles, and can be hard to follow. Generally positive (most reviews rate him 4–5). |
| 2 | Is Professor Austin a good teacher? | Reviews are split. Some students rate him 5.0 and call him encouraging and fair with curving; others rate him 1.0, saying he doesn't teach, relies on videos, and weights exams heavily. The honest answer is that opinions strongly conflict. |
| 3 | How are exams weighted in Professor Austin's physics class? | At least one student reports exams are worth 75% of the final grade, with class averages in the 50s. |
| 4 | Does Professor McCook use study guides? | No. One student specifically notes he doesn't believe in study guides, and grades rely heavily on exams, random quizzes, and notebook checks. |
| 5 | Which professor should I take if I want an easy class? | McCook's US1877 course is described as easy and highly recommended (rated 5.0), but this is course-specific; his other courses are rated much harder. A good answer should flag that "easy" depends on the specific course. |

---

## Anticipated Challenges

1. **Contradictory reviews for the same professor.** Austin and McCook both have reviews ranging from 1.0 to 5.0 for overlapping courses. Semantic retrieval might surface only the positive or only the negative chunks depending on how the query is phrased, producing a one-sided answer that hides the real disagreement. This is the failure case I most expect to document.

2. **Short chunks lacking context.** Some reviews are a single sentence ("Good professor who is really into math!"). When retrieved alone, these chunks carry almost no information for the LLM to ground an answer in, which could lead to vague responses or the model filling gaps with general knowledge (hallucination). My source-citation requirement should help me catch when this happens.

---

## Architecture


https://mermaid.ai/play?utm_source=ai_live_editor&utm_medium=share#pako:eNptUsGOmzAQ_ZWRL3toSAMkEFC7UgOrVaVE6nbbHgp7cMwErAU7a5tk0yj_XmOSnsrBYubNe35v5DNhskKSklLsWnlkDVUGfuSlAPt9KXLJ-g6Fga-iRm24FJ-26uN9CFPzbmDHW9QT8Beg8MDxqB347WQaKRxo-7RC9QKedw-rImt68cpF7cae9y03YAfvPM-7A417qqiRyoH-VRE-gw9soL2MllZOKiseui1WldWCD_ALmeXBsz3QsWnbehsu-HrjrSPvELimHuAKuICsUbKj-eoqmTnJvPiORnE80Ha0hx0VhjPQvOMtVdycrEeqWONgI_fe6-hMw_YETGouECquDRUMr9K5k34oHlGgDXdb36OSb7Beb1xRK9mLyjqjQh9R2Txa9oohMG4cxWqNak_FT20HnnpUp3GlWTAuAt6G3n-z30IGY8pSkAmpFa9IalSPE9Kh6uhQkvMwWRLTYIclSe1vhTvat6a0j-NiaXsqfkvZ3ZjWd92QdEdbbat-X1GDOae1ot2_rkIbTWU2oSFpGDkNkp7JO0nny3gaBnGYxMHcj6NlspiQE0njaLqc-XPfHotk6c_iy4T8cbfOplGymIWLMJwH_jzxo-TyF8JD4Ho
---

![Architecture diagram](images/architecture.png)


---

## AI Tool Plan

I'll use Claude as my primary code-generation tool, feeding it specific sections of this planning.md so the output matches my spec rather than a generic RAG template. I'll work stage by stage rather than asking for the whole pipeline at once, so I can verify each piece before moving on.

**1. Ingestion + Chunking**
- *Tool:* Claude
- *Input:* My Chunking Strategy section plus a sample of one .txt file, with instructions to split on the `---` separator and parse the metadata fields (PROFESSOR, RATING, COURSE, DATE) into a structured object alongside the review text.
- *Expected output:* A function that reads all 3 files from my data folder and returns a list of chunks, each with its text and metadata attached.
- *Verification:* I'll check the function returns exactly 15 chunks and spot-check that the metadata on a few chunks matches the original review.

**2. Embedding + Vector Store**
- *Tool:* Claude
- *Input:* My Architecture diagram and Retrieval Approach section, specifying all-MiniLM-L6-v2 for embeddings and ChromaDB for storage.
- *Expected output:* Code that embeds each chunk, stores it in ChromaDB with its metadata, and persists the store locally.
- *Verification:* I'll confirm the collection contains 15 entries and run one test query to see that it returns results.

**3. Retrieval**
- *Tool:* Claude
- *Input:* My Retrieval Approach section, specifying semantic similarity search and a top-k value.
- *Expected output:* A function that embeds a user query and returns the top-k most relevant chunks with their metadata.
- *Verification:* I'll run my 5 evaluation questions and manually check whether the retrieved chunks are actually relevant before adding generation.

**4. Generation**
- *Tool:* Claude
- *Input:* My requirement that answers be grounded only in retrieved chunks and include source attribution.
- *Expected output:* Code that passes the retrieved chunks to the Groq LLM with a prompt instructing it to answer only from the provided context and cite which professor/review each claim comes from.
- *Verification:* I'll test with a question whose answer isn't in my documents to confirm the system says it doesn't know rather than hallucinating.

**5. Evaluation**
- *Tool:* Claude
- *Input:* My Evaluation Plan table with the 5 questions and expected answers.
- *Expected output:* A script that runs each question through the full pipeline and logs the question, retrieved chunks, and generated answer for me to score.
- *Verification:* I'll judge each result as accurate, partially accurate, or inaccurate myself, since judging correctness is my job, not the AI's.

Across all stages, I'll read and understand every piece of generated code before using it, and adjust the prompts when output doesn't match my spec rather than accepting code I can't explain.

**Milestone 3 — Ingestion and chunking:**

**Milestone 4 — Embedding and retrieval:**

**Milestone 5 — Generation and interface:**
