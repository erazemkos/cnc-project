from sqlalchemy import Column, ForeignKey, Integer, String, BLOB, DateTime, func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Machine(Base):
    __tablename__ = 'machines'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_number = Column(String, nullable=False)
    
    # Relationship to spindle_load_data
    spindle_load_data = relationship('SpindleLoadData', back_populates='machine')

class Process(Base):
    __tablename__ = 'processes'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    process_number = Column(String, nullable=False)
    
    # Relationship to spindle_load_data
    spindle_load_data = relationship('SpindleLoadData', back_populates='process')

class Label(Base):
    __tablename__ = 'labels'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String, nullable=False)
    
    # Relationship to spindle_load_data
    spindle_load_data = relationship('SpindleLoadData', back_populates='label')

class SpindleLoadData(Base):
    __tablename__ = 'spindle_load_data'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    machine_id = Column(Integer, ForeignKey('machines.id'), nullable=False)
    process_id = Column(Integer, ForeignKey('processes.id'), nullable=False)
    label_id = Column(Integer, ForeignKey('labels.id'), nullable=False)
    filename = Column(String, nullable=False)
    data = Column(BLOB)  # .h5 data will be stored as a binary large object
    timestamp = Column(DateTime, default=func.current_timestamp())
    
    # Relationships to machine, process, and label
    machine = relationship('Machine', back_populates='spindle_load_data')
    process = relationship('Process', back_populates='spindle_load_data')
    label = relationship('Label', back_populates='spindle_load_data')

