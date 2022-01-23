import sqlite3, random, tkinter

isDump = False

class command:
    # constructor method
    def __init__(self, sql_command_parm):
        self.sql_command = sql_command_parm

    # str representation returned
    def __str__(self):
        return self.sql_command


class query:
    num = 1

    def __init__(self, menu_option, menu_command):
        self.menu_option = menu_option
        self.menu_command = menu_command
        self.key = str(query.num)
        query.num += 1

    def __str__(self):
        return "Question:{menu_option} Command:{menu_command}".format(menu_option=self.menu_option,
                                                                      menu_command=self.menu_command)

    def run_query(self, curr, dump=False):
        try:
            summary = ""
            headers = []
            for i in curr.execute(self.menu_command).description:
                headers.append(i[0])
            for i in headers:
                summary += i + ","
            summary = summary[:-1] + "\n"
            for i in curr.execute(self.menu_command).fetchall():
                for j in i:
                    summary += str(j) + ","
                summary = summary[:-1] + "\n"
            if dump:
                f = open("dump.csv", "w")
                f.write(summary)
                f.close()
            else:
                return (summary)
        except Exception as e:
            print(e)


numberOfDeathsEachYear = """--Number of deaths in each year, from max number to minimum
                        select year, count(*) as "Number of deaths" from deathInfo
                        group by year 
                        order by "Number of deaths" desc;
                    """

kingdomVsKingdom = """--Which kingdom won or lost with which kingdom on which battle
select bs.battleName, attacker1 as won, defender1 as lost
from BattleSide bs
NATURAL join 
Battle b
JOIN
outcome o
on bs.battleName = b.battleName and b.battleNumber = o.battleNumber and o.attackOutcome="win"

UNION

select bs.battleName, defender1 as won, attacker1 as lost
from BattleSide bs
NATURAL join 
Battle b
JOIN
outcome o
on bs.battleName = b.battleName and b.battleNumber = o.battleNumber and o.attackOutcome="loss";"""

maxNoble = """--Which house has the max number of noble people
Select allegiance, count(*) as count_nobel from person
group by allegiance
having person.nobility=1 and allegiance != "None"
order by count(*) DESC
limit 1;
"""
kingdomMaxWin = """--4which kingdom has the most wins

select "Kingdom", sum(countWins) as numberOfWins from (
select attacker1 as "Kingdom", count(*) as countWins
from outcome o
JOIN
BattleSide bs
JOIN
Battle b
on
o.attackOutcome = "win" and bs.battleName = b.battleName and o.battleNumber = b.battleNumber
group by attacker1

UNION

select defender1 as "Kingdom", count(*)
from outcome o
JOIN
BattleSide bs
JOIN
Battle b
on
o.attackOutcome = "loss" and bs.battleName = b.battleName and o.battleNumber = b.battleNumber
group by defender1

order by count(*) DESC)

group by "Kingdom"
order by sum(countWins) desc 
limit 1
;
"""
deathNumKingdom = """--how many died from each kingdom

select allegiance, count(*) as numDeaths
from Person
JOIN
deathInfo
on Person.PersonName = deathInfo.PersonName

group by allegiance
order by numDeaths desc;

"""
deadKings = """--All the kings who died

select DISTINCT(King) as "Dead King"
from (
select battleName, attackerKing as "King"
from KingOfAttacker
join 
deathInfo
on KingOfAttacker.attackerKing = deathInfo.PersonName

UNION

select battleName, defenderKing as "King"
from kingOfDefender
join 
deathInfo
on kingOfDefender.defenderKing = deathInfo.PersonName);

"""
commanderVsNum = """--Number  of Commanders vs Number of battles won

select numCommander, count(*) as numBattleWins
from (
Select b.battleName, count(attackercommander) as numCommander

FROM
Battle b
JOIN
outcome o
JOIN
CommanderWhoAttacked c

on
b.battleName = c.BattleName and o.battleNumber = b.battleNumber and o.attackOutcome="win"
group by b.battleName
UNION

Select b.battleName, count(defenderCommander) as numCommander

FROM
Battle b
JOIN
outcome o
JOIN
CommanderWhoDefend c

on
b.battleName = c.BattleName and o.battleNumber = b.battleNumber and o.attackOutcome="loss"
group by b.battleName)
group by numCommander
order by numCommander;

"""
allWinterBattles = """--All the battles that happend in winter
select b.battleNumber,battleName
from 
battle  b
join 
BattleArea ba
on b.battleNumber = ba.battleNumber and ba.summer=0;
"""
allSummerBattles = """--All the battles that happend in summer
select b.battleNumber,battleName
from 
battle  b
join 
BattleArea ba
on b.battleNumber = ba.battleNumber and ba.summer=1;
"""
battlesWonByBattleType = """--Number of battles won by each battle typeof
select count(*) as "Battles Won", battleType from BattleSide  JOIN Battle on BattleSide.battleName = Battle.battleName 
JOIN outcome on outcome.battleNumber = Battle.battleNumber GROUP by battleType HAVING outcome.attackOutcome = 'win'
order by "Battles Won" DESC;"""

