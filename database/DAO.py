from database.DB_connect import DBConnect
from model.constructor import Constructor


class DAO():
    @staticmethod
    def getNodi():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query = """SELECT * 
                    from constructors"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(Constructor(**row))

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getDizionario(v1, v2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select r1.constructorId, r1.raceId, r1.driverId, r1.position
from races r, results r1
where r.raceId = r1.raceId and year between %s and %s
group by r1.constructorId, r1.raceId, r1.driverId, r1.position
"""
        cursor.execute(query, [v1, v2])

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getArchi(v1, v2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """with pesi as (select r1.constructorId, count(*) as peso
from races r, results r1 
where r.raceId = r1.raceId and year between %s and %s
and position is not null
group by r1.constructorId having count(*) >0)

select  p1.constructorId, p2.constructorId, max(p1.peso+p2.peso)
from pesi p1, pesi p2
where p1.constructorId>p2.constructorId
group by p1.constructorId, p2.constructorId"""
        cursor.execute(query, [v1, v2])

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getIntersezioni(v1, v2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """with pesi as (select r1.constructorId, count(*) as peso
from races r, results r1 
where r.raceId = r1.raceId and year between %s and %s
and position is not null
group by r1.constructorId having count(*) >0), 
top as (
select  p1.constructorId primo, p2.constructorId secondo, max(p1.peso+p2.peso) as tot
from pesi p1, pesi p2
where p1.constructorId>p2.constructorId
group by p1.constructorId, p2.constructorId), 
tabella as (
select primo, max(tot) as max
from top
group by primo
union 
select secondo as primo, max(tot) as max
from top
group by secondo)

select primo, max(max)
from tabella
group by primo"""
        cursor.execute(query, [v1, v2])

        res = {}
        for row in cursor:
            el = list(row)
            res[el[0]] = el[1]

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getAnni():
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select distinct year
        from races
        order by year desc"""
        cursor.execute(query)

        res = []
        for row in cursor:
            res.append(row)

        cursor.close()
        cnx.close()
        return res

    @staticmethod
    def getM(v1, v2):
        cnx = DBConnect.get_connection()
        cursor = cnx.cursor()
        query = """select constructorId, count(distinct year)
from results r, races r1 
where r.raceId = r1.raceId 
and year between %s and %s
group by constructorId"""
        cursor.execute(query, [v1, v2])

        res = {}
        for row in cursor:
            el = list(row)
            res[el[0]] = el[1]

        cursor.close()
        cnx.close()
        return res

