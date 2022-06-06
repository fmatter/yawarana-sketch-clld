from clld_morphology_plugin.models import Morph, Morpheme, Wordform, POS
from clld_corpus_plugin.models import Text
from clld.db.meta import DBSession
from clld.db.models import Sentence
from clld_corpus_plugin.util import rendered_sentence
from clld.web.util.htmllib import HTML
from yawarana_sketch_clld.models import Phoneme
from clld_document_plugin.models import Document

def my_render_ex(req, objid, ids=None, subexample=False, **kwargs):
    if "subexample" in kwargs.get("format", []):
        subexample=True
    example_id = kwargs.get("example_id", [None])[0]
    if objid == "__all__":
        if ids:
            ex_strs = [my_render_ex(req, mid, subexample=True) for mid in ids[0].split(",")]
            return HTML.ol(HTML.li(HTML.ol(*ex_strs, class_="subexample"), class_="example", id_=example_id), class_="example")
    sentence = DBSession.query(Sentence).filter(Sentence.id == objid).first()
    if subexample:
        return rendered_sentence(req, sentence, sentence_link=True, counter_class="subexample", in_context=True)
    else:
        return HTML.ol(rendered_sentence(req, sentence, sentence_link=True, in_context=True, example_id=example_id, counter_class="example"), class_="example")
    return 

def render_morpheme(req, objid, **kwargs):
    morpheme = DBSession.query(Morpheme).filter(Morpheme.id == objid).first()
    url = req.route_url("morpheme", id=objid, **kwargs)
    with_translation = "with_translation" in kwargs
    md_str = f"*[{morpheme.name}]({url})*"
    if with_translation:
        meanings = [x.meaning.name for x in morpheme.meanings]
        md_str += f" ‘{', '.join(meanings)}’"
    return md_str

custom_model_map = {
    "MorphTable": {"route": "morph", "model": Morph, "decorate": lambda x: f"*{x}*"},
    "MorphsetTable": {
        "route": "morpheme",
        "model": Morpheme,
        "decorate": lambda x: f"*{x}*",
    },
    "TextTable": {"route": "text", "model": Text, "decorate": lambda x: f"'{x}'"},
    "POSTable": {"route": "pos", "model": POS},
    "FormTable": {"route": "wordform", "model": Wordform, "decorate": lambda x: f"*{x}*"},
    "ChapterTable": {"route": "document", "model": Document},
    "PhonemeTable": {"route": "phoneme", "model": Phoneme, "decorate": lambda x: f"/{x}/"},
}
custom_function_map = {"ExampleTable": my_render_ex, "MorphsetTable": render_morpheme}
