(amm) greg@epfl:~/workspace-idevelop/amm$ http POST http://127.0.0.1:8000/v1/apikeys/ username='kermit' password='lgMB@Ece2Gqj6o3J'
HTTP/1.0 201 Created
Content-Type: application/json
Date: Wed, 08 Feb 2017 09:11:14 GMT
Server: WSGIServer/0.2 CPython/3.5.2
X-Frame-Options: SAMEORIGIN

{
    "access_key": "3cb8230f0c134f170f40",
    "secret_key": "74d623c9d954481bdee772fec12cc17ab8f38c1f"
}



(amm) greg@epfl:~/workspace-idevelop/amm$ http GET http://127.0.0.1:8000/v1/apikeys/ access_key=='3cb8230f0c134f170f40' secret_key=='74d623c9d954481bdee772fec12cc17ab8f38c1f'
HTTP/1.0 201 Created
Content-Type: application/json
Date: Wed, 08 Feb 2017 09:16:25 GMT
Server: WSGIServer/0.2 CPython/3.5.2
X-Frame-Options: SAMEORIGIN

[
    "3cb8230f0c134f170f40"
]
