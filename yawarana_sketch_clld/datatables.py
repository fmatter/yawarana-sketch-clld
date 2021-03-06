from sqlalchemy.orm import joinedload
from clld.web import datatables
from clld.web.datatables.base import LinkCol, Col, LinkToMapCol
from clld.web.datatables.base import DataTable


from yawarana_sketch_clld import models


class Phonemes(DataTable):
    def col_defs(self):
        return [LinkCol(self, "name")]


def includeme(config):
    config.register_datatable("phonemes", Phonemes)
