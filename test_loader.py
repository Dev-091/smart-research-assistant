from loaders.pdf_loader import load_pdf

# Path to the sample PDF
pdf_path = "data/raw/sample.pdf"

# Load the PDF
documents = load_pdf(pdf_path)

# Print basic information
print(f"Number of pages: {len(documents)}")

print("-" * 50)

# Print first page content
#print(documents[0].page_content)

print("-" * 50)

# Print metadata
#print(documents[0].metadata)

print(type(documents))

print(type(documents[0]))

print(dir(documents[0]))