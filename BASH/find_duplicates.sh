#!/bin/bash

# Find all files and their checksums and sizes
find . -type f -exec bash -c 'printf "%s %s %s\n" "$(md5sum {})" "$(stat -c%s {})" "{}"' \; | \

# Sort by checksum and size, then find duplicates
sort -k1,2 | uniq -D -f 2 | \

# Save duplicates to duplo.txt
tee duplo.txt | \

# Extract filenames from the output and remove the leading './'
cut -d' ' -f3- | sed 's|^\./||' > duplicates.txt

# Prompt user for confirmation
read -p "Do you want to delete the duplicates? (Yes/No): " answer

# Convert answer to lowercase for case-insensitive comparison (using tr)
answer=$(echo "$answer" | tr '[:upper:]' '[:lower:]')

# Use case statement for comparison (more portable than [[ ... ]])
case "$answer" in
    yes|y)
        # Delete duplicates
        xargs rm -f < duplicates.txt
        echo "Duplicates deleted."
        ;;
    no|n)
        echo "Duplicates saved to duplo.txt."
        ;;
    *)
        echo "Invalid input. Please answer Yes or No."
        ;;
esac
