## What is digits_to_png? ##
digits_to_png is a script and a package to convert digits to png image, with user specified spacing between digits.
digits_to_png runs with python3 in Linux.

## Packages Needed ##
mnist
png
random
numpy
time
sys

## Usage ##
You can excute it directly in the shell:

$$ python ./digits_to_png.py

or import the package to your python script:

from digits_to_png import digits_to_png
d_to_p = digits_to_png()
digits = [0,1,2]
spacing = 10
result,errmsg,filepath = d_to_p.produce_image(digits,spacing)
print(errmsg)
print(filepath)

