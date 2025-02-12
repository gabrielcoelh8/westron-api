from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.database.meta.declarative_base import postgres_base
from app.database.meta.schema import schema


class ExtratoBancario(postgres_base):
    __tablename__ = 'extrato_bancario'
    __table_args__ = (
        UniqueConstraint('tipo', 'instituicao_financeira_id', name='uq_tipo_instituicao_financeira_id'),
        {'schema': schema}
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tipo: Mapped[str] = mapped_column(nullable=False)
    instituicao_financeira_id: Mapped[int] = mapped_column(
        ForeignKey(f'{schema}.instituicao_financeira.id'), nullable=False
    )

    instituicao_financeira: Mapped['InstituicaoFinanceira'] = relationship(
        'InstituicaoFinanceira',
        back_populates='extratos_bancarios'
    )
    aliases_extrato_bancario: Mapped[list['ExtratoBancarioAlias']] = relationship(
        'ExtratoBancarioAlias',
        back_populates='extrato_bancario'
    )
    prompts_extrato_bancario: Mapped[list['PromptExtratoBancario']] = relationship(
        'PromptExtratoBancario',
        back_populates='extrato_bancario'
    )

    @validates('tipo')
    def validate_tipo(self, key, value):
        if not value or value.strip() == '':
            raise ValueError('O campo \'tipo\' não pode ser uma string vazia.')
        return value
