#coding:utf-8
from sqlalchemy import Column, String, Integer
import sqlalchemy.exc

from db import Base, Session
from util.log import logger

class UserSms(Base):
    __tablename__ = 'ci_user_sms'

    sid = Column(Integer, primary_key=True, autoincrement=True)
    identifier = Column(String(255), nullable=False)
    status = Column(Integer, nullable=False, default=1)
    valid = Column(Integer, nullable=False, default=1)

    def __init__(self, sid, status, valid=1, identifier=''):
        self.sid = sid
        self.status = status
        self.identifier = identifier
        self.valid = valid

    @classmethod
    def update(cls, sid, status, valid=1, identifier=''):
        try:
            r = Session.query(cls).filter(cls.sid == sid).first()
            if r:
                r.identifier = identifier
                r.status = status
                r.valid = valid
                Session.add(r)
                Session.commit()
            return r
        except sqlalchemy.exc.IntegrityError, e:
            Session.rollback()
            logger.warning('msg[update %s error] e[%s]' % (__tablename__, e))
            return None
