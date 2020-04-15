from base64 import b64decode
from typing import Any, Dict

from flask import Flask, Response, jsonify, request
from movies.Movies import MOVIES
from movies.user import Users

app = Flask(__name__)
all_users = Users()


@app.route('/movies', methods=['post', 'get'])
def action_with_movies() -> Any:
    user_data = request.headers.get('Authorization')

    if not user_data:
        return Response(
            status=401,
            headers={'WWW-Authenticate': 'Basic realm="How about authorization?"'},
        )

    decode_data = b64decode(user_data).decode()
    try:
        username, password = decode_data.split(':')
    except ValueError:
        return Response(status=400)

    if not all_users.check_user_existence(username):
        all_users.create_user(username, password)

    if not all_users.check_user_password(username, password):
        return Response(
            status=401,
            headers={'WWW-Authenticate': 'Basic realm="How about authorization?"'},
        )

    content = request.json
    current_id = content['id']
    try:
        method = content['method']
    except KeyError:
        return Response(status=404)

    return pars_request(method, content, current_id)


def pars_request(method: str, content: Dict[str, Any], current_id: str) -> Any:
    if method == 'add_comment':
        return add_comment(content['params'], current_id)

    if method == 'rate_film':
        return rate_film(content['params'], current_id)

    if method == 'get_rating':
        return get_rating(content['params'], current_id)

    if method == 'get_ratings_count':
        return get_ratings_count(content['params'], current_id)

    if method == 'get_comments_count':
        return get_comments_count(content['params'], current_id)

    return pars_next_requests(method, content, current_id)


def pars_next_requests(method: str, content: Dict[str, Any], current_id: str) -> Any:
    if method == 'get_films_by_year':
        return get_films_by_year(content['params'], current_id)

    if method == 'get_films_by_substring':
        return get_films_by_substring(content['params'], current_id)

    if method == 'get_top_films':
        return get_top_films(content['params'], current_id)

    return Response(status=404)


def add_comment(params: Dict[str, Any], current_id: str) -> Any:
    try:
        name_film = params['name_film']
        comment = params['comment']
        MOVIES[name_film].add_comment(comment)
    except KeyError:
        return Response(status=400)

    result = {'jsonrpc': '2.0', 'result': 'comment add', 'id': current_id}
    return jsonify(result)


def rate_film(params: Dict[str, Any], current_id: str) -> Any:
    try:
        name_film = params['name_film']
        rate = params['rate']
    except KeyError:
        return Response(status=400)

    if rate > 10 or rate < 0:
        return Response(status=400)
    MOVIES[name_film].rate_film(rate)
    result = {'jsonrpc': '2.0', 'result': 'Movie rated', 'id': current_id}
    return jsonify(result)


def get_rating(params: Dict[str, Any], current_id: str) -> Any:
    try:
        name_film = params['name_film']
    except KeyError:
        return Response(status=400)

    rating = MOVIES[name_film].get_rating()
    result = {'jsonrpc': '2.0', 'result': rating, 'id': current_id}
    return jsonify(result)


def get_ratings_count(params: Dict[str, Any], current_id: str) -> Any:
    try:
        name_film = params['name_film']
        ratings_count = MOVIES[name_film].number_rated
    except KeyError:
        return Response(status=400)

    result = {'jsonrpc': '2.0', 'result': ratings_count, 'id': current_id}
    return jsonify(result)


def get_comments_count(params: Dict[str, Any], current_id: str) -> Any:
    try:
        name_film = params['name_film']
        comments_count = MOVIES[name_film].get_comments_count()
    except KeyError:
        return Response(status=400)

    result = {'jsonrpc': '2.0', 'result': comments_count, 'id': current_id}
    return jsonify(result)


def get_films_by_year(params: Dict[str, Any], current_id: str) -> Any:
    try:
        year = params['year']
    except KeyError:
        return Response(status=400)

    result_list_movies = []
    for movie in MOVIES.values():
        if movie.year == year:
            result_list_movies.append(movie.__dict__)
    result = {'jsonrpc': '2.0', 'result': result_list_movies, 'id': current_id}
    return jsonify(result)


def get_films_by_substring(params: Dict[str, Any], current_id: str) -> Any:
    try:
        substring = params['substring']
    except KeyError:
        return Response(status=400)

    result_list_movies = []
    for movie in MOVIES.values():
        if substring in movie.name:
            result_list_movies.append(movie.__dict__)

    result = {'jsonrpc': '2.0', 'result': result_list_movies, 'id': current_id}
    return jsonify(result)


def get_top_films(params: Dict[str, Any], current_id: str) -> Any:
    try:
        rate = params['rate']
    except KeyError:
        return Response(status=400)

    result_list_movies = []
    for movie in MOVIES.values():
        if movie.get_rating() > rate:
            result_list_movies.append(movie.__dict__)
    result = {'jsonrpc': '2.0', 'result': result_list_movies, 'id': current_id}
    return jsonify(result)
