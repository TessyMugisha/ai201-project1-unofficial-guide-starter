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

## Embedding Model

**Model used:** `all-MiniLM-L6-v2` from sentence-transformers. I chose it because it runs locally with no API key and no rate limits, produces 384-dimensional vectors, and performs well on short text, which fits my review corpus and a class-project budget.

**Production tradeoff reflection:** If I were deploying this for real users and cost wasn't a constraint, I'd weigh a few things. Context length: MiniLM truncates longer inputs, which is fine for short reviews but would limit me if I expanded to long-form guides or syllabi. Multilingual support: MiniLM is English-first, so a multilingual model would matter for a more diverse corpus. Accuracy on domain-specific text: a larger or fine-tuned model might better capture the specific vocabulary students use about classes. Latency and local vs. API: a local model keeps data private and avoids per-call costs but doesn't scale as cleanly as a managed API, while a hosted embedding service scales easily but adds cost and a network dependency. For production I'd likely test a larger hosted model against MiniLM on my own evaluation questions before deciding.

---

## Grounded Generation

**System prompt grounding instruction:** My system prompt tells the model to answer using only the student reviews provided in the context, and explicitly: do not use outside knowledge; if the context doesn't contain the answer, say you don't have enough information in the reviews and don't make anything up; when reviews disagree, show both sides honestly; and cite the sources you used by their numbers. I also set temperature to 0.2 so the model stays close to the source text instead of inventing plausible-sounding detail.

**How source attribution is surfaced in the response:** Before generation, each retrieved chunk is formatted with a numbered label showing the professor, course, and rating (for example `[1] Chris Austin - PHYS1214 (rated 1.0)`). The model cites those numbers in its answer, and after generation my code also prints a "Retrieved from" list showing every chunk used, with its professor, course, rating, and distance score. So attribution is guaranteed by the program structure, not left entirely to the model.

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