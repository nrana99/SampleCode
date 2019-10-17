# SampleCode
Nadims coding test. Programs are written in Python 3.7

Steps to run the program with a single client. Repeat step 2 in separate process to spawn multiple parallel clients.

python Nadim_Server.py
python Nadim_Client.py

NOTES
======

o MyDict is a dictionary which will hold key,value pairs where key = input digits and value = count of occurences for this key.

o Unique_Values is a SET data type since set data type retains uniqueness. The data structure is merely used to display that SET 
  can also be used here. Since the original problem statement required me to also display statistics, SET data type will lose the
  statistics collection. I am commenting out the SET operation on line 199.

o File will be written out when client sends in "terminate" message

o A separate book-keeping thread is spawned and runs that displays statistics every 10 seconds (original requirement)

o Since accept() is a blocking call, I am spawning a master thread which will listen to the client and then spawns worker client threads

o Initially I used list with NOT IN operator everytime I appeneded to the list but that was expensive. I implemented the solution
  using dictionary since dictionary implements hash table and extremely fast in searching for duplicate values

