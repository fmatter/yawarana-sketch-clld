# yawarana-sketch-clld

This is the source code for a [CLLD](https://clld.org/) app serving a digital grammar sketch of [Yawarana](https://glottolog.org/resource/languoid/id/yaba1248), accessible [here](https://fl.mt/yawarana-sketch).
The corresponding [CLDF](https://cldf.clld.org/) dataset can be found [here](https://github.com/fmatter/yawarana-sketch-cldf).
The heavy lifting is done by these plugins:

* [clld-morphology-plugin](https://github.com/fmatter/clld-morphology-plugin)
* [clld-corpus-plugin](https://github.com/fmatter/clld-corpus-plugin)
* [clld-markdown-plugin](https://github.com/clld/clld-markdown-plugin)
* [clld-document-plugin](https://github.com/fmatter/clld-document-plugin)

The app itself only has an additional `Phoneme` model.
It should be usable with other datasets.