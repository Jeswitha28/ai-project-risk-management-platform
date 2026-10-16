from ingestion.docx_parser import parse_docx

doc = parse_docx("data/sample_docs/sample_meeting_notes.docx")

print("File:", doc.filename)
print("Type:", doc.file_type)
print("Characters:", len(doc.text))
print("---")
print(doc.text)