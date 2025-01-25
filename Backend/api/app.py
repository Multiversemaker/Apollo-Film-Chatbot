from flask import Flask, Response, request
from flask_cors import CORS
import json
from utils import async_route, extract_search_term
from database import MovieDatabase

app = Flask(__name__)
CORS(app)
db = MovieDatabase()

@app.route("/movie-with-attribute", methods=['GET'])
@async_route
async def movie_with_attribute():
    movie_attribute = request.args.get('movie_attribute', '').lower()
    search_type = request.args.get('search_type', 'general')

    print(f"[INFO] Received Request: movie_attribute={movie_attribute}, search_type={search_type}")
    
    if not movie_attribute:
        return Response(
            response=json.dumps([], ensure_ascii=False).encode('utf-8'),
            status=200,
            mimetype="application/json; charset=utf-8"
        )

    try:
        if search_type == 'country':
            movies = await db.search_movies_by_country(movie_attribute)
        elif search_type == 'genre':
            movies = await db.search_movies_by_genre(movie_attribute)
        elif search_type == 'year':
            movies = await db.search_movies_by_year(int(movie_attribute))
        else:
            search_term = extract_search_term(movie_attribute)
            if search_term == "unknown":
                return Response(
                    response=json.dumps({"message": "Tidak ada film yang ditemukan dengan kata kunci tersebut."}),
                    status=200,
                    mimetype="application/json; charset=utf-8"
                )
            movies = await db.search_movies(search_term)

        if not movies:
            if search_type == 'country':
                message = "Maaf, tidak ada film yang ditemukan dari negara tersebut."
            elif search_type == 'genre':
                message = f"Maaf, tidak ada film dengan genre '{movie_attribute}'."
            elif search_type == 'year':
                message = f"Maaf, tidak ada film yang dirilis pada tahun {movie_attribute}."
            else:
                message = f"Maaf, tidak ada film yang ditemukan untuk '{movie_attribute}'."
            return Response(
                response=json.dumps({"message": message}, ensure_ascii=False),
                status=200,
                mimetype="application/json; charset=utf-8"
            )

        return Response(
            response=json.dumps(movies, ensure_ascii=False).encode('utf-8'),
            status=200,
            mimetype="application/json; charset=utf-8"
        )

    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        return Response(
            response=json.dumps({
                "error": "An error occurred while searching for movies",
                "details": str(e)
            }, ensure_ascii=False).encode('utf-8'),
            status=500,
            mimetype="application/json; charset=utf-8"
        )
@app.route("/recommend-movies", methods=['GET'])
@async_route
async def recommend_movies():
    min_rating = float(request.args.get('min_rating', 0))  # Default minimum rating 0
    print(f"[INFO] Received Request: min_rating={min_rating}")

    try:
        movies = await db.search_movies_by_rating(min_rating)

        if not movies:
            return Response(
                response=json.dumps({"message": "No movies found with the specified rating."}),
                status=200,
                mimetype="application/json; charset=utf-8"
            )

        return Response(
            response=json.dumps(movies, ensure_ascii=False).encode('utf-8'),
            status=200,
            mimetype="application/json; charset=utf-8"
        )

    except Exception as e:
        print(f"[ERROR] An error occurred: {str(e)}")
        return Response(
            response=json.dumps({
                "error": "An error occurred while searching for movies",
                "details": str(e)
            }, ensure_ascii=False).encode('utf-8'),
            status=500,
            mimetype="application/json; charset=utf-8"
        )
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=9001)