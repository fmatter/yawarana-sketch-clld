from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models import common, IdNameDescriptionMixin
from clld.db.meta import PolymorphicBaseMixin

from yawarana_sketch_clld.interfaces import IPhoneme
from clld_morphology_plugin.models import Wordform

# -----------------------------------------------------------------------------
# specialized common mapper classes
# -----------------------------------------------------------------------------


@implementer(IPhoneme)
class Phoneme(Base, IdNameDescriptionMixin):
    pass


class FormPhoneme(Base, PolymorphicBaseMixin):
    phoneme_pk = Column(Integer, ForeignKey("phoneme.pk"), nullable=False)
    form_pk = Column(Integer, ForeignKey("wordform.pk"), nullable=False)
    phoneme = relationship(Phoneme, innerjoin=True, backref="forms")
    form = relationship(Wordform, innerjoin=True, backref="segments")
