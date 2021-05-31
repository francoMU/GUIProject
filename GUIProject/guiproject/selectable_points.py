from dataclasses import dataclass, field
from typing import List
from marshmallow import Schema, fields, post_load


@dataclass
class Data:
    energies: List = field(default_factory=list)
    delta: List = field(default_factory=list)


class DataSchema(Schema):
    energies = fields.List(fields.Float(), required=True)
    delta = fields.List(fields.Float(), required=True)

    @post_load
    def make_user(self, data, **kwargs):
        return Data(**data)
