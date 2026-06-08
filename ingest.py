"""
ingest.py
Document ingestion + chunking for The Unofficial Guide RAG project.

Reads professor-review .txt files, splits each file on the '---' separator
(one review = one chunk, no overlap), and parses the metadata + review text
into structured chunks ready for embedding.

Matches the planning.md spec:
  - Domain: OC professor reviews from Rate My Professors
  - Chunking Strategy: one review per chunk, split on '---', no overlap
"""

from pathlib import Path

# Folder where your 3 .txt files live (howard.txt, austin.txt, mccook.txt).
# Change this if your files are somewhere else.
DATA_DIR = Path("data")


def parse_block(block: str) -> dict:
    """
    Turn one text block (either the file header or a single review)
    into a dictionary of FIELD: value pairs.

    Each line looks like 'RATING: 5.0', so we split on the first ':' only.
    """
    fields = {}
    for line in block.strip().splitlines():
        if ":" in line:
            key, value = line.split(":", 1)  # split on first colon only
            fields[key.strip().upper()] = value.strip()
    return fields


def load_file(path: Path) -> list[dict]:
    """
    Load one .txt file and return a list of chunk dicts.

    File structure:
        <header block>
        ---
        <review 1>
        ---
        <review 2>
        ---
        ...

    The header (PROFESSOR, DEPARTMENT, SCHOOL, SOURCE) applies to every
    review in that file, so we parse it once and attach it to each chunk.
    """
    raw = path.read_text(encoding="utf-8")

    # Split the whole file on the separator.
    # First piece = header, every piece after = one review.
    parts = [p for p in raw.split("---") if p.strip()]

    header = parse_block(parts[0])  # PROFESSOR / DEPARTMENT / SCHOOL / SOURCE
    review_blocks = parts[1:]  # the actual reviews

    chunks = []
    for i, block in enumerate(review_blocks):
        review = parse_block(block)

        # The text we'll actually embed and show is the REVIEW field.
        text = review.get("REVIEW", "").strip()
        if not text:
            continue  # skip any empty/malformed block

        # Metadata travels WITH the chunk so retrieval can cite the source.
        metadata = {
            "professor": header.get("PROFESSOR", "unknown"),
            "department": header.get("DEPARTMENT", "unknown"),
            "school": header.get("SCHOOL", "unknown"),
            "source": header.get("SOURCE", "unknown"),
            "rating": review.get("RATING", "unknown"),
            "difficulty": review.get("DIFFICULTY", "unknown"),
            "date": review.get("DATE", "unknown"),
            "course": review.get("COURSE", "unknown"),
            "grade": review.get("GRADE", "unknown"),
            "would_take_again": review.get("WOULD_TAKE_AGAIN", "unknown"),
            # a stable id so you can trace a chunk back to its file + position
            "chunk_id": f"{path.stem}_{i + 1}",
        }

        chunks.append({"text": text, "metadata": metadata})

    return chunks


def load_all(data_dir: Path = DATA_DIR) -> list[dict]:
    """Load every .txt file in the data folder and return all chunks combined."""
    all_chunks = []
    for path in sorted(data_dir.glob("*.txt")):
        file_chunks = load_file(path)
        print(f"  {path.name}: {len(file_chunks)} reviews")
        all_chunks.extend(file_chunks)
    return all_chunks


if __name__ == "__main__":
    print("Loading documents...")
    chunks = load_all()

    print(f"\nTotal chunks: {len(chunks)}")

    # Spot-check: print the first chunk so you can confirm parsing worked.
    if chunks:
        first = chunks[0]
        print("\nFirst chunk preview:")
        print("  text:    ", first["text"][:80], "...")
        print("  prof:    ", first["metadata"]["professor"])
        print("  course:  ", first["metadata"]["course"])
        print("  rating:  ", first["metadata"]["rating"])
        print("  chunk_id:", first["metadata"]["chunk_id"])
