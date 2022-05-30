from pathlib import Path

from clld.web.assets import environment

import yawarana_sketch_clld


environment.append_path(
    Path(yawarana_sketch_clld.__file__).parent.joinpath("static").as_posix(),
    url="/yawarana_sketch_clld:static/",
)
environment.load_path = list(reversed(environment.load_path))
