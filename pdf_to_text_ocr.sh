for filename in *.pdf; do
filename_base=$(echo "$filename" | cut -f 1 -d '.')
echo __________ $filename $filename_base _____________________
  convert -density 400 "$filename" -resize 300% "img/${filename_base}_image.png"
echo > "txt/${filename_base}.txt"
for imagename in "img/${filename_base}"_imag*.png; do
  imagename_base=$(echo "$imagename" | cut -f 1 -d '.')
echo $imagename $imagename_base
  # ~/programy/tesseract/install/bin/tesseract "$imagename" "$imagename_base" -l pol
  /usr/bin/tesseract "$imagename" "$imagename_base" -l pol
  cat "${imagename_base}.txt" >> "txt/${filename_base}.txt"
  rm "${imagename_base}.txt"
done
done
