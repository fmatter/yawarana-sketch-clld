import sys
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clld_corpus_plugin.models import (
    SentenceSlice,
    SentenceTag,
    Tag,
    Text,
    TextSentence,
    TextTag,
)
from clld_document_plugin.models import Document
from clld_morphology_plugin.models import (
    POS,
    FormMeaning,
    FormSlice,
    Inflection,
    Lexeme,
    LexemeLexemePart,
    LexemeMorphemePart,
    Meaning,
    Morph,
    Morpheme,
    MorphemeMeaning,
    Wordform,
    Wordform_files,
)
from clldutils.loglib import get_colorlog
from pycldf import Sources
from slugify import slugify
import logging
import yawarana_sketch_clld
from yawarana_sketch_clld import models

log = get_colorlog(__name__, sys.stdout, level=logging.DEBUG)


def main(args):

    ds = args.cldf
    ds_tables = list(ds.components.keys()) + [str(x.url) for x in ds.tables]
    license_dic = {
        "creativecommons.org/licenses/by/4.0": {
            "license_icon": "cc-by.png",
            "license_name": "Creative Commons Attribution 4.0 International License",
        },
        "creativecommons.org/licenses/by-sa/4.0": {
            "license_icon": "cc-by-sa.png",
            "license_name": "Creative Commons Attribution-ShareAlike 4.0 International",
        },
    }

    data = Data()

    dataset = data.add(
        common.Dataset,
        yawarana_sketch_clld.__name__,
        id=yawarana_sketch_clld.__name__,
        name=ds.properties["dc:title"],
        domain=ds.properties.get("dc:identifier", "://").split("://")[1],
        publisher_name="",
        publisher_place="",
        publisher_url="",
        license=ds.properties["dc:license"],
        jsondata=license_dic.get(
            ds.properties["dc:license"].split("//", 1)[1].strip("/"), {}
        ),
    )

    if "ContributorTable" in ds_tables:
        log.info("Contributors")
        for contributor in ds.iter_rows("ContributorTable"):
            if dataset.contact is None and contributor["Email"] is not None:
                dataset.contact = contributor["Email"]

            new_cont = data.add(
                common.Contributor,
                contributor["ID"],
                id=contributor["ID"],
                name=contributor["Name"],
                email=contributor["Email"],
                url=contributor["Url"],
            )
            dataset.editors.append(
                common.Editor(
                    contributor=new_cont, ord=contributor["Order"], primary=True
                )
            )

    log.info("Sources")
    for rec in bibtex.Database.from_file(ds.bibpath):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    log.info("Languages")
    for lang in ds.iter_rows("LanguageTable"):
        data.add(
            common.Language,
            lang["ID"],
            id=lang["ID"],
            name=lang["Name"],
            latitude=lang["Latitude"],
            longitude=lang["Longitude"],
        )

    log.info("Meanings")
    for meaning in ds.iter_rows("ParameterTable"):
        data.add(Meaning, meaning["ID"], id=meaning["ID"], name=meaning["Name"])

    log.info("Morphemes")
    for morpheme in ds.iter_rows("MorphsetTable"):
        new_morpheme = data.add(
            Morpheme,
            morpheme["ID"],
            id=morpheme["ID"],
            name=morpheme["Name"],
            language=data["Language"][morpheme["Language_ID"]],
            description=" / ".join(
                data["Meaning"][x].name for x in morpheme["Parameter_ID"]
            ),
            comment=morpheme["Comment"],
        )
        for meaning in morpheme["Parameter_ID"]:
            data.add(
                MorphemeMeaning,
                f"{morpheme['ID']}-{meaning}",
                id=f"{morpheme['ID']}-{meaning}",
                morpheme=new_morpheme,
                meaning=data["Meaning"][meaning],
            )

    log.info("Morphs")
    for morph in ds.iter_rows("MorphTable"):
        data.add(
            Morph,
            morph["ID"],
            id=morph["ID"],
            name=morph["Name"],
            language=data["Language"][morph["Language_ID"]],
            morpheme=data["Morpheme"][morph["Morpheme_ID"]],
            description=" / ".join(
                data["Meaning"][x].name for x in morph["Parameter_ID"]
            ),
        )

    tag_dic = {}

    def tag_slug(tag):
        if tag not in tag_dic:
            tagslug = slugify(tag)
            suff = 1
            while f"{tagslug}-{suff}" in tag_dic.values():
                suff += 1
            tag_dic[tag] = f"{tagslug}-{suff}"
        return tag_dic[tag]

    log.info("Texts")
    for text in ds.iter_rows("TextTable"):
        tags = text["Metadata"].pop("tags", [])
        new_text = data.add(
            Text,
            text["ID"],
            id=text["ID"],
            name=text["Title"],
            description=text["Description"],
            text_metadata=text["Metadata"],
        )
        for tag in tags:
            if tag not in data["Tag"]:
                data.add(Tag, tag, id=tag, name=tag)
            data.add(TextTag, text["ID"] + tag, tag=data["Tag"][tag], text=new_text)

    log.info("Sentences")
    for ex in ds.iter_rows("ExampleTable"):
        new_ex = data.add(
            common.Sentence,
            ex["ID"],
            id=ex["ID"],
            name=ex["Primary_Text"],
            description=ex["Translated_Text"],
            markup_description=ex["Original_Translation"],
            analyzed="\t".join(ex["Analyzed_Word"]),
            gloss="\t".join(ex["Gloss"]),
            language=data["Language"][ex["Language_ID"]],
            comment=ex["Comment"],
        )
        for tag in set(ex["Tags"]):
            if not tag:
                continue
            slug = tag_slug(tag)
            if slug not in data["Tag"]:
                data.add(Tag, slug, id=slug, name=tag)
            data.add(
                SentenceTag, ex["ID"] + slug, tag=data["Tag"][slug], sentence=new_ex
            )
        if ex["Text_ID"] is not None:
            data.add(
                TextSentence,
                ex["ID"],
                sentence=new_ex,
                text=data["Text"][ex["Text_ID"]],
                part_no=ex["Part"],
            )
        elif len(ex["Source"]) > 0:
            bibkey, pages = Sources.parse(ex["Source"][0])
            source = data["Source"][bibkey]
            DBSession.add(
                common.SentenceReference(
                    sentence=new_ex, source=source, key=source.id, description=pages
                )
            )

    log.info("Phonemes")
    phoneme_dict = {}
    for pnm in ds.iter_rows("PhonemeTable"):
        phoneme_dict[pnm["Name"]] = pnm["ID"]
        data.add(models.Phoneme, pnm["ID"], id=pnm["ID"], name=pnm["Name"])

    log.info("Parts of speech")
    for pos in ds.iter_rows("POSTable"):
        data.add(
            POS,
            pos["ID"],
            id=pos["ID"],
            name=pos["Name"],
            description=pos["Description"],
        )

    log.info("Wordforms")
    for form in ds.iter_rows("FormTable"):
        new_form = data.add(
            Wordform,
            form["ID"],
            id=form["ID"],
            name=form["Form"].replace("-", "").replace("???", ""),
            segmented=form["Form"],
            language=data["Language"][form["Language_ID"]],
            description=" / ".join(
                data["Meaning"][x].name for x in form["Parameter_ID"]
            ),
        )
        if form["POS"] is not None:
            new_form.pos = data["POS"][form["POS"]]
        if len(form["Source"]) > 0:
            new_form.source = data["Source"][form["Source"][0]]

        for meaning in form["Parameter_ID"]:
            data.add(
                FormMeaning,
                f"{form['ID']}-{meaning}",
                form=new_form,
                meaning=data["Meaning"][meaning],
            )
        for seg in form["Segments"]:
            if seg != "???":
                data.add(
                    models.FormPhoneme,
                    form["ID"] + seg,
                    form=new_form,
                    phoneme=data["Phoneme"][phoneme_dict[seg]],
                )

    log.info("Lexemes")
    for lex in ds.iter_rows("LexemeTable"):
        new_lex = data.add(
            Lexeme,
            lex["ID"],
            id=lex["ID"],
            name=lex["Name"],
            description=lex["Description"],
            language=data["Language"][lex["Language_ID"]],
            comment=lex["Comment"],
        )
        if lex["ID"] in data["Morpheme"]:
            new_lex.root_morpheme = data["Morpheme"][lex["ID"]]

    for lexlex in ds.iter_rows("LexemeLexemeParts"):
        data.add(
            LexemeLexemePart,
            lexlex["ID"],
            base_lexeme=data["Lexeme"][lexlex["Base_ID"]],
            derived_lexeme=data["Lexeme"][lexlex["Lexeme_ID"]],
        )

    for lexmorph in ds.iter_rows("LexemeMorphemeParts"):
        data.add(
            LexemeMorphemePart,
            lexmorph["ID"],
            morpheme=data["Morpheme"][lexmorph["Morpheme_ID"]],
            lexeme=data["Lexeme"][lexmorph["Lexeme_ID"]],
        )

    log.info("Inflected forms")
    for form in ds.iter_rows("InflectionTable"):
        data.add(
            Inflection,
            form["ID"],
            lexeme=data["Lexeme"][form["Lexeme_ID"]],
            form=data["Wordform"][form["Form_ID"]],
        )

    log.info("Audio")
    for audio in ds.iter_rows("MediaTable"):
        if audio["ID"] in data["Sentence"]:
            sentence_file = common.Sentence_files(
                object_pk=data["Sentence"][audio["ID"]].pk,
                name="%s" % audio["ID"],
                id="%s" % audio["ID"],
                mime_type="audio/wav",
            )
            DBSession.add(sentence_file)
            DBSession.flush()
            DBSession.refresh(sentence_file)
        elif audio["ID"] in data["Wordform"]:
            form_file = Wordform_files(
                object_pk=data["Wordform"][audio["ID"]].pk,
                name=audio["Name"],
                id=audio["ID"],
                mime_type="audio/wav",
            )
            DBSession.add(form_file)
            DBSession.flush()
            DBSession.refresh(form_file)

    log.info("Form slices")
    for mf in ds.iter_rows("FormSlices"):
        morph = data["Morph"][mf["Morph_ID"]]
        morpheme = morph.morpheme
        morpheme_meaning_id = f"{morpheme.id}-{mf['Morpheme_Meaning']}"
        form = data["Wordform"][mf["Form_ID"]]
        form_meaning_id = f"{form.id}-{mf['Form_Meaning']}"

        new_slice = data.add(
            FormSlice,
            mf["ID"],
            form=form,
            morph=morph,
            morpheme_meaning=data["MorphemeMeaning"][morpheme_meaning_id],
            form_meaning=data["FormMeaning"][form_meaning_id],
        )
        if mf["Index"]:
            new_slice.index = int(mf["Index"])
        else:
            print(mf)

    log.info("Sentence slices")
    for sf in ds.iter_rows("ExampleSlices"):
        if sf["Form_ID"] + "-" + sf["Parameter_ID"] not in data["FormMeaning"]:
            log.warning(
                "This sentence slice's form ID is not associated with a meaning"
            )
            log.warning(sf)
            continue
        data.add(
            SentenceSlice,
            sf["ID"],
            form=data["Wordform"][sf["Form_ID"]],
            sentence=data["Sentence"][sf["Example_ID"]],
            index=int(sf["Slice"]),
            form_meaning=data["FormMeaning"][sf["Form_ID"] + "-" + sf["Parameter_ID"]],
        )

    if "ChapterTable" in ds_tables:
        log.info("Documents")
        chapters = {}
        for chapter in ds.iter_rows("ChapterTable"):
            if chapter["ID"] == "landingpage":
                dataset.description = chapter["Description"]
            else:
                ch = data.add(
                    Document,
                    chapter["ID"],
                    id=chapter["ID"],
                    name=chapter["Name"],
                    description=chapter["Description"],
                )
                if chapter["Number"] is not None:
                    ch.chapter_no = int(chapter["Number"])
                    ch.order = chr(int(chapter["Number"]) + 96)
                    chapters[ch.chapter_no] = ch
                else:
                    ch.order = "zzz"
        for nr, chapter in chapters.items():
            if 1 < nr:
                chapter.preceding = chapters[nr - 1]
    else:
        dataset.description = "This is just the corpus version."

    # # adding a presentation
    # slide_content = open(
    #     "/home/florianm/Dropbox/research/cariban/yawarana/papers/optional_ergative/yawarana-ergative-slides/output/clld/content.txt",
    #     "r",
    #     encoding="utf-8",
    # ).read()
    # slides = data.add(
    #     Document,
    #     "ergative-slides",
    #     id="ergative-slides",
    #     name="Ergativity",
    #     description=slide_content,
    #     order="zzzzz",
    #     kind="slides"
    # )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
