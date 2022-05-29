import collections

from pyramid.config import Configurator
from clld.db.models import common
from clld.interfaces import IMapMarker, IValueSet, IValue, IDomainElement
from clldutils.svg import pie, icon, data_url

# we must make sure custom models are known at database initialization!
from yawarana_grammar import models, interfaces
from yawarana_grammar.adapters import PdfDownload


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include("clld.web.app")
    config.include("clld_corpus_plugin")
    config.include("clld_morphology_plugin")
    config.include("clld_markdown_plugin")

    config.register_resource(
        "document", models.Document, interfaces.IDocument, with_index=True
    )

    config.register_resource(
        "phoneme", models.Phoneme, interfaces.IPhoneme, with_index=True
    )
    config.register_download(PdfDownload(common.Dataset, config.root_package.__name__))
    return config.make_wsgi_app()
