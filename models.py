from flask import g, current_app, request
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.orm import relationship
from sqlalchemy import Table

from sqlalchemy_oso.flask import AuthorizedSQLAlchemy

db = AuthorizedSQLAlchemy(
    get_oso=lambda: current_app.oso,
    get_user=lambda: getattr(g, "current_user", None),
    get_action=lambda: "read"
)


class ECG(db.Model):
    __tablename__ = 'ecg'

    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Integer)

    created_by_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    created_by = relationship("Patients")

    study_id = db.Column(db.Integer, db.ForeignKey('studies.id'))
    studies = relationship("Studies", backref="ecg")

    description = db.Column(db.Text)


class Studies(db.Model):
    __tablename__ = "studies"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)

    created_by_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
    created_by = relationship("Patients")


patient_study = db.Table(
    "patient_study",
    db.Column('patient_id', db.Integer, db.ForeignKey('patient.id')),
    db.Column('study_id', db.Integer, db.ForeignKey('studies.id'))
)


class Patients(db.Model):
    __tablename__ = 'patients'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256))

    projects = relationship('Studies', secondary=patient_study,
                            backref="patients")