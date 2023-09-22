# GameOFthrones

Group Paricipants:

Rayan Imran
Aakash Chouhan
Vedant Pulahru


- Data Source
We were running the pyton file on Anaconda environment

https://www.kaggle.com/mylesoneill/game-of-thrones

battles.csv

character-deaths.csv

- A summary of data:

. The data was chosen as it had interesting relations within our game of thrones database model. where different kingdom battled each other and many fascinating relations were made.

. It consist of commanders, king, characters info and the relations include of the location of battle and how they are fought between defender and attackers.

. character death file has 917 rows and battles file has 38 records

- Discussion in data model

. The data had many null values and did not made any relation sense between them, those columns were broken down. Two different tables were combined so those columns were deleted which were not required in the combination. Moreover, the multivalued table had to be broken down with the help of python using split, so that it appears appropriately in the database.

- Summary of the database
1, Battle (cardinality: 38, arity=3)
2, BattleArea (cardinality: 38, arity=4)
3, BattleSide (cardinality: 38, arity=8)
4, CommanderWhoAttacked (cardinality: 80, arity=2)
5, CommanderWhoDefend (cardinality: 67, arity=2)
6, KingOfAttacker (cardinality: 38, arity=2)
7, Person (cardinality: 917, arity=4)
8, deathInfo (cardinality: 305, arity=2)
9, kingOfDefender (cardinality: 38, arity=2)
10,outcome   (cardinality: 37, arity=4)

