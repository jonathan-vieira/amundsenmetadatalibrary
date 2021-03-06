from http import HTTPStatus
from typing import Iterable, Union, Mapping

from flask import request
from flask_restful import Resource, fields, marshal
from flasgger import swag_from

from metadata_service.proxy import get_proxy_client

popular_table_fields = {
    'database': fields.String,
    'cluster': fields.String,
    'schema': fields.String,
    'table_name': fields.String(attribute='name'),
    'table_description': fields.String(attribute='description'),  # Optional
}

popular_tables_fields = {
    'popular_tables': fields.List(fields.Nested(popular_table_fields))
}


class PopularTablesAPI(Resource):
    """
    PopularTables API
    """
    def __init__(self) -> None:
        self.client = get_proxy_client()

    @swag_from('swagger_doc/popular_tables_get.yml')
    def get(self) -> Iterable[Union[Mapping, int, None]]:
        limit = request.args.get('limit', 10, type=int)
        popular_tables = self.client.get_popular_tables(num_entries=limit)
        return marshal({'popular_tables': popular_tables}, popular_tables_fields), HTTPStatus.OK
