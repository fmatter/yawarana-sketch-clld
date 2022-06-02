from clld_morphology_plugin.models import Morph, Morpheme, Wordform, POS
from clld_corpus_plugin.models import Text
from clld.db.meta import DBSession
from clld.db.models import Sentence
from clld_corpus_plugin.util import rendered_sentence
from clld.web.util.htmllib import HTML
from yawarana_sketch_clld.models import Document, Phoneme

def my_render_ex(req, objid, ids=None, subexample=False, **kwargs):
    if "subexample" in kwargs.get("format", []):
        subexample=True
    pexample_id = kwargs.get("example_id", [""])[0]
    if objid == "__all__":
        if ids:
            ex_strs = [my_render_ex(req, mid, subexample=True) for mid in ids[0].split(",")]
            return HTML.ol(HTML.li(HTML.ol(*ex_strs, class_="subexample"), class_="example", id_=pexample_id), class_="example")
    sentence = DBSession.query(Sentence).filter(Sentence.id == objid)[0]
    if subexample:
        return rendered_sentence(req, sentence, sentence_link=True, counter_class="subexample", in_context=True)
    else:
        return HTML.ol(rendered_sentence(req, sentence, sentence_link=True, in_context=True, counter_class="example"), class_="example")
    return 

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
custom_function_map = {"ExampleTable": my_render_ex}
