#!/bin/bash
# input_file = $1
echo "Modifing text file to desired format...."
python3 remove_accent.py  "$1" "$2-no-accent"
bash /home/labic-redbull/.julia/v0.5/AdaGram/utils/tokenize.sh "$2-no-accent" "$2-clean"
echo "Done!"
echo "Creating a dictionary...."
bash /home/labic-redbull/.julia/v0.5/AdaGram/utils/dictionary.sh "$2-clean" "$2-dictionary"
echo "Done!"
echo "Creating model...."
bash /home/labic-redbull/.julia/v0.5/AdaGram/train.sh --window 5 --remove-top-k 10 --dim 100 --prototypes 10 --alpha 0.1 --d 0 --subsample 0.5 --epochs 1 --stopwords stopwords.txt "$2-clean" "$2-dictionary" "$2-trained"

echo "Done!"

