#!/bin/sh

mkdir -p $2

echo "Copying dependencies for the binary/library $1..."
deps=$(ldd $1 | awk 'BEGIN{ORS=" "}$1\
~/^\//{print $1}$3~/^\//{print $3}'\
 | sed 's/,$/\n/')

#Copy the deps
for dep in $deps
do
    cp $dep $2
done