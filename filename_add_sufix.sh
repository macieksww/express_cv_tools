for file in *.txt; do
    mv "$file" "${file%.txt}_z.txt"
done

for file in *.odt; do
    mv "$file" "${file%.odt}_z.odt"
done

for file in *.jpg; do
    mv "$file" "${file%.jpg}_z.jpg"
done

for file in *.docx; do
    mv "$file" "${file%.docx}_z.docx"
done

for file in *.doc; do
    mv "$file" "${file%.doc}_z.doc"
done

for file in *.pdf; do
    mv "$file" "${file%.pdf}_z.pdf"
done
