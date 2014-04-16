#!/bin/sh
cd memtest86+-4.20/
make clean
rm *Case*
make
cp memtest.bin ~/../../media/A15D-2FA8/memtest
rm *Case*
cd ../
