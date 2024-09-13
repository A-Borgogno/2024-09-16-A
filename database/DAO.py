from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_edges(idMap):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * from neighbor n """
            cursor.execute(query)

            for row in cursor:
                if row["state1"] in idMap and row["state2"] in idMap:
                    s1 = idMap[row["state1"]]
                    s2 = idMap[row["state2"]]
                    if s1.Nshape is None:
                        s1.Nshape = 0
                    if s2.Nshape is None:
                        s2.Nshape = 0
                    peso = s1.Nshape+s2.Nshape
                    if s1.Nall > s2.Nall:
                        result.append((s1, s2, peso))
                    else:
                        result.append((s2, s1, peso))

            result = list(dict.fromkeys(result))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(row["id"],
                          row["Name"],
                          row["Capital"],
                          row["Lat"],
                          row["Lng"],
                          row["Area"],
                          row["Population"],
                          row["Neighbors"]))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(datetime) as anno 
                    FROM sighting s 
                    ORDER BY anno DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes_year(anno: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT  sig.shape s
                        FROM sighting sig
                        WHERE YEAR(sig.datetime)= %s
                        and sig.shape  != ""
                        ORDER BY s asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["s"])

            cursor.close()
            cnx.close()
        return result


    @staticmethod
    def get_nodes(year: int, shape: str):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select t1.*, t2.Nshape
                        from (SELECT s.*, count(*) as Nall
                                FROM state s , sighting s2 
                                where s2.state = s.id 
                                and YEAR(s2.`datetime`) = %s
                                GROUP by s.id) t1 
                        left join 
                        (SELECT s.*, count(*) as Nshape
                                FROM state s , sighting s2 
                                where s2.state = s.id 
                                and YEAR(s2.`datetime`) = %s
                                and s2.shape = %s
                                GROUP by s.id) t2
                        on t1.id = t2.id"""
            cursor.execute(query, (year, year, shape))

            for row in cursor:
                result.append(State(**row))

            cursor.close()
            cnx.close()
        return result
