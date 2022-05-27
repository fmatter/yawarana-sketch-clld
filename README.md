# yawarana-sketch-clld

This is the source code for a CLLD app serving a digital grammar sketch of [Yawarana](https://glottolog.org/resource/languoid/id/yaba1248).
Most of the heavy lifting is done by the following plugins:

* [clld-morphology-plugin](https://github.com/fmatter/clld-morphology-plugin)
* [clld-corpus-plugin](https://github.com/fmatter/clld-corpus-plugin)
* [clld-markdown-plugin](https://github.com/clld/clld-markdown-plugin)

The app itself has additional `Document` and `Phoneme` models, as well as [some CSS](blob/main/yawarana_grammar/static/project.css) and [JS](blob/main/yawarana_grammar/static/project.js).

The app can be viewed [here](fl.mt/yawarana-sketch).