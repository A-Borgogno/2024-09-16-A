from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    # @staticmethod
    # def get_all_states():
    #     cnx = DBConnect.get_connection()
    #     result = []
    #     if cnx is None:
    #         print("Connessione fallita")
    #     else:
    #         cursor = cnx.cursor(dictionary=True)
    #         query = """select *
    #                 from state s"""
    #         cursor.execute(query)
    #
    #         for row in cursor:
    #             result.append(
    #                 State(**row))
    #
    #         cursor.close()
    #         cnx.close()
    #     return result

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
    def get_lat_lng_limits():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT MIN(s.Lat) as lat_min, MAX(s.Lat) as lat_max, MIN(s.Lng) as lng_min, MAX(s.Lng) as lng_max
                       from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["lat_min"])
                result.append(row["lat_max"])
                result.append(row["lng_min"])
                result.append(row["lng_max"])

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
                    ORDER BY anno ASC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
                        FROM sighting s 
                        ORDER BY shape DESC"""
            cursor.execute(query)

            for row in cursor:
                if row["shape"] != "":
                    result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_nodes(lat, lng, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT s1.*, SUM(si1.duration) as duration
                        from state s1, sighting si1
                        where s1.id = si1.state 
                        and si1.shape=%s
                        AND s1.Lat >%s and s1.Lng >%s
                        GROUP BY s1.id """
            cursor.execute(query, (shape, lat, lng))

            for row in cursor:
                result.append(State(**row))
                if result[-1].Neighbors is None:
                    result[-1].Neighbors = []

            cursor.close()
            cnx.close()
        return result




