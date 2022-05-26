from pathlib import Path

from clld.web.assets import environment

import yawarana_grammar


environment.append_path(
    Path(yawarana_grammar.__file__).parent.joinpath("static").as_posix(),
    url="/yawarana_grammar:static/",
)
environment.load_path = list(reversed(environment.load_path))
