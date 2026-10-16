from ingestion.pdf_parser import parse_pdf

doc = parse_pdf("data/sample_docs/sample_proposal.pdf")

print("File:", doc.filename)
print("Pages:", doc.page_count)
print("Characters:", len(doc.text))
print("---")
print(doc.text[:500])
