#!/usr/bin/env python3
# encoding: utf-8

"""
AM3DB tests test_main module
"""

from rmgpy.reaction import Reaction

from am3db.main import AM3DB, generate_am_reactions_from_rmg_reactions
from am3db.reaction import AMReaction


def test_generate_family_reactions():
    """Test the generate_family_reactions() method."""
    db = AM3DB(user='developer')
    rmg_rxns = db.generate_family_reactions(family_label='1,3_NH3_elimination')
    assert len(rmg_rxns) > 3
    for rmg_rxn in rmg_rxns:
        assert isinstance(rmg_rxn, Reaction)

    rmg_rxns = db.generate_family_reactions(family_label='H_Abstraction', num=10)
    assert len(rmg_rxns) == 10
    for rmg_rxn in rmg_rxns:
        assert isinstance(rmg_rxn, Reaction)


def test_generate_am_reactions_from_rmg_reactions():
    """Test the generate_am_reactions_from_rmg_reactions() function"""
    db = AM3DB(user='developer')
    rmg_rxns = db.generate_family_reactions(family_label='1,3_Insertion_CO2')
    am_rxns = generate_am_reactions_from_rmg_reactions(rmg_rxns)
    assert len(am_rxns) == len(rmg_rxns) == 8
    for am_rxn in am_rxns:
        assert isinstance(am_rxn, AMReaction)








