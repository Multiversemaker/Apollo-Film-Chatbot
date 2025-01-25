from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from utils import translate_text, get_country_name

class MovieDatabase:
    def __init__(self):
        self.driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    async def search_movies(self, search_term):
        return await self._search_movies_with_query(
            query="""
                MATCH (m:Movie)
                WHERE toLower(m.title) CONTAINS toLower($search_term)
                    OR toLower(replace(m.title, ' ', '')) CONTAINS toLower(replace($search_term, ' ', ''))
                OPTIONAL MATCH (m)<-[:BERMAIN_PERAN_FILM]-(a:Actor)
                OPTIONAL MATCH (m)-[:ASAL]->(c:Country)
                OPTIONAL MATCH (m)-[:GENRE]->(g:Genre)
                WITH DISTINCT m,
                    collect(DISTINCT a.name) AS actors,
                    collect(DISTINCT c.country) AS countries,
                    collect(DISTINCT g.genre) AS genres
                RETURN
                    m.title AS title,
                    COALESCE(m.plot, 'No description available') AS description,
                    CASE
                        WHEN size(countries) > 1 THEN
                            reduce(s = head(countries), x IN tail(countries) | s + ', ' + x)
                        WHEN size(countries) = 1 THEN head(countries)
                        ELSE 'Unknown origin'
                    END AS origin,
                    actors,
                    genres
                ORDER BY m.title
            """,
            parameters={"search_term": search_term}
        )

    async def search_movies_by_country(self, country_name):
        return await self._search_movies_with_query(
            query="""
                MATCH (m:Movie)-[:ASAL]->(c:Country)
                WHERE toLower(c.country) CONTAINS toLower($country_name)
                OPTIONAL MATCH (m)<-[:BERMAIN_PERAN_FILM]-(a:Actor)
                OPTIONAL MATCH (m)-[:GENRE]->(g:Genre)
                WITH DISTINCT m,
                    collect(DISTINCT a.name) AS actors,
                    collect(DISTINCT c.country) AS countries,
                    collect(DISTINCT g.genre) AS genres
                RETURN
                    m.title AS title,
                    COALESCE(m.plot, 'No description available') AS description,
                    CASE
                        WHEN size(countries) > 1 THEN
                            reduce(s = head(countries), x IN tail(countries) | s + ', ' + x)
                        WHEN size(countries) = 1 THEN head(countries)
                        ELSE 'Unknown origin'
                    END AS origin,
                    actors,
                    genres
                ORDER BY m.title
            """,
            parameters={"country_name": country_name}
        )

    async def search_movies_by_rating(self, min_rating=7.0):
        query = """
        MATCH (m:Movie)
        WHERE m.imdbRating >= $min_rating
        WITH m
        OPTIONAL MATCH (m)<-[:BERMAIN_PERAN_FILM]-(a:Actor)
        OPTIONAL MATCH (m)-[:ASAL]->(c:Country)
        OPTIONAL MATCH (m)-[:GENRE]->(g:Genre)
        WITH m, 
            collect(DISTINCT a.name) AS actors,
            collect(DISTINCT c.country) AS countries,
            collect(DISTINCT g.genre) AS genres
        RETURN
            m.title AS title,
            COALESCE(m.plot, 'No description available') AS description,
            CASE 
                WHEN size(countries) > 1 THEN
                    reduce(s = head(countries), x IN tail(countries) | s + ', ' + x)
                WHEN size(countries) = 1 THEN head(countries)
                ELSE 'Unknown origin'
            END AS origin,
            actors,
            genres
        ORDER BY m.imdbRating DESC
        LIMIT 10
        """
        
        with self.driver.session() as session:
            try:
                result = session.run(query, min_rating=float(min_rating))
                
                movies = []
                for record in result:
                    translated_description = await translate_text(record.get("description", "No description available"))
                    origin = get_country_name(record.get("origin", "Unknown origin"))
                    
                    movies.append({
                        "title": record.get("title", "Untitled"),
                        "description": translated_description,
                        "origin": origin,
                        "actors": record.get("actors", []),
                        "genres": record.get("genres", [])
                    })
                return movies

            except Exception as e:
                print(f"Error in query execution: {str(e)}")
                raise e

    async def search_movies_by_rating(self, min_rating=0):
        return await self._search_movies_with_query(
            query="""
               MATCH (m:Movie)
                WHERE m.imdbRating >= 7
                WITH m
                OPTIONAL MATCH (m)<-[:BERMAIN_PERAN_FILM]-(a:Actor)
                OPTIONAL MATCH (m)-[:ASAL]->(c:Country)
                OPTIONAL MATCH (m)-[:GENRE]->(g:Genre)
                WITH m, 
                    collect(DISTINCT a.name) AS actors,
                    collect(DISTINCT c.country) AS countries,
                    collect(DISTINCT g.genre) AS genres
                RETURN
                    m.title AS title,
                    m.plot AS description,
                    CASE 
                        WHEN size(countries) > 0 THEN countries[0]
                        ELSE 'Unknown origin'
                    END AS origin,
                    actors,
                    genres,
                    m.imdbRating AS imdbRating
                ORDER BY m.imdbRating DESC
                LIMIT 10
            """,
            parameters={"min_rating": float(min_rating)}
        )


    async def _search_movies_with_query(self, query, parameters):
        with self.driver.session() as session:
            try:
                result = session.run(query, **parameters)

                movies = []
                for record in result:
                    translated_description = await translate_text(record.get("description", "No description available"))
                    origin = get_country_name(record.get("origin", "Unknown origin"))
                    
                    movies.append({
                        "title": record.get("title", "Untitled"),
                        "description": translated_description,
                        "origin": origin,
                        "actors": record.get("actors", []),
                        "genres": record.get("genres", []),
                        "year": record.get("year", "Unknown year")
                    })
                return movies

            except Exception as e:
                print(f"Error in query execution: {str(e)}")
                raise e
    async def search_movies_by_rating(self, min_rating=0):
        return await self._search_movies_with_query(
            query="""
               MATCH (m:Movie)
                WHERE m.imdbRating >= 7
                WITH m
                OPTIONAL MATCH (m)<-[:BERMAIN_PERAN_FILM]-(a:Actor)
                OPTIONAL MATCH (m)-[:ASAL]->(c:Country)
                OPTIONAL MATCH (m)-[:GENRE]->(g:Genre)
                WITH DISTINCT m,
                    collect(DISTINCT a.name) AS actors,
                    collect(DISTINCT c.country) AS countries,
                    collect(DISTINCT g.genre) AS genres
                RETURN
                    m.title AS title,
                    COALESCE(m.plot, 'No description available') AS description,
                    CASE
                        WHEN size(countries) > 1 THEN
                            reduce(s = head(countries), x IN tail(countries) | s + ', ' + x)
                        WHEN size(countries) = 1 THEN head(countries)
                        ELSE 'Unknown origin'
                    END AS origin,
                    actors,
                    genres
                LIMIT 10
                ORDER BY m.imdbRating DESC
            """,
            parameters={"min_rating": min_rating}
        )
