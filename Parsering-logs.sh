#!/usr/bin/env bash
LOG_FILE="/Users/victoriayaakov/Documents/Repos/DevOps/access-log.log"
# Per IP
cut -d ' ' -f1 access-log.log | sort -n | uniq -c | sort -nr | head -20 > "access-log.log.2"
cat access-log.log.2
rm access-log.log.2
# Per Date

grep -Eo '[0-9]{1,2}/[A-Za-z]{3}/[0-9]{4}' $LOG_FILE | sort | uniq -c | sort -nr > access-log.log.3
# # Display the formatted log file
cat access-log.log.3
rm access-log.log.3


