from loaders.pdf_loader import load_pdf
from splitters.text_splitter import split_documents

documents = load_pdf("data/raw/sample.pdf")

chunks = split_documents(documents)

print(f"Total Pages : {len(documents)}")
print(f"Total Chunks : {len(chunks)}")

print("\n" + "="*80)

for i in range(3):
    print(f"\nCHUNK {i+1}")
    print("-"*80)

    print(chunks[i].page_content)

    print("\nLength :", len(chunks[i].page_content))

    print("\nMetadata :", chunks[i].metadata)

    print("\n" + "="*80)