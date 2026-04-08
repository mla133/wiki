#! /usr/bin/env bash
cd ~/.todo
echo >> note.txt
date >> note.txt
if [[ $# -ne 0 ]]; then
	echo $@ >> note.txt
fi
vim "+normal Go" +startinsert note.txt
