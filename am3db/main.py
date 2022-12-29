"""
AM3DB's main module.
"""

import datetime
import os
import time
import random
from enum import Enum
from IPython.display import display
from typing import Dict, List, Optional, Tuple, Union

from arc.rmgdb import make_rmg_database_object, load_families_only

from am3db.logger import Logger
from am3db.reaction import AMReaction


class AM3DB(object):
    """
    The main AM3DB class.

    Args:
        user (str): The username.
        project (str, optional): A project name.
        families (Union[str, List[str]], optional): The families to load.

    Attributes:
        user (str): The username.
        project (str): A project name.
        logger (Logger): The AM3DB Logger object instance.
    """

    def __init__(self,
                 user: str,
                 project: str = 'update AM3DB',
                 families: Union[str, List[str]] = 'default',
                 ):

        self.user = user
        self.project = project
        self.logger = Logger(user=self.user,
                             project=self.project,
                             )
        self.rmgdb = make_rmg_database_object()
        load_families_only(self.rmgdb, kinetics_families=families)

    def generate_family_reactions(self,
                                  family_label: str,
                                  num: Optional[int] = None,
                                  mode: str = 'training',
                                  ) -> list:
        """
        Generate reactions for a specific family.

        Args:
            family_label (str): The label of the desired family.
            num (int, optional): The number of reactions to return.
                                 If ``num`` is ``None`` and ``mode`` is 'training', returns all training reactions.
            mode (str, optional): Whether to return training reactions (by default) or new randomly-generated reactions.

        Returns:
            list: The respective RMG reactions.
        """
        if mode != 'training':
            raise NotImplemented('Only "training" mode is implemented')
        if num is None and mode != 'training':
            raise ValueError('num can only be None for "training" mode')
        rmg_rxns = list()
        if mode == 'training':
            num_training_rxns = len(self.rmgdb.kinetics.families[family_label].depositories[0].entries)
            if num is None or num > num_training_rxns:
                rmg_rxns = self.rmgdb.kinetics.families[family_label].depositories[0].entries.values()
                rmg_rxns = [entry.item for entry in rmg_rxns]
            else:
                indices = list()
                while len(indices) < num:
                    index = random.randint(0, len(self.rmgdb.kinetics.families[family_label].depositories[0].entries) - 1)
                    if index not in indices:
                        indices.append(index)
                for index in indices:
                    if index in self.rmgdb.kinetics.families[family_label].depositories[0].entries.keys():
                        rmg_rxns.append(self.rmgdb.kinetics.families[family_label].depositories[0].entries[index].item)
        return rmg_rxns


def generate_am_reactions_from_rmg_reactions(rmg_rxns: list,
                                             ) -> list:
    """
    Generate AMReaction objects corresponding to RMG Reaction object instances.

    Args:
         rmg_rxns (list): RMG Reaction object instances.

    Returns:
        list: Corresponding AMReaction object instances.
    """
    am_rxns = list()
    for rmg_rxn in rmg_rxns:
        am_rxn = AMReaction(rmg_reaction=rmg_rxn,
                            reactants=[spc.molecule[0].to_smiles() for spc in rmg_rxn.reactants],
                            products=[spc.molecule[0].to_smiles() for spc in rmg_rxn.products],
                            )
        for spc in am_rxn.r_species + am_rxn.p_species:
            spc.generate_conformers(n_confs=1)
            spc.initial_xyz = spc.final_xyz = spc.conformers[0]
        am_rxns.append(am_rxn)
    return am_rxns































