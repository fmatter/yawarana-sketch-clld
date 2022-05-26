from yawarana_grammar import models
from clld.db.meta import DBSession
from clld.cliutil import Data, bibtex2source


def main(args):
    data = Data()
    data.add(
        models.Document,
        "tsam",
        id="tsam",
        name="Notes: TAM suffixes",
        description=open(
            "/home/florianm/Dropbox/research/cariban/yawarana/yaw_notes/clld_output.txt",
            "r",
        ).read(),
    )
    print("good")
    print(data)


if __name__ == "__main__":
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
