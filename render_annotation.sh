#! /bin/sh
input='./annotation.md'
output='/tmp/juggling_detector_annotation.html'
from='markdown+fenced_code_blocks+fenced_code_attributes'
pandoc --from $from\
       --to html\
       --highlight-style breezedark\
       --standalone\
       --metadata=title:"Juggling Detector Annotation"\
       $pandoc_options\
       -o $output\
       $input
echo "$output"
