from bson.json_util import dumps
from flask import Response


def wrong_res(error):
    res_obj = {"error": error}
    return Response(dumps(res_obj), status=500, mimetype="application/json")