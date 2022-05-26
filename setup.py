from setuptools import setup, find_packages


setup(
    name='yawarana_grammar',
    version='0.0.1.dev',
    description='yawarana_grammar',
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'clld',  # >=7.0
        'waitress',
        'clld_morphology_plugin @ git+ssh://git@github.com/fmatter/clld-morphology-plugin',
        'clld_corpus_plugin @ git+ssh://git@github.com/fmatter/clld-corpus-plugin',
        'clld_markdown_plugin @ git+ssh://git@github.com/clld/clld-markdown-plugin',
        'cldfviz'
],
extras_require={
        'dev': ['flake8', 'waitress'],
        'test': [
            'mock',
            'pytest>=5.4',
            'pytest-clld',
            'pytest-mock',
            'pytest-cov',
            'coverage>=4.2',
            'selenium',
            'zope.component>=3.11.0',
        ],
    },
    test_suite="yawarana_grammar",
    entry_points="""\
    [paste.app_factory]
    main = yawarana_grammar:main
""")
