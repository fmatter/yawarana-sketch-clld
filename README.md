# yawarana-sketch-clld

This is the source code for a [CLLD](https://clld.org/) app serving a digital grammar sketch of [Yawarana](https://glottolog.org/resource/languoid/id/yaba1248), accessible [here](https://fl.mt/yawarana-sketch).
The corresponding [CLDF](https://cldf.clld.org/) dataset can be found [here](https://github.com/fmatter/yawarana-sketch-cldf).
Most of the heavy lifting is done by the following plugins:

* [clld-morphology-plugin](https://github.com/fmatter/clld-morphology-plugin)
* [clld-corpus-plugin](https://github.com/fmatter/clld-corpus-plugin)
* [clld-markdown-plugin](https://github.com/clld/clld-markdown-plugin)

The app itself has additional `Document` and `Phoneme` models, as well as some [CSS](yawarana_grammar/static/project.css) and [JS](yawarana_grammar/static/project.js).
It should be possible to use it with other datasets.