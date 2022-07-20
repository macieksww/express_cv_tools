# docx to txt
for filename in *.docx; do
filename_base=$(echo "$filename" | cut -f 1 -d '.')
echo __________ $filename $filename_base _____________________
docx2txt "$filename"
done

# doc to txt

for filename in *.doc; do
filename_base=$(echo "$filename" | cut -f 1 -d '.')
echo __________ $filename $filename_base _____________________
catdoc "$filename" > "${filename_base}.txt"
done

# odt to txt

for filename in *.odt; do
filename_base=$(echo "$filename" | cut -f 1 -d '.')
echo __________ $filename $filename_base _____________________
odt2txt --output="${filename_base}.txt" "$filename" 
done
