import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String(250))

    @property
    def serialize(self):
        return{
            'name': self.name,
            'id': self.id,
            'email': self.email,
            'picture': self.picture
            }


class Country(Base):
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.id
            }


class State(Base):
    __tablename__ = 'state'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    about = Column(String(250))
    State_capital = Column(String(250))
    State_culture = Column(String(250))
    State_population = Column(Integer)
    State_Language = Column(String(250))
    State_area = Column(String(250))
    districts = Column(Integer)
    state_id = Column(Integer, ForeignKey('country.id'))
    country = relationship(Country)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'about': self.about,
            'id': self.id,
            'State_capital': self.State_capital,
            'State_culture': self.State_culture,
            'State_population': self.State_population,
            'State_Language': self.State_Language,
            'State_area': self.State_area,
            'districts': self.districts,
            'state_id': self.state_id
            }

engine = create_engine('sqlite:///stateslist.db')
Base.metadata.create_all(engine)
