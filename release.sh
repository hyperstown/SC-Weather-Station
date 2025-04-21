#!/bin/bash

#output_filename="release_$(date +%Y-%m-%d_%H,%M).tar.gz"
output_filename="release.tar.gz"

files_and_folders=("src" "server")

tar -czvf "$output_filename" "${files_and_folders[@]}"

echo "Archive created: $output_filename"
