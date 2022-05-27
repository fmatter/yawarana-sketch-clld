import itertools
import collections

from pycldf import Sources, Dataset
from clldutils.misc import nfilter
from clldutils.color import qualitative_colors
from clld.cliutil import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clld_morphology_plugin.models import (
    MorphemeMeaning,
    Morpheme,
    Morph,
    Meaning,
    Wordform,
    FormSlice,
    FormMeaning,
    Wordform_files,
)
from clld_corpus_plugin.models import Text, TextSentence, SentenceSlice
import yawarana_grammar
from yawarana_grammar import models
from slugify import slugify
import re


def main(args):

    ds = Dataset.from_metadata(
        "/home/florianm/Dropbox/research/cariban/yawarana/yaw_cldf/cldf/metadata.json"
    )

    data = Data()
    dataset = data.add(
        common.Dataset,
        yawarana_grammar.__name__,
        id=yawarana_grammar.__name__,
        name="A digital sketch grammar of Yawarana",
        domain="fl.mt/yawarana-sketch",
        contact="florianmatter@gmail.com",
        publisher_name="",
        publisher_place="University of Oregon",
        publisher_url="",
        license="http://creativecommons.org/licenses/by/4.0/",
        jsondata={
            "license_icon": "cc-by.png",
            "license_name": "Creative Commons Attribution 4.0 International License",
        },
    )

    fm = common.Contributor(
        id="fm",
        name="Florian Matter",
        email="florianmatter@gmail.com",
        url="https://fl.mt",
    )

    nc = common.Contributor(
        id="nc",
        name="Natalia Cáceres Arandia",
    )

    sg = common.Contributor(
        id="sg",
        name="Spike Gildea",
    )
    dataset.editors.append(common.Editor(contributor=fm, ord=1, primary=True))
    dataset.editors.append(common.Editor(contributor=nc, ord=2, primary=True))
    dataset.editors.append(common.Editor(contributor=sg, ord=3, primary=True))

    print("Sources")
    for rec in bibtex.Database.from_file(ds.bibpath):
        data.add(common.Source, rec.id, _obj=bibtex2source(rec))

    print("Languages")
    for lang in ds.iter_rows("LanguageTable"):
        data.add(
            common.Language,
            lang["ID"],
            id=lang["ID"],
            name=lang["Name"],
            latitude=lang["Latitude"],
            longitude=lang["Longitude"],
        )

    print("Meanings")
    for meaning in ds.iter_rows("ParameterTable"):
        data.add(Meaning, meaning["ID"], id=meaning["ID"], name=meaning["Name"])

    print("Morphemes")
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
        )
        for meaning in morpheme["Parameter_ID"]:
            data.add(
                MorphemeMeaning,
                f"{morpheme['ID']}-{meaning}",
                id=f"{morpheme['ID']}-{meaning}",
                morpheme=new_morpheme,
                meaning=data["Meaning"][meaning],
            )

    print("Morphs")
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

    print("Texts")
    for text in ds.iter_rows("TextTable"):
        data.add(
            Text,
            text["ID"],
            id=text["ID"],
            name=text["Title"],
            description=text["Description"],
            text_metadata=text["Metadata"],
        )

    print("Sentences")
    for ex in ds.iter_rows("ExampleTable"):
        data.add(
            common.Sentence,
            ex["ID"],
            id=ex["ID"],
            name=ex["Primary_Text"],
            description=ex["Translated_Text"],
            analyzed="\t".join(ex["Analyzed_Word"]),
            gloss="\t".join(ex["Gloss"]),
            language=data["Language"][ex["Language_ID"]],
            comment=ex["Comment"],
        )
        data.add(
            TextSentence,
            ex["ID"],
            sentence=data["Sentence"][ex["ID"]],
            text=data["Text"][ex["Text_ID"]],
        )

    print("Phonemes!")
    phoneme_dict = {}
    for pnm in ds.iter_rows("PhonemeTable"):
        phoneme_dict[pnm["Name"]] = pnm["ID"]
        data.add(models.Phoneme, pnm["ID"], id=pnm["ID"], name=pnm["Name"])

    print("Wordforms")
    for form in ds.iter_rows("FormTable"):
        new_form = data.add(
            Wordform,
            form["ID"],
            id=form["ID"],
            name=form["Form"].replace("-", "").replace("∅", ""),
            segmented=form["Form"],
            language=data["Language"][form["Language_ID"]],
            description=" / ".join(
                data["Meaning"][x].name for x in form["Parameter_ID"]
            ),
        )
        for meaning in form["Parameter_ID"]:
            data.add(
                FormMeaning,
                f"{form['ID']}-{meaning}",
                form=new_form,
                meaning=data["Meaning"][meaning],
            )
        for seg in form["Segments"]:
            data.add(
                models.FormPhoneme,
                form["ID"] + seg,
                form=new_form,
                phoneme=data["Phoneme"][phoneme_dict[seg]],
            )

    print("Audio")
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

    print("Form slices")
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

    print("Sentence slices")
    for sf in ds.iter_rows("ExampleSlices"):
        data.add(
            SentenceSlice,
            sf["ID"],
            form=data["Wordform"][sf["Form_ID"]],
            sentence=data["Sentence"][sf["Example_ID"]],
            index=int(sf["Slice"]),
            form_meaning=data["FormMeaning"][sf["Form_ID"] + "-" + sf["Parameter_ID"]],
        )

    print("Documents")
    tent = open(
        "/home/florianm/Dropbox/research/cariban/yawarana/yaw_sketch/clld_output.txt",
        "r",
    ).read()
    tent = "\n" + tent
    delim = "\n# "
    parts = tent.split(delim)[1::]

    tag_dic = {}
    content_dic = {}
    for (i, part) in enumerate(parts):
        title, content = part.split("\n", 1)
        tag = re.findall("#(.*?)'", title)
        title = title.split("{#")[0].strip()
        if len(tag) == 0:
            tag = slugify(title)
        else:
            tag = tag[0]
        content_dic[tag] = {"title": title, "content": f"<a id='{tag}'></a>" + content}

        tags = re.findall("<a id='(.*?)'></a>", content_dic[tag]["content"])
        for subtag in tags:
            if subtag in tag_dic:
                print(f"duplicate tag {subtag} in {tag}: {tag_dic[subtag]}")
            tag_dic[subtag] = tag

    # for tag in content_dic.keys():
    #     refs = re.findall(r"<a href='#(.*?)' .*?</a>", tent)
    #     for ref in refs:
    #         if tag_dic[ref] != tag:
    #             content_dic[tag]["content"] = re.sub(
    #                 rf"<a href='#{ref}'.*?</a>",
    #                 f"[crossref](ChapterTable?_anchor={ref}#cldf:{tag_dic[ref]})",
    #                 content_dic[tag]["content"],
    #             )

    for i, (tag, doc_data) in enumerate(content_dic.items()):
        data.add(
            models.Document,
            tag,
            id=tag,
            name=doc_data["title"],
            description=doc_data["content"],
            chapter_no=i + 1,
            order=chr(i + 96),
        )

    data.add(
        models.Document,
        "ambiguity",
        id="ambiguity",
        name="Manuscript: Parsing ambiguity",
        order="zzz",
        description=open(
            "/home/florianm/Dropbox/research/cariban/yawarana/yawarana-parsing-ambiguity/clld_output.txt",
            "r",
        ).read(),
    )

    data.add(
        models.Document,
        "tam",
        id="tam",
        name="Notes: TAM suffixes",
        order="zzz",
        description=open(
            "/home/florianm/Dropbox/research/cariban/yawarana/yaw_notes/clld_output.txt",
            "r",
        ).read(),
    )

    data.add(common.Language, "tri", id="tri", name="Tiriyo")

    sourced_ex = data.add(
        common.Sentence,
        "sourced-sentence",
        id="sourced-sentence",
        name="Jekï tuuka.",
        description="S/he has hit my pet.",
        analyzed="\t".join(["j-ekɨ", "tuuka"]),
        gloss="\t".join(["1-pet", "hit:PRS.PFV"]),
        language=data["Language"]["tri"],
    )

    sourced_ex1 = data.add(
        common.Sentence,
        "sourced-sentence1",
        id="sourced-sentence1",
        name="Kaikui inetawawei wï.",
        description="I haven't heard the jaguar's voice",
        analyzed="\t".join(["kaikui", "in-eta-ewa=w-ei", "wï"]),
        gloss="\t".join(["jaguar", "3NEG-hear-NEG=1Sa-COP:PRS.PFV", "1PRO"]),
        language=data["Language"]["tri"],
    )

    source = data["Source"]["triomeira1999"]
    for s_ex in [sourced_ex, sourced_ex1]:
        DBSession.add(
            common.SentenceReference(
                sentence=s_ex, source=source, key=source.id, description="239"
            )
        )


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodically whenever data has been updated.
    """
