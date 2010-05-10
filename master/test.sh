#!/bin/sh
while true; do
    pushing
    git checkout master
    ./run_game.py -full -nosound
    git checkout experimental
    ./run_game.py -full -nosound
    echo "##############################"
    sleep 5
done
