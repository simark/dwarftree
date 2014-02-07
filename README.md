# dwarftree

A visual, tree-based, DWARF explorer. It uses [pyelftools](https://github.com/eliben/pyelftools).

## What do I do ?

If you have a recent compiler, it might user DWARF 4. At least, this is the case with gcc 4.8.2-10ubuntu2. pyelftools doesn't seem to support it yet, so make sure to compile with DWARF 3.

    gcc -gdwarf-3 test.c
    
Then, open dwarftree.

    python3 dwarftree.py
    
Finally, you can use the superior input device (AKA the mouse ;) to open up `a.out`.

## Dependencies

* Python 3
* pyelftools
  * `sudo pip3 install pyelftools`
* PyGObject / PyGI
  * Debian/Ubuntu: `python3-gi` package
  * Fedora: `pygobject3` package
  
## Screenshot
![Screenshot](http://nova.polymtl.ca/~simark/ss/tmp.EwQc8kcem0.png)
