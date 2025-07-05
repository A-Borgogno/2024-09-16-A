from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


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
                    State(**row))

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
    def getShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct(shape) as shape
                        from sighting s
                        where shape != ""
                        order by shape desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllLat():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select Lat 
                        from state s """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Lat"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllLon():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select Lng 
                            from state s """
            cursor.execute(query)

            for row in cursor:
                result.append(row["Lng"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodes(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.*
                        from state s, sighting s2 
                        where s2.state = s.id
                        and s.Lat > %s
                        and s.Lng > %s
                        and s2.shape = %s
                        group by s2.state"""
            cursor.execute(query, (lat, lon, shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getNodiPesati(lat, lon, shape):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select s.state, sum(duration) as totale
                        from sighting s
                        where s.state in (select s.id
                                            from state s, sighting s2 
                                            where s2.state = s.id
                                            and s.Lat > %s
                                            and s.Lng > %s
                                            and s2.shape = %s 
                                            group by s2.state)
                        group by s.state """

            cursor.execute(query, (lat, lon, shape))

            for row in cursor:
                result[row["state"]] = row["totale"]
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def sonoVicini(id1, id2):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select *
                        from neighbor n 
                        where n.state1 = %s 
                        and n.state2 = %s """

            cursor.execute(query, (id1, id2))

            for row in cursor:
                result.append((row["state1"], row["state2"]))
            cursor.close()
            cnx.close()
        return result


