from sqlalchemy.orm import Session
from models import Machine, Process, Label, SpindleLoadData


def get_machine_by_number(db: Session, machine_number: str):
    return db.query(Machine).filter(Machine.machine_number == machine_number).first()


def get_or_create_machine(db: Session, machine_number: str):
    machine = get_machine_by_number(db, machine_number)
    if not machine:
        machine = Machine(machine_number=machine_number)
        db.add(machine)
        db.commit()
        db.refresh(machine)
    return machine.id


def get_process_by_number(db: Session, process_number: str):
    return db.query(Process).filter(Process.process_number == process_number).first()


def get_or_create_process(db: Session, process_number: str):
    process = get_process_by_number(db, process_number)
    if not process:
        process = Process(process_number=process_number)
        db.add(process)
        db.commit()
        db.refresh(process)
    return process.id


def get_label_by_text(db: Session, label_text: str):
    return db.query(Label).filter(Label.label == label_text).first()


def get_or_create_label(db: Session, label_text: str):
    label = get_label_by_text(db, label_text)
    if not label:
        label = Label(label=label_text)
        db.add(label)
        db.commit()
        db.refresh(label)
    return label.id


def create_spindle_load_data(db: Session, machine_id: int, process_id: int, label_id: int, filename: str, data_blob: bytes):
    db_data = SpindleLoadData(
        machine_id=machine_id,
        process_id=process_id,
        label_id=label_id,
        filename=filename,
        data=data_blob
    )
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return db_data


def get_spindle_load_data(session: Session, machine_number: str, process_number: str, label: str):
    """
    Retrieve spindle load data from the database based on machine number, process number, and label.
    """
    return session.query(SpindleLoadData
        ).join(Machine, SpindleLoadData.machine_id == Machine.id
        ).join(Process, SpindleLoadData.process_id == Process.id
        ).join(Label, SpindleLoadData.label_id == Label.id
        ).filter(
            Machine.machine_number == machine_number,
            Process.process_number == process_number,
            Label.label == label
        ).all()