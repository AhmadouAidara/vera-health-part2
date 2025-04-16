import pandas as pd

def load_journals(filepath: str) -> pd.DataFrame:
    with open(filepath, "r", encoding="utf-8") as f:
        lines = f.readlines()

    journal_lines = [line.strip() for line in lines if ":" in line and "{" not in line and "}" not in line]
    journal_entries = []
    current_entry = {}

    for line in journal_lines:
        if line.startswith("Journal:"):
            if current_entry:
                journal_entries.append(current_entry)
                current_entry = {}
            current_entry["journal"] = line.split(":", 1)[1].strip().strip('",')
        elif line.startswith("SJR:"):
            sjr_raw = line.split(":", 1)[1].strip().strip('",')
            try:
                current_entry["sjr"] = float(sjr_raw)
            except ValueError:
                current_entry["sjr"] = None
        elif line.startswith("Quartile:"):
            current_entry["quartile"] = line.split(":", 1)[1].strip().strip('",')

    if current_entry:
        journal_entries.append(current_entry)

    return pd.DataFrame(journal_entries)


def merge_journal_metadata(documents, journal_df):
    updated_docs = []
    for doc in documents:
        doc_journal = getattr(doc, "journal", "").strip().lower()
        match = journal_df[journal_df["journal"].str.lower() == str(doc_journal)]
        if not match.empty:
            doc.metadata["sjr"] = match.iloc[0]["sjr"]
            doc.metadata["quartile"] = match.iloc[0]["quartile"]
        else:
            doc.metadata["sjr"] = None
            doc.metadata["quartile"] = None
        updated_docs.append(doc)
    return updated_docs