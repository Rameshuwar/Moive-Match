"""Add database integrity constraints

Revision ID: 239d1543b06f
Revises: b47d2b1a6fd2
Create Date: 2026-10-05 09:53:38.156570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '239d1543b06f'
down_revision: Union[str, Sequence[str], None] = 'b47d2b1a6fd2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_check_constraint(
        "ck_movies_duration_positive",
        "movies",
        "duration_minutes > 0",
    )

    op.create_check_constraint(
        "ck_show_prices_ticket_price_positive",
        "show_prices",
        "ticket_price > 0",
    )

    op.create_check_constraint(
        "ck_show_prices_available_seats_nonnegative",
        "show_prices",
        "available_seats >= 0",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(
        "ck_show_prices_available_seats_nonnegative",
        "show_prices",
        type_="check",
    )

    op.drop_constraint(
        "ck_show_prices_ticket_price_positive",
        "show_prices",
        type_="check",
    )

    op.drop_constraint(
        "ck_movies_duration_positive",
        "movies",
        type_="check",
    )