import os
from abc import ABC, abstractmethod
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from database_utils.constants import DATABASE_UTILS_PATH, SQLITE_PREFIX, DATABASE_NAME
from database_utils.models import Machine, Process, Label, SpindleLoadData, Base


class IDatabaseHandler(ABC):
    @abstractmethod
    def get_or_create_machine(self, machine_name: str) -> int:
        """ Creates a new machine id or just queries it if it already exists """
        pass

    @abstractmethod
    def get_or_create_process(self, process_name: str) -> int:
        """ Creates a new process id or just queries it if it already exists """
        pass

    @abstractmethod
    def get_or_create_label(self, label_text: str) -> int:
        """ Creates a new label or just queries it if it already exists """
        pass

    @abstractmethod
    def create_spindle_load_data(self, machine_id: int, process_id: int, label_id: int, filename: str, data_blob: bytes):
        """ Creates SpindleLoadData in db """
        pass

    @abstractmethod
    def get_spindle_load_data(self, machine_name: str, process_name: str, label: str):
        """ Queries specific SpindleLoadData in db """
        pass


class DatabaseHandler(IDatabaseHandler):
    def __init__(self, session: Session):
        self._db = session

    def _get_machine_by_number(self, machine_name: str) -> Optional[Machine]:
        """ Returns a sql alchemy Machine model specified by name if it exists """
        return self._db.query(Machine).filter(Machine.machine_name == machine_name).first()

    def get_or_create_machine(self, machine_name: str) -> int:
        """ See base class """
        machine = self._get_machine_by_number(machine_name)
        if not machine:
            machine = Machine(machine_name=machine_name)
            self._db.add(machine)
            self._db.commit()
            self._db.refresh(machine)
        return machine.id

    def _get_process_by_number(self, process_name: str) -> Optional[Process]:
        """ Returns a sql alchemy Process model specified by name if it exists """
        return self._db.query(Process).filter(Process.process_name == process_name).first()

    def get_or_create_process(self, process_name: str) -> int:
        """ See base class """
        process = self._get_process_by_number(process_name)
        if not process:
            process = Process(process_name=process_name)
            self._db.add(process)
            self._db.commit()
            self._db.refresh(process)
        return process.id

    def _get_label_by_text(self, label_text: str) -> Optional[Label]:
        """ Returns a sql alchemy Label model specified by name if it exists """
        return self._db.query(Label).filter(Label.label == label_text).first()

    def get_or_create_label(self, label_text: str) -> int:
        """ See base class """
        label = self._get_label_by_text(label_text)
        if not label:
            label = Label(label=label_text)
            self._db.add(label)
            self._db.commit()
            self._db.refresh(label)
        return label.id

    def create_spindle_load_data(self, machine_id: int, process_id: int,
                                 label_id: int, filename: str, data_blob: bytes) -> Optional[SpindleLoadData]:
        """ See base class """
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

    def get_spindle_load_data(self, machine_name: str, process_name: str, label: str):
        """ See base class """
        return self._db.query(SpindleLoadData
            ).join(Machine, SpindleLoadData.machine_id == Machine.id
            ).join(Process, SpindleLoadData.process_id == Process.id
            ).join(Label, SpindleLoadData.label_id == Label.id
            ).filter(
                Machine.machine_name == machine_name,
                Process.process_name == process_name,
                Label.label == label
            ).all()


def create_db_handler(handler_type: str = "sql_alchemy") -> IDatabaseHandler:
    """ Factory method for creating ORM objects """
    if handler_type == "sql_alchemy":
        # Determine where we are
        if os.path.basename(os.getcwd()) == DATABASE_UTILS_PATH:
            database_url = f"{SQLITE_PREFIX}./{DATABASE_NAME}"
        else:
            database_url = f"{SQLITE_PREFIX}./{DATABASE_UTILS_PATH}/{DATABASE_NAME}"

        engine = create_engine(database_url)
        Base.metadata.create_all(bind=engine)
        return DatabaseHandler(Session(engine))
    else:
        raise NotImplementedError("Handler type {handler_type} not implemented.")
