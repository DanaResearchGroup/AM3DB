"""
AM3DB's database module.
"""

from typing import TYPE_CHECKING, List, Optional

from am3db.common import DATABASE_PATH

if TYPE_CHECKING:
    from am3db.reaction import AMReaction


def update_reaction(reaction: 'AMReaction'):
    """
    Update a Reaction in the database.
    """





