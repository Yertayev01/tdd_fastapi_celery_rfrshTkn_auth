from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float, ForeignKey, func, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'tb_user_info'

    USER_MNG_ID = Column(BigInteger, primary_key=True, nullable=False, comment='사용자 관리 ID')
    USCL_CD = Column(String(8), nullable=False, default='USCL0001', comment='사용자 코드')
    LOGI_CD = Column(String(8), nullable=False, default='LOGI0001', comment='소설로그인 코드')
    USER_ID = Column(String(100), nullable=False, comment='사용자 ID')
    PSSWRD = Column(String(100), nullable=False, comment='비밀번호')
    USER_NM = Column(String(50), nullable=False, comment='사용자명')
    DISPLAY_NM = Column(String(50), comment='보이는 이름')
    EMAIL = Column(String(255), nullable=False, comment='이메일')
    PHONE_NO = Column(String(255), comment='휴대전화번호')
    LOGIN_DT = Column(DateTime, default=func.now(), comment='로그인 일시')
    PSSWRD_ERR_NT = Column(Integer, default=0, comment='비밀번호 오류 횟수')
    PSSWRD_LAST_CHANGE_DT = Column(DateTime, default=func.now(), comment='패스워드 마지막 변경일시')
    USE_YN = Column(String(1), nullable=False, default='Y', comment='사용 여부')
    DEL_YN = Column(String(1), nullable=False, default='N', comment='삭제 여부')
    REG_USER_ID = Column(String(100), nullable=False, comment='생성 아이디')
    REG_DT = Column(DateTime, nullable=False, default=func.now(), comment='생성일시')
    MOD_USER_ID = Column(String(100), nullable=False, comment='수정 아이디')
    MOD_DT = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now(), comment='수정일시')