class menu:
    def __init__(self):
        self.options = []

    def add_option(self, query_obj):
        self.options.append(query_obj)

    def __str__(self):
        summary = ""
        for i in self.options:
            summary += str(i.key) + ". " + i.menu_option + "\n"
        return summary

    def run_query(self, key, cur, dump=False):
        found = None
        for i in self.options:
            if i.key == key:
                found = i
                return found.run_query(cur, dump)
        return found


con = sqlite3.connect("data.db")
con.execute("PRAGMA foreign_keys = 1")
cur = con.cursor()
temp_menu = menu()

q1 = query("Number of deaths in each year, from max number to minimum?", numberOfDeathsEachYear)
temp_menu.add_option(q1)
q2 = query("Which kingdom won or lost with which kingdom on which battle?", kingdomVsKingdom)
temp_menu.add_option(q2)
q3 = query("Which house has the max number of noble people?", maxNoble)
temp_menu.add_option(q3)
q4 = query("which kingdom has the most wins?", kingdomMaxWin)
temp_menu.add_option(q4)
q5 = query("how many died from each kingdom?", deathNumKingdom)
temp_menu.add_option(q5)
q6 = query("All the kings who died?", deadKings)
temp_menu.add_option(q6)
q7 = query("Number of Commanders vs Number of battles won?", commanderVsNum)
temp_menu.add_option(q7)
q8 = query("Which battles happened in Winter?", allWinterBattles)
temp_menu.add_option(q8)
q9 = query("Which battles happened in Summer?", allSummerBattles)
temp_menu.add_option(q9)
q10 = query("Number of battles won by each battle type?", battlesWonByBattleType)
temp_menu.add_option(q10)

window = None


def main():
    try:
        global cur
        global window
        # connecting to the database


        # test command


        # turn off print

    #     Menu window and options
        window = tkinter.Tk()
        window.geometry("600x600")

        buttons = []
        button1 = tkinter.Button(window, text=q1.menu_option, command= query1)
        buttons.append(button1)

        button2 = tkinter.Button(window, text=q2.menu_option, command=query2)
        buttons.append(button2)

        button3 = tkinter.Button(window, text=q3.menu_option, command=query3)
        buttons.append(button3)

        button4 = tkinter.Button(window, text=q4.menu_option, command=query4)
        buttons.append(button4)

        button5 = tkinter.Button(window, text=q5.menu_option, command=query5)
        buttons.append(button5)

        button6 = tkinter.Button(window, text=q6.menu_option, command=query6)
        buttons.append(button6)

        button7 = tkinter.Button(window, text=q7.menu_option, command=query7)
        buttons.append(button7)

        button8 = tkinter.Button(window, text=q8.menu_option, command=query8)
        buttons.append(button8)

        button9 = tkinter.Button(window, text=q9.menu_option, command=query9)
        buttons.append(button9)

        button10 = tkinter.Button(window, text=q10.menu_option, command=query10)
        buttons.append(button10)

        dumpButton = tkinter.Button(window,bg="pink", text="Do you want output in csv File, click Here...", command=dump)
        buttons.append(dumpButton)

        printButton = tkinter.Button(window, bg="pink",text="Do you want to Print Here, click Here...", command=printLabel)
        buttons.append(printButton)


        for i in buttons:
            i.pack()

        window.mainloop()

    except Exception as error:
        print(error)

printL = None

def dump():
    global isDump
    isDump = True

def printLabel():
    global isDump
    isDump = False

def query1():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q1.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q1.run_query(cur, False))
        printL.pack()


def query2():
    global printL
    if printL != None:
        printL.destroy()
        printL = None
    if isDump:
        q2.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q2.run_query(cur, False))
        printL.pack()

def query3():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q3.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q3.run_query(cur, False))
        printL.pack()

def query4():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q4.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q4.run_query(cur, False))
        printL.pack()

def query5():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q5.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q5.run_query(cur, False))
        printL.pack()

def query6():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q6.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q6.run_query(cur, False))
        printL.pack()

def query7():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q7.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q7.run_query(cur, False))
        printL.pack()

def query8():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q8.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q8.run_query(cur, False))
        printL.pack()


def query9():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q9.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q9.run_query(cur, False))
        printL.pack()

def query10():
    global printL
    if printL != None:
        printL.pack_forget()
        printL = None
    if isDump:
        q10.run_query(cur, True)
    else:
        printL = tkinter.Label(window, text = q10.run_query(cur, False))
        printL.pack()


main()