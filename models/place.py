#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from os import getenv
from models.base_model import BaseModel, Base
from models.review import Review
from sqlalchemy import Column, String, Table
from sqlalchemy import ForeignKey, Integer, Float
from sqlalchemy.orm import relationship


association_table = Table("place_amenity", Base.metadata,
                          Column("place_id", String(60),
                                 ForeignKey("places.id"),
                                 primary_key=True,
                                 nullable=False),
                          Column("amenity_id", String(60),
                                 ForeignKey("amenities.id"),
                                 primary_key=True,
                                 nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """

    __tablename__ = "places"

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity")

    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def amenities(self):
            """ returns the list of Amenity instances based
            on the attribute amenity_ids that
            contains all Amenity.id linked to the Place. """

            ls = []
            dic = models.storage.all("Amenity").items()
            for key, value in dic:
                if value.id in self.amenity_ids:
                    ls.append(dic[key])

            return ls

        @amenities.setter
        def amenities(self, obj):
            """ handles append method for adding an Amenity.id to
            the attribute amenity_ids. This method should accept
            only Amenity object, otherwise, do nothing. """

            if type(obj).__name__ == "Amenity":
                self.amenity_ids.append(obj.id)
