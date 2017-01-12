#WHOSTAT : A tool for analyze the log produced by who.sh.

Author: Zhichuang Sun
Date: Dec, 2015

### Introduction

who.sh is a shell scirpt that deployed on a shared server that stat who has been on server for what time.
The output of this tool looks like follow:

```
Name: alice

Total time on server: 100.5 hours

time in a day:  3.5  hours

date1:

	1.0--2.5

	18.0--20.0

time in a day:  3.5  hours

date2:
	1.0--2.5

	18.0--20.0

...
```
Appendix I: who.sh

```shellscript
while 1
do
who	>> ~/tmp/whostat.txt
sleep 30*3600 # every half an hour, adjustable
date	>> ~/tmp/whostat.txt
echo "" >> ~/tmp/whostat.txt
done
```
