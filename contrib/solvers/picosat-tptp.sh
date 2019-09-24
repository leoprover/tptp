#!/bin/sh
picosat "$@" |
(read result;
case "$result" in
    "s SATISFIABLE") echo "% SZS output start"; cat; echo "% SZS output end"; echo "% SZS status Satisfiable";exit 0;;
    "s UNSATISFIABLE") echo "% SZS status Unsatisfiable";exit 0;;
esac; cat;)
