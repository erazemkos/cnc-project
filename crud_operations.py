from sqlalchemy.orm import Session
from models import Machine, Process, Label, SpindleLoadData, Base
from typing import Optional
from sqlalchemy import create_engine
from constants import DATABASE_URL


class DatabaseHandler:
    def __init__(self, session: Session):
        self._db = session

    def _get_machine_by_number(self, machine_number: int) -> Optional[Machine]:
        return self._db.query(Machine).filter(Machine.machine_number == machine_number).first()

    def get_or_create_machine(self, machine_number: int) -> int:
        machine = self._get_machine_by_number(machine_number)
        if not machine:
            machine = Machine(machine_number=machine_number)
            self._db.add(machine)
            self._db.commit()
            self._db.refresh(machine)
        return machine.id

    def _get_process_by_number(self, process_number: int) -> Optional[Process]:
        return self._db.query(Process).filter(Process.process_number == process_number).first()

    def get_or_create_process(self, process_number: int) -> int:
        process = self._get_process_by_number(process_number)
        if not process:
            process = Process(process_number=process_number)
            self._db.add(process)
            self._db.commit()
            self._db.refresh(process)
        return process.id

    def _get_label_by_text(self, label_text: str) -> Optional[Label]:
        return self._db.query(Label).filter(Label.label == label_text).first()

    def get_or_create_label(self, label_text: str) -> int:
        label = self._get_label_by_text(label_text)
        if not label:
            label = Label(label=label_text)
            self._db.add(label)
            self._db.commit()
            self._db.refresh(label)
        return label.id

    def create_spindle_load_data(self, machine_id: int, process_id: int,
                                 label_id: int, filename: str, data_blob: bytes) -> Optional[SpindleLoadData]:
        db_data = SpindleLoadData(
            machine_id=machine_id,
            process_id=process_id,
            label_id=label_id,
            filename=filename,
            data=data_blob
        )
        self._db.add(db_data)
        self._db.commit()
        self._db.refresh(db_data)
        return db_data

    def get_spindle_load_data(self, machine_number: str, process_number: str, label: str):
        """
        Retrieve spindle load data from the database based on machine number, process number, and label.
        """
        return self._db.query(SpindleLoadData
            ).join(Machine, SpindleLoadData.machine_id == Machine.id
            ).join(Process, SpindleLoadData.process_id == Process.id
            ).join(Label, SpindleLoadData.label_id == Label.id
            ).filter(
                Machine.machine_number == machine_number,
                Process.process_number == process_number,
                Label.label == label
            ).all()


def create_db_handler() -> DatabaseHandler:
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    return DatabaseHandler(Session(engine))
