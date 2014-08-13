# coding: utf-8
from sqlalchemy import Column, Integer, DateTime, Float, ForeignKey
from models import Base


class ItemsCarts(Base):
    __tablename__ = 'items_carts'

    id          = Column(Integer, primary_key=True)
    carts_id    = Column(Integer, ForeignKey('carts.id'), nullable=False)
    variant_id  = Column(Integer, ForeignKey('variants.id'), nullable=False)
    cnt         = Column(Integer)
    price       = Column(Float)
    cost        = Column(Float)
    added       = Column(DateTime)