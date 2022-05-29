<%from clld_markdown_plugin import markdown%> ${markdown(request, """#### The corpus

A corpus of [texts](texts) forms the basis of this grammar sketch.
They were collected by [Natalia Cáceres-Arandia](https://pages.uoregon.edu/nataliac/) in the course of the NSF funded project ['Documenting Linguistic Structure and Language Change in Yawarana'](https://nsf.gov/awardsearch/showAward?AWD_ID=1500714&HistoricalAwards=false).
They were transcribed in ELAN and enriched with morphological annotation by [uniparser-yawarana](https://github.com/fmatter/uniparser-yawarana/) ([matter2022uniparser](sources.bib?with_internal_ref_link&ref#cldf:matter2022uniparser))
The following excerpt showcases the features of the corpus:

[Example ctorat-03](ExampleTable?example_no=1#cldf:ctorat-03)

The first object line is a link to the entire text record ('sentence', 'example'...).
The second line contains links to individual word forms.
The third line contains links to individual morphs.
The link in parentheses leads to the (con-)text of the record.
Audio associated with the record is shown below it.
Translations are partially in English, partially in the contact language, Spanish.

Words that uniparser-yawarana was unable to parse are glossed with `***`:

[Example convrisamaj-28](ExampleTable?example_no=2#cldf:convrisamaj-28)

Words with multiple possible analyses (where none has been confirmed manually yet) are glossed with `?`:

[Example anfoperso-01](ExampleTable?example_no=3#cldf:anfoperso-01)

#### The 'dictionary'
The dictionary part of this app contains different kinds of entities.
At the moment, these are morphemes, morphs, and word forms.
They relate to each other as follows: word forms are forms that occur in the annotated corpus or were uttered in elicitation.
At the moment, there are no unattested (but existent) word forms.
Word forms are composed of morphs, which in turn belong to morphemes.
Word forms as well as morphemes and their morphs can have different meanings, depending on the context.

To illustrate: the form [](FormTable#cldf:f90c63ed-bd4c-43b7-b9f9-2709d3ff0ddd1-septcp) 's/he slept' is composed of the morphs [Morph f90c63ed-bd4c-43b7-b9f9-2709d3ff0ddd1](MorphTable?#cldf:f90c63ed-bd4c-43b7-b9f9-2709d3ff0ddd1) and [Morph septcp](MorphTable?#cldf:septcp), which in turn belong to the morphemes [Morpheme f90c63ed-bd4c-43b7-b9f9-2709d3ff0ddd](MorphsetTable?#cldf:f90c63ed-bd4c-43b7-b9f9-2709d3ff0ddd) and [Morpheme septcp](MorphsetTable?#cldf:septcp).
All of the preceding links lead to detail views of these entities, with information like morphological structure, associated word forms, and, most importantly, tokens from the corpus.

#### The grammar
...is under construction.
The text is written with [pylingdocs](https://github.com/fmatter/pylingdocs), and is available as individual chapters under [documents](documents).
A PDF version can be found [here](download).

""")[0]|n}