# The in-memory repository will handle object storage and validation.
# It follows a consistent interface that will later be replaced by a
# database-backed repository.
from abc import ABC, abstractmethod
from app import db


class Repository(ABC):
    """Abstract base class for all repositories"""
    
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    """In-memory repository for storing objects"""
    
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None
        )


class SQLAlchemyRepository(Repository):
    """Base repository class for SQLAlchemy ORM operations"""

    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add an object to the database"""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get an object by ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects of this model type"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with the given data"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object by ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Get an object by a specific attribute"""
        return self.model.query.filter_by(
            **{attr_name: attr_value}
        ).first()
