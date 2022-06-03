from setuptools import setup, find_packages


setup(
    name="yawarana_sketch_clld",
    version="0.0.3.dev",
    description="yawarana_sketch_clld",
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author="Florian Matter",
    author_email="florianmatter@gmail.com",
    url="https://github.com/fmatter/yawarana-sketch-clld",
    keywords="web pyramid pylons",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "clld",  # >=7.0
        "waitress",
        "clld_morphology_plugin @ git+https://git@github.com/fmatter/clld-morphology-plugin@0.0.3",
        "clld_corpus_plugin @ git+https://git@github.com/fmatter/clld-corpus-plugin@0.0.3",
        "clld_document_plugin @ git+https://git@github.com/fmatter/clld-document-plugin@0.0.1",
        "clld_markdown_plugin @ git+https://git@github.com/clld/clld-markdown-plugin",
        "cldfviz",
    ],
    extras_require={
        "dev": ["flake8", "waitress"],
        "test": [
            "mock",
            "pytest>=5.4",
            "pytest-clld",
            "pytest-mock",
            "pytest-cov",
            "coverage>=4.2",
            "selenium",
            "zope.component>=3.11.0",
        ],
    },
    test_suite="yawarana_sketch_clld",
    entry_points="""\
    [paste.app_factory]
    main = yawarana_sketch_clld:main
""",
)
