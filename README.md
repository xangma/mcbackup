# mcbackup
python script to run and backup minecraft server

Some other notes:

- Lines 38 and 39 are where the maximum number of backups can be set. Currently it's set at 24. When it saves a new one it gets rid of the oldest one.

- As for Task Scheduling thing, I back up to a mapped network drive which is apparently difficult with the Task Scheduler. You have to use UNC paths (\\sharename\folder) and ...

Set the action to be start a program:
C:\Windows\System32\cmd.exe

with the arguments:

/c C:\Pathtopython\python.exe C:\pathtoscript\mcbackup.py

starting in:

C:\pathtoserverfolder\

This setup allows the backups to be put on a network drive.
