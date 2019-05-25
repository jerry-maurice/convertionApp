from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime
from sqlalchemy import Float, Text, Boolean, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)

import random, string, datetime



Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase +
                                   string.digits) for x in range(32))

''' About User'''
class User(Base):
    # store user info
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    picture = Column(String(250))
    title = Column(String(50))
    email = Column(String(250), index=True)
    firstName = Column(String(250), nullable=False)
    lastName = Column(String(250), nullable=False)
    password_hash = Column(String(250), nullable=False)
    transaction = relationship('Transaction', backref='User')

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id':self.id})

    def is_active(self):
        return True

    def get_id(self):
        return self.email

    def is_authenticated(self):
        return self.authenticated

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(secret_key)
        try:
            data=s.loads(token)
        except SignatureExpired:
            # Valid token but expired
            return None
        except BadSignature:
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        return{
            'id':self.id,
            'email':self.email,
            'title':self.title,
            'firstName':self.firstName,
            'lastName':self.lastName,
            'picture':self.picture
            }


''' about transaction '''
class Transaction(Base):
    # store transaction
    __tablename__ = 'transaction'
    id = Column(Integer, primary_key=True)
    transferDate = Column(DateTime, default=datetime.datetime.utcnow)
    usAmount = Column(Float, nullable=False)
    gdAmount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    comment = Column(Text)
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        return{
            'id':self.id,
            'transferDate':self.transferDate,
            'usAmount':self.usAmount,
            'gdAmount':self.gdAmount,
            'rate':self.rate,
            'comment':self.comment,
            'user_id':self.user_id
            }


''' about rate '''
class Rate(Base):
    # store rate
    __tablename__ = 'rate'
    id = Column(Integer, primary_key=True)
    convertRate = Column(Float, nullable=False)

    @property
    def serialize(self):
        return{
            'id':self.id,
            'convertRate':self.convertRate
            }


engine = create_engine('mysql+pymysql://root:Bank2427249@localhost/transfer', pool_pre_ping=True)
Base.metadata.create_all(engine)

