"""aw_test

Revision ID: 52d5eb6dfd04
Revises: 
Create Date: 2024-06-25 15:06:55.820990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '52d5eb6dfd04'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        'tb_user_info',
        sa.Column('USER_MNG_ID', sa.BigInteger, primary_key=True, nullable=False, comment='사용자 관리 ID'),
        sa.Column('USCL_CD', sa.String(8), nullable=False, default='USCL0001', comment='사용자 코드'),
        sa.Column('LOGI_CD', sa.String(8), nullable=False, default='LOGI0001', comment='소설로그인 코드'),
        sa.Column('USER_ID', sa.String(100), nullable=False, comment='사용자 ID'),
        sa.Column('PSSWRD', sa.String(100), nullable=False, comment='비밀번호'),
        sa.Column('USER_NM', sa.String(50), nullable=False, comment='사용자명'),
        sa.Column('DISPLAY_NM', sa.String(50), comment='보이는 이름'),
        sa.Column('EMAIL', sa.String(255), nullable=False, comment='이메일'),
        sa.Column('PHONE_NO', sa.String(255), comment='휴대전화번호'),
        sa.Column('LOGIN_DT', sa.DateTime, default=sa.func.now(), comment='로그인 일시'),
        sa.Column('PSSWRD_ERR_NT', sa.Integer, default=0, comment='비밀번호 오류 횟수'),
        sa.Column('PSSWRD_LAST_CHANGE_DT', sa.DateTime, default=sa.func.now(), comment='패스워드 마지막 변경일시'),
        sa.Column('USE_YN', sa.String(1), nullable=False, default='Y', comment='사용 여부'),
        sa.Column('DEL_YN', sa.String(1), nullable=False, default='N', comment='삭제 여부'),
        sa.Column('REG_USER_ID', sa.String(100), nullable=False, comment='생성 아이디'),
        sa.Column('REG_DT', sa.DateTime, nullable=False, default=sa.func.now(), comment='생성일시'),
        sa.Column('MOD_USER_ID', sa.String(100), nullable=False, comment='수정 아이디'),
        sa.Column('MOD_DT', sa.DateTime, nullable=False, default=sa.func.now(), onupdate=sa.func.now(), comment='수정일시')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tb_user_info')
    # ### end Alembic commands ###