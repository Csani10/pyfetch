#!/usr/bin/env bash
# show-256-colors.sh – print all 256 ANSI colours with their IDs

echo "256-colour palette"
echo "=================="

# foreground colours 0-255
for i in {0..255}; do
  printf "\033[38;5;%sm%3s\033[0m " "$i" "$i"
  # 16 columns → newline every 16th swatch
  (( (i+1) % 16 == 0 )) && echo
done

echo
echo "Done."
