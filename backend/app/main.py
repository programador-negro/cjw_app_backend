from fastapi import FastAPI, Body, Path, Query, Depends
from fastapi.responses import HTMLResponse, JSONResponse
from app.schemes import Movies, User, JWTBearer
from typing import List
from app.jwt_manager import create_token
from os import getenv
from app.managers.db_manager import DbManager
from app.view_users import users_view
from app.view_auth import auth_view
from app.view_people import router as people_router
from app.view_assignments import router as assignments_router
from app.view_privileges import router as privileges_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.title = "CJW Application API"
app.version = "1.0.0"

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers

app.include_router(auth_view)
app.include_router(users_view)
app.include_router(people_router)
app.include_router(assignments_router)
app.include_router(privileges_router)


# ----------------------------------------
# MAIN END POINT
# GET METHOD
# -----------
@app.get('/', tags=['home'])  # ruta de la API
def message():
    with open('app/sources/templates/home.html', 'r') as file:
        response = file.read()
    return HTMLResponse(response)  # mensaje

# ----------------------------------------
# END POINT WITH AUTHORIZATION
# RESPONSE A LIST OF MOVIES OBJECT/CLASS
# GET METHOD
# -----------
# @app.get('/movies', tags=['movies'],
#         response_model= List[Movies],  # indica que retorna una lista de objetos (json)
#         dependencies=[Depends(JWTBearer())]) # indica que solo se peude acceder a la vista una vez autenticado
# def get_movies():
#     # return movies
#     return JSONResponse(content=movies, status_code=200)


# ----------------------------------------
# END POINT WITH PARAMETER
# RESPONSE A MOVIES OBJECT
# GET METHOD
# -----------
# @app.get('/movies/{id}', tags=['movies'], response_model=Movies)
# def get_movies(id: int = Path(default = 1, ge = 1, le = 2000)):
#     for item in movies:
#         if item['id'] == id:
#             # return item
#             return JSONResponse(content=item)
#     # return []
#     return JSONResponse(content=[], status_code=404)

# ----------------------------------------
# END POINT WITH QUERY PARAMETER
# GET METHOD
# -----------
# @app.get('/movies/', tags=['movies'])
# def get_movies(category: str = Query(default = 1, min_length = 5, max_length= 15)):
#     '''
#     '''
#     for item in movies:
#         if item['category'] == category:
#             return item
#     return []


# @app.post('/movies', tags=['movies'])
# # La funcion Body() permite enviar los datos como un payload o json en vez de campos query independientes
# def create_movie(id: int = Body(), title: str = Body(), overview: str = Body(), year: int = Body(), rating: float = Body(), category: str = Body()):
#     movies.append({"id": id,
#                    "title": title,
#                    "overview": overview,
#                    "year": year,
#                    "rating": rating,
#                    "category": category})

#     return movies

# @app.put('/movies', tags=['movies'])
# def update_movie(id: int,
# 	title: str = Body(), 
# 	overview: str = Body(), 
# 	year: int = Body(), 
# 	rating: float = Body(), 
# 	category: str = Body()):

# 	for item in movies:
# 		if item['id'] == id:
# 			item["title"] =  title
# 			item["overview"] = overview
# 			item["year"] = year
# 			item["rating"] = rating
# 			item["category"] = category
# 			return movies

# ----------------------------------------
# DELETE METHOD
# -----------
# @app.delete('/movies', tags=['movies'])
# def delete_movie(id: int):
# 	for item in movies:
# 		if item['id'] == id:
# 			movies.remove(item)
# 			return movies

# ----------------------------------------
# POST METHOD
# -----------
# Usando Esquemas para la manipulacion de datos
# @app.post('/movies', tags=['movies'])
# # La funcion Body() permite enviar los datos como un payload o json en vez de campos query independientes
# def create_movie(movie: Movies):
#     movies.append(movie)
#     return movies

# ----------------------------------------
# PUT METHOD
# ----------
# @app.put('/movies', tags=['movies'])
# def update_movie(id: int, movie: Movies):
# 	for item in movies:
# 		if item['id'] == id:
# 			item["title"] =  movie.title
# 			item["overview"] = movie.overview
# 			item["year"] = movie.year
# 			item["rating"] = movie.rating
# 			item["category"] = movie.category
# 			return movies
