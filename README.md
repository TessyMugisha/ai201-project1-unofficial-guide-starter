# The Unofficial Guide — Project 1

[Watch the project walkthrough on Loom](https://www.loom.com/share/66461b5fbaac4b53b49a4e007036fe07)

---

## Domain

My domain is student reviews of Oklahoma Christian University professors, collected from Rate My Professors. This knowledge is valuable because it reflects honest, firsthand student experience of what a professor's class is actually like, things like grading style, teaching approach, and workload, that the official course catalog never tells you. It's hard to find otherwise because it lives scattered across individual review pages, often contradicts itself, and requires reading through many opinions to form an accurate picture.

---

## Document Sources

I treat each individual review as one document, since a single review is the natural self-contained unit of student knowledge. I collected 15 reviews across 3 professors from 3 different departments.

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Paul Howard (Math) — MATH1614, rated 5.0 | Rate My Professors review | ratemyprofessors.com/professor/1666205 |
| 2 | Paul Howard (Math) — MATH1213, rated 5.0 | Rate My Professors review | ratemyprofessors.com/professor/1666205 |
| 3 | Paul Howard (Math) — MATH1623, rated 4.0 | Rate My Professors review | ratemyprofessors.com/professor/1666205 |
| 4 | Paul Howard (Math) — MATH1623, rated 4.0 | Rate My Professors review | ratemyprofessors.com/professor/1666205 |
| 5 | Paul Howard (Math) — MATH1213, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/1666205 |
| 6 | Chris Austin (Physics) — PHYS1114, rated 4.0 | Rate My Professors review | ratemyprofessors.com/professor/1629835 |
| 7 | Chris Austin (Physics) — PHYS1214, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/1629835 |
| 8 | Chris Austin (Physics) — PHYS1214, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/1629835 |
| 9 | Chris Austin (Physics) — PHYS1214, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/1629835 |
| 10 | Chris Austin (Physics) — PHYS1214, rated 5.0 | Rate My Professors review | ratemyprofessors.com/professor/1629835 |
| 11 | Matthew McCook (History) — HIST2213, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/134785 |
| 12 | Matthew McCook (History) — 1223, rated 1.0 | Rate My Professors review | ratemyprofessors.com/professor/134785 |
| 13 | Matthew McCook (History) — US1877, rated 5.0 | Rate My Professors review | ratemyprofessors.com/professor/134785 |
| 14 | Matthew McCook (History) — HIST122301, rated 4.0 | Rate My Professors review | ratemyprofessors.com/professor/134785 |
| 15 | Matthew McCook (History) — FRESHMAN geography, rated 2.0 | Rate My Professors review | ratemyprofessors.com/professor/134785 |

---

## Chunking Strategy

**Chunk size:** One review per chunk (variable length, roughly 20–120 words each). I split each file on the `---` separator between reviews rather than by a fixed character or token count.

**Overlap:** None.

**Why these choices fit your documents:** My documents are individual professor reviews, which are already short and self-contained. Each review is one student's complete opinion, so the natural boundary is the review itself, not an arbitrary character count. Splitting mid-review would break a single coherent opinion across two chunks, and merging multiple reviews into one chunk would blur different students' perspectives, which matters a lot here because reviews for the same professor often contradict each other. Overlap exists to preserve context that gets cut at an arbitrary boundary, but since my boundaries fall cleanly between whole reviews, there's no context to carry over, so overlap would only add noise. Before chunking, I stripped each review down to its text and metadata fields (professor, rating, course, date) so no site boilerplate or HTML made it into the chunks, and I kept that metadata attached to each chunk for source attribution.

**Final chunk count:** 15 chunks.

---

## Sample Chunks

Five representative chunks from the corpus, each as it appears after ingestion and cleaning. The `chunk_id` field is the internal identifier used in ChromaDB.

**Chunk 1** — Source: `PROFESSOR Paul Howard.txt` | MATH1614 | rated 5.0
> He's genuinely such a nice person, and is extremely helpful in person if you have any questions. He can be a little intimidating, but he's great once you realize it's unintentional in any way.

**Chunk 2** — Source: `PROFESSOR Paul Howard.txt` | MATH1213 | rated 1.0
> He did not teach, but expected the students to learn on their own time fully. Often times his math was incorrect or unclear.

**Chunk 3** — Source: `PROFESSOR Chris Austin.txt` | PHYS1214 | rated 1.0
> As a physics class, I expected difficult content and exams, but the exams are worth 75% of your final grade and the averages are in the 50s. He doesn't teach sections of the content covered on exams and expects students to gather resources that are unhelpful for those questions.

**Chunk 4** — Source: `PROFESSOR Chris Austin.txt` | PHYS1214 | rated 5.0
> This class was one of the most difficult courses I have had to take. However, don't be discouraged if you get a few bad grades! If you work hard and improve with each exam, Dr. Austin will consider this. He is very encouraging and wants you to succeed. He is also gracious with curving, especially when he feels like you've earned the grade.

**Chunk 5** — Source: `PROFESSOR Matthew McCook.txt` | HIST2213 | rated 1.0
> He doesn't give many assignments and doesn't believe in study guides for anything. Grades rely heavily on exams and random quizzes. He also does notebook checks for grades, and he has a very lecture-heavy class.

---

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` from sentence-transformers. I chose it because it runs locally with no API key and no rate limits, produces 384-dimensional vectors, and performs well on short text, which fits my review corpus and a class-project budget.

**Production tradeoff reflection:** If I were deploying this for real users and cost wasn't a constraint, I'd weigh a few things. Context length: MiniLM truncates longer inputs, which is fine for short reviews but would limit me if I expanded to long-form guides or syllabi. Multilingual support: MiniLM is English-first, so a multilingual model would matter for a more diverse corpus. Accuracy on domain-specific text: a larger or fine-tuned model might better capture the specific vocabulary students use about classes. Latency and local vs. API: a local model keeps data private and avoids per-call costs but doesn't scale as cleanly as a managed API, while a hosted embedding service scales easily but adds cost and a network dependency. For production I'd likely test a larger hosted model against MiniLM on my own evaluation questions before deciding.

---

## Retrieval Test Results

Three queries run against the vector store before generation was connected. Each shows the top-4 retrieved chunks and their distance scores (lower = more similar).

---

**Query 1:** "What do students say about Professor Howard's teaching style?"

| Rank | Professor | Course | Rating | Distance | Chunk preview |
|------|-----------|--------|--------|----------|---------------|
| 1 | Paul Howard | MATH1213 | 5.0 | 0.28 | "He's very intelligent, and just wants everybody to love math as much as he does…" |
| 2 | Paul Howard | MATH1614 | 5.0 | 0.31 | "He's genuinely such a nice person, and is extremely helpful in person…" |
| 3 | Paul Howard | MATH1213 | 1.0 | 0.41 | "He did not teach, but expected the students to learn on their own time fully…" |
| 4 | Paul Howard | MATH1623 | 4.0 | 0.44 | "He's odd but nice. He tries to explain everything clearly but then rushes…" |

**Why these chunks are relevant:** All four describe Howard's in-class behavior directly — his pace, passion, clarity, and consistency — which maps tightly onto the query. Chunks 1 and 2 supply the positive picture (passionate, caring, helpful by email), chunk 3 the critical counterpoint (didn't teach, math was wrong), and chunk 4 something in between. The retrieval correctly returned only Howard reviews and correctly surfaced both sides of the disagreement.

---

**Query 2:** "How are exams weighted in Professor Austin's physics class?"

| Rank | Professor | Course | Rating | Distance | Chunk preview |
|------|-----------|--------|--------|----------|---------------|
| 1 | Chris Austin | PHYS1214 | 1.0 | 0.352 | "…exams are worth 75% of your final grade and the averages are in the 50s…" |
| 2 | Chris Austin | PHYS1214 | 1.0 | 0.51 | "He never really taught and made you watch videos for the class." |
| 3 | Chris Austin | PHYS1114 | 4.0 | 0.56 | "Seems like a hard class, and is. But if you try in class and do the practice test…" |
| 4 | Chris Austin | PHYS1214 | 1.0 | 0.59 | "He makes you do notes before class so he doesn't have to teach you." |

**Why these chunks are relevant:** Chunk 1 is the strongest match (distance 0.352, the lowest score of any query in this project) because it contains the exact fact being asked: the 75% exam weight and the low class averages. The query's specific language — "exams weighted," "physics class" — aligns tightly with chunk 1's text. Chunks 2–4 are also Austin reviews and correctly returned, but they address teaching format rather than grading percentages, so they score higher distances.

---

**Query 3:** "Does Professor McCook use study guides?"

| Rank | Professor | Course | Rating | Distance | Chunk preview |
|------|-----------|--------|--------|----------|---------------|
| 1 | Matthew McCook | HIST2213 | 1.0 | 0.38 | "He doesn't give many assignments and doesn't believe in study guides for anything…" |
| 2 | Matthew McCook | 1223 | 1.0 | 0.52 | "Rambles and expects you to figure out which of his anecdotes will make their way onto the test." |
| 3 | Matthew McCook | HIST122301 | 4.0 | 0.61 | "So kind. He's a really good professor, it's just a difficult class and an unfortunate subject…" |
| 4 | Matthew McCook | FRESHMAN | 2.0 | 0.64 | "Beware of his geography class. He expects you to know crucial geographical topics for his exams…" |

---

## Grounded Generation

**System prompt grounding instruction:** My system prompt tells the model to answer using only the student reviews provided in the context, and explicitly: do not use outside knowledge; if the context doesn't contain the answer, say you don't have enough information in the reviews and don't make anything up; when reviews disagree, show both sides honestly; and cite the sources you used by their numbers. I also set temperature to 0.2 so the model stays close to the source text instead of inventing plausible-sounding detail.

**How source attribution is surfaced in the response:** Before generation, each retrieved chunk is formatted with a numbered label showing the professor, course, and rating (for example `[1] Chris Austin - PHYS1214 (rated 1.0)`). The model cites those numbers in its answer, and after generation my code also prints a "Retrieved from" list showing every chunk used, with its professor, course, rating, and distance score. So attribution is guaranteed by the program structure, not left entirely to the model.

---

## Example Responses

Two successful responses with inline citations visible, and one out-of-scope query showing the system's refusal.

---

**Response 1 — Query:** "What do students say about Professor Howard's teaching style?"

**Answer:**
Students describe Professor Howard as passionate but sometimes hard to follow. He "just wants everybody to love math as much as he does" and is "super passionate about what he's teaching," but "rambles on and on" and "sometimes talks too fast and is hard to follow" [1]. He is "extremely helpful in person" [2] and responds to emails quickly [1]. One reviewer also notes he "sometimes lets you work in groups on tests and quizzes" [4].

One dissenting review (rated 1.0) states he "did not teach, but expected the students to learn on their own time" and that his math was "often incorrect or unclear" [3]. The majority of reviews lean positive, but students should expect a fast-paced, enthusiastic lecturer.

**Retrieved from:**
- [1] Paul Howard — MATH1213 (rated 5.0, distance 0.280)
- [2] Paul Howard — MATH1614 (rated 5.0, distance 0.310)
- [3] Paul Howard — MATH1213 (rated 1.0, distance 0.410)
- [4] Paul Howard — MATH1623 (rated 4.0, distance 0.440)

---

**Response 2 — Query:** "How are exams weighted in Professor Austin's physics class?"

**Answer:**
According to one student review, exams are worth 75% of the final grade in Professor Austin's PHYS1214 class, and class averages on those exams are in the 50s [1]. The same reviewer notes he "doesn't teach sections of the content covered on exams" and points students to resources that are unhelpful for exam questions [1]. The other retrieved reviews address his teaching approach and class format but do not specify grading percentages [2][3][4].

**Retrieved from:**
- [1] Chris Austin — PHYS1214 (rated 1.0, distance 0.352)
- [2] Chris Austin — PHYS1214 (rated 1.0, distance 0.510)
- [3] Chris Austin — PHYS1114 (rated 4.0, distance 0.560)
- [4] Chris Austin — PHYS1214 (rated 1.0, distance 0.590)

---

**Out-of-scope refusal — Query:** "What dining halls are open late at Oklahoma Christian University?"

**Answer:**
I don't have enough information in the reviews to answer that question. The available reviews cover student experiences with three professors — Paul Howard (Mathematics), Chris Austin (Physics), and Matthew McCook (History) — and none of them mention dining halls or campus facilities.

**Retrieved from:**
- [1] Matthew McCook — US1877 (rated 5.0, distance 0.721)
- [2] Paul Howard — MATH1614 (rated 5.0, distance 0.734)
- [3] Matthew McCook — HIST122301 (rated 4.0, distance 0.751)
- [4] Paul Howard — MATH1623 (rated 4.0, distance 0.762)

---

## Query Interface

**Interface type:** Command-line. Run with `python query.py` from the project root (requires `.env` with `GROQ_API_KEY` set and the ChromaDB store already built via `python embed_store.py`).

**Input:** A plain-text question typed at the `Question:` prompt. The system accepts any natural-language question. Type `quit` or `exit` to stop the session.

**Output:**
- `Answer:` — the LLM-generated response, grounded in the retrieved reviews, with numbered inline citations (`[1]`, `[2]`, etc.) linking claims to specific reviews.
- `Retrieved from:` — the top-4 chunks used, each showing professor name, course code, rating, and semantic distance score.

**Sample interaction transcript:**

```
Question: How are exams weighted in Professor Austin's physics class?

Answer:
According to one student review, exams are worth 75% of the final grade in Professor
Austin's PHYS1214 class, and the class averages on those exams are in the 50s [1].
The same reviewer notes he "doesn't teach sections of the content covered on exams"
and points students to resources that are unhelpful for exam questions [1]. The other
retrieved reviews address his teaching approach and class format but do not specify
grading percentages [2][3][4].

Retrieved from:
  [1] Chris Austin - PHYS1214 (rated 1.0, distance 0.352)
  [2] Chris Austin - PHYS1214 (rated 1.0, distance 0.510)
  [3] Chris Austin - PHYS1114 (rated 4.0, distance 0.560)
  [4] Chris Austin - PHYS1214 (rated 1.0, distance 0.590)

--------------------------------------------------
```

---

## Evaluation Report

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about Professor Howard's teaching style? | Mixed: passionate and caring, but rambles and talks fast | Showed both sides, cited a 1.0 and a 5.0 review, named the conflict | Relevant | Accurate |
| 2 | Is Professor Austin a good teacher? | Reviews are split between 1.0 and 5.0 | Said there is no Professor Austin in the reviews | Off-target | Inaccurate |
| 3 | How are exams weighted in Professor Austin's physics class? | Exams worth 75% of the grade | Correctly reported 75%, cited the right review (distance 0.352) | Relevant | Accurate |
| 4 | Does Professor McCook use study guides? | No, he doesn't believe in them | Correctly answered no, cited the relevant review | Relevant | Accurate |
| 5 | Which professor should I take if I want an easy class? | McCook's US1877, but course-dependent | Recommended McCook US1877, flagged that his other course is hard | Relevant | Accurate |

Result: 4 accurate, 1 inaccurate.

---

## Failure Case Analysis

**Question that failed:** "Is Professor Austin a good teacher?"

**What the system returned:** The system said it didn't have enough information and that there was no Professor Austin in the reviews, even though Austin has 5 reviews in my corpus.

**Root cause (tied to a specific pipeline stage):** This is a retrieval failure, not a generation failure. The top 4 retrieved chunks were two McCook reviews and two Howard reviews, with no Austin review among them. Because generation is correctly grounded, the model saw no Austin content and honestly said it had nothing to go on. The reason retrieval missed is semantic: the phrase "good teacher" matches generic praise found in other reviews (McCook's "really good professor," Howard's positive review) more strongly than it matches Austin's reviews, which are framed around specifics like exam weighting and video lectures rather than the abstract phrase "good teacher." So the generically-positive chunks outranked Austin's and pushed him out of the top 4. I know it's a phrasing issue and not missing data because Question 3, which asked about Austin's exam weighting using specific terms, retrieved his review easily with the lowest distance of any query (0.352).

**What you would change to fix it:** Increase top-k so more candidates make the cut, add metadata filtering so a question naming a professor restricts retrieval to that professor's reviews, or combine semantic search with keyword (BM25) search so the name "Austin" gets matched directly instead of only semantically.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the Chunking Strategy section in planning.md before I wrote any code forced me to decide that one review equals one chunk. That single decision made ingestion simple to build and easy to defend, and it's the reason my source citations work cleanly, because each chunk maps to exactly one review with its own metadata attached. Having that settled up front meant I wasn't second-guessing chunk boundaries while coding.

**One way your implementation diverged from the spec, and why:** My planning assumed retrieval would reliably surface the right professor whenever one was named in the question. In practice, the Austin question showed that semantic search can rank generic praise above the specifically-named professor's reviews. I didn't change my chunking strategy to fix this before the deadline, but I documented it as my failure case and identified metadata filtering as the real fix, which I'd implement next.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* I described my plan to reuse a TF-IDF and Groq setup from a previous project for retrieval.
- *What it produced:* It flagged that TF-IDF is keyword matching, not semantic search, so it wouldn't satisfy the rubric's requirement for semantic similarity or the embedding-model reflection. It recommended switching to all-MiniLM-L6-v2 embeddings with ChromaDB while keeping Groq for generation.
- *What I changed or overrode:* I took the direction and dropped TF-IDF for MiniLM + ChromaDB, but kept Groq for the generation step like I originally planned.

**Instance 2**

- *What I gave the AI:* My Chunking Strategy section plus a sample of my review file format, and asked it to implement the ingestion and chunking script.
- *What it produced:* A parser that splits each file on the `---` separator, pulls out the metadata fields, and returns a list of chunks with metadata attached.
- *What I changed or overrode:* I reviewed the code, confirmed it returned exactly 15 chunks, and spot-checked the metadata against the original reviews before using it. I also directed it to print distance scores in the retrieval output so I could judge retrieval quality for this evaluation report.