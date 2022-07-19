from clld_morphology_plugin.models import Morph, Morpheme, Wordform, POS, Lexeme
from clld_corpus_plugin.models import Text
from clld.db.meta import DBSession
from clld.db.models import Sentence
from clld_corpus_plugin.util import rendered_sentence
from clld.web.util.htmllib import HTML
from yawarana_sketch_clld.models import Phoneme
from clld_document_plugin.models import Document
import re

# from pylingdocs.helpers

glossing_delimiters = [
    "-",
    "–",
    ".",
    "=",
    ";",
    ":",
    "*",
    "~",
    "<",
    ">",
    r"\[",
    r"\]",
    "(",
    ")",
    "/",
    r"\\",
]


def is_gloss_abbr_candidate(part, parts, j):
    return (
        part == part.upper()  # needs to be uppercase
        and part not in glossing_delimiters + ["[", "]", "\\"]  # and not a delimiter
        and part != "?"  # question marks may be used for unknown or ambiguous analyses
        and not (
            len(parts) > j + 2
            and parts[j + 2] in glossing_delimiters
            and parts[j + 1] not in [">", "-"]
        )
    )

def split_word(word):
    parts = re.split(r"([" + "|".join(glossing_delimiters) + "])", word)
    parts = [x for x in parts if x != ""]
    return parts

def decorate_gloss_string(input_string, decoration=lambda x: f"\\gl{{{x}}}"):
    words_list = input_string.split(" ")
    for i, word in enumerate(words_list):  # pylint: disable=too-many-nested-blocks
        output = " "
        # take proper nouns into account
        if len(word) == 2 and word[0] == word[0].upper() and word[1] == ".":
            output += word
        else:
            parts = split_word(word)
            for j, part in enumerate(parts):
                if is_gloss_abbr_candidate(part, parts, j):
                    # take care of numbered genders
                    if part[0] == "G" and re.match(r"\d", part[1:]):
                        output += f"\\gl{{{part.lower()}}}"
                    else:
                        for gloss in resolve_glossing_combination(part):
                            output += decoration(gloss.lower())
                else:
                    output += part
        words_list[i] = output[1:]
    gloss_text_upcased = " ".join(words_list)
    return gloss_text_upcased

def resolve_glossing_combination(input_string):
    output = []
    temp_text = ""
    for i, char in enumerate(list(input_string)):
        if re.match(r"[1-3]+", char):
            if i < len(input_string) - 1 and input_string[i + 1] == "+":
                temp_text += char
            elif input_string[i - 1] == "+":
                temp_text += char
                output.append(temp_text)
                temp_text = ""
            else:
                if temp_text != "":
                    output.append(temp_text)
                output.append(char)
                temp_text = ""
        else:
            temp_text += char
    if temp_text != "":
        output.append(temp_text)
    return output

def my_render_ex(req, objid, table, ids=None, subexample=False, **kwargs):
    if "subexample" in kwargs.get("format", []):
        subexample=True
    example_id = kwargs.get("example_id", [None])[0]
    if objid == "__all__":
        if ids:
            ex_strs = [my_render_ex(req, mid, table, subexample=True) for mid in ids[0].split(",")]
            return HTML.ol(HTML.li(HTML.ol(*ex_strs, class_="subexample"), class_="example", id_=example_id), class_="example")
    sentence = DBSession.query(Sentence).filter(Sentence.id == objid).first()
    if subexample:
        return rendered_sentence(req, sentence, sentence_link=True, counter_class="subexample", in_context=True)
    else:
        return HTML.ol(rendered_sentence(req, sentence, sentence_link=True, in_context=True, example_id=example_id, counter_class="example"), class_="example")

table_dic = {"MorphsetTable": [Morpheme, "morpheme"], "FormTable": [Wordform, "wordform"], "LexemeTable": [Lexeme, "lexeme"]}
def render_lfts(req, objid, table, **kwargs):
    model, route = table_dic[table]
    unit = DBSession.query(model).filter(model.id == objid).first()
    url = req.route_url(route, id=objid, **kwargs)
    with_translation = "no_translation" not in kwargs
    md_str = f"*[{unit.name}]({url})*"
    if with_translation:
        meanings = [decorate_gloss_string(x.meaning.name, decoration=lambda x: f"<span class='smallcaps'>{x}</span>") for x in unit.meanings]
        md_str += f" ‘{', '.join(meanings)}’"
    return md_str


def render_lex(req, objid, table, **kwargs):
    unit = DBSession.query(Lexeme).filter(Lexeme.id == objid).first()
    url = req.route_url("lexeme", id=objid, **kwargs)
    with_translation = "no_translation" not in kwargs
    md_str = f"*[{unit.name}]({url})*"
    if with_translation:
        meanings = [decorate_gloss_string(x, decoration=lambda x: f"<span class='smallcaps'>{x}</span>") for x in [unit.description]]
        md_str += f" ‘{', '.join(meanings)}’"
    return md_str

custom_model_map = {
    "MorphTable": {"route": "morph", "model": Morph, "decorate": lambda x: f"*{x}*"},
    "TextTable": {"route": "text", "model": Text, "decorate": lambda x: f"'{x}'"},
    "POSTable": {"route": "pos", "model": POS},
    "FormTable": {"route": "wordform", "model": Wordform, "decorate": lambda x: f"*{x}*"},
    "ChapterTable": {"route": "document", "model": Document},
    "PhonemeTable": {"route": "phoneme", "model": Phoneme, "decorate": lambda x: f"/{x}/"},
}
custom_function_map = {"ExampleTable": my_render_ex, "MorphsetTable": render_lfts, "FormTable": render_lfts, "LexemeTable": render_lex}
