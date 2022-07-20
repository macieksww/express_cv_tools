for filename in *.pdf; do
echo ________________________ $filename _________________________________
  pdf2txt.py "$filename" | sed s/\(cid\:[0-9]*\)//g
done
