from sqlalchemy.orm import Session
from .models import Machine, Process, Label, SpindleLoadData
import h5py
import io

def get_machine_by_number(db: Session, machine_number: str):
    return db.query(Machine).filter(Machine.machine_number == machine_number).first()

def get_process_by_number(db: Session, process_number: str):
    return db.query(Process).filter(Process.process_number == process_number).first()

def get_label_by_text(db: Session, label_text: str):
    return db.query(Label).filter(Label.label == label_text).first()

def create_machine(db: Session, machine_number: str):
    db_machine = Machine(machine_number=machine_number)
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine

def create_process(db: Session, process_number: str):
    db_process = Process(process_number=process_number)
    db.add(db_process)
    db.commit()
    db.refresh(db_process)
    return db_process

def create_label(db: Session, label_text: str):
    db_label = Label(label=label_text)
    db.add(db_label)
    db.commit()
    db.refresh(db_label)
    return db_label

def create_spindle_load_data(db: Session, machine_id: int, process_id: int, label_id: int, filename: str, data):
    db_data = SpindleLoadData(
        machine_id=machine_id,
        process_id=process_id,
        label_id=label_id,
        filename=filename,
        data=data
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data

def add_spindle_load_data(db: Session, machine_number: str, process_number: str, label_text: str, filename: str, file_path: str):
    machine = get_machine_by_number(db, machine_number)
    if not machine:
        machine = create_machine(db, machine_number)
    
    process = get_process_by_number(db, process_number)
    if not process:
        process = create_process(db, process_number)
    
    label = get_label_by_text(db, label_text)
    if not label:
        label = create_label(db, label_text)
    
    with h5py.File(file_path, 'rb') as file:
        binary_data = io.BytesIO(file.read()).getvalue()
    
    return create_spindle_load_data(db, machine.id, process.id, label.id, filename, binary_data)

def get_all_spindle_load_data(db: Session):
    return db.query(SpindleLoadData).all()

def get_spindle_load_data_by_machine(db: Session, machine_number: str):
    machine = get_machine_by_number(db, machine_number)
    if machine:
        return db.query(SpindleLoadData).filter(SpindleLoadData.machine_id == machine.id).all()
    return []

def get_spindle_load_data_by_process(db: Session, process_number: str):
    process = get_process_by_number(db, process_number)
    if process:
        return db.query(SpindleLoadData).filter(SpindleLoadData.process_id == process.id).all()
    return []

def get_spindle_load_data_by_label(db: Session, label_text: str):
    label = get_label_by_text(db, label_text)
    if label:
        return db.query(SpindleLoadData).filter(SpindleLoadData.label_id == label.id).all()
    return []

