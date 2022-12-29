"""
AM3DB's family module.
"""

from typing import TYPE_CHECKING, List, Optional

from arc.reaction import ARCReaction

if TYPE_CHECKING:
    from rmgpy.reaction import Reaction
    from arc.species import ARCSpecies


class AMReaction(ARCReaction):
    """
    An AM3DB Species class.

    Args:
        label (str, optional): The reaction's label in the format `r1 + r2 <=> p1 + p2`
                               (or unimolecular on either side, as appropriate).
        reactants (List[str], optional): A list of reactant *labels* corresponding to an :ref:`ARCSpecies <species>`.
        products (List[str], optional): A list of product *labels* corresponding to an :ref:`ARCSpecies <species>`.
        r_species (List[ARCSpecies], optional): A list of reactants :ref:`ARCSpecies <species>` objects.
        p_species (List[ARCSpecies], optional): A list of products :ref:`ARCSpecies <species>` objects.
        rmg_reaction (Reaction, optional): An RMG Reaction class.
        multiplicity (int, optional): The reaction surface multiplicity. A trivial guess will be made unless provided.
        charge (int, optional): The reaction surface charge.
        species_list (list, optional): A list of ARCSpecies entries for matching reactants and products
                                       to existing species.

    Attributes:
        label (str): The reaction's label in the format `r1 + r2 <=> p1 + p2`
                     (or unimolecular on either side, as appropriate).
        family (KineticsFamily): The RMG kinetic family, if applicable.
        family_own_reverse (bool): Whether the RMG family is its own reverse.
        reactants (List[str]): A list of reactants labels corresponding to an :ref:`ARCSpecies <species>`.
        products (List[str]): A list of products labels corresponding to an :ref:`ARCSpecies <species>`.
        r_species (List[ARCSpecies]): A list of reactants :ref:`ARCSpecies <species>` objects.
        p_species (List[ARCSpecies]): A list of products :ref:`ARCSpecies <species>` objects.
        rmg_reaction (Reaction): An RMG Reaction class.
        rmg_reactions (list): A list of RMG Reaction objects with RMG rates for comparisons.
        multiplicity (int): The reaction surface multiplicity. A trivial guess will be made unless provided.
        charge (int): The reaction surface charge.
        atom_map (List[int]): An atom map, mapping the reactant atoms to the product atoms.
                              I.e., an atom map of [0, 2, 1] means that reactant atom 0 matches product atom 0,
                              reactant atom 1 matches product atom 2, and reactant atom 2 matches product atom 1.

        id (int): THe reaction ID in the database.
    """

    def __init__(self,
                 label: str = '',
                 reactants: Optional[List[str]] = None,
                 products: Optional[List[str]] = None,
                 r_species: Optional[List['ARCSpecies']] = None,
                 p_species: Optional[List['ARCSpecies']] = None,
                 rmg_reaction: Optional['Reaction'] = None,
                 multiplicity: Optional[int] = None,
                 charge: Optional[int] = None,
                 species_list: Optional[List['ARCSpecies']] = None,
                 ):

        super().__init__(label=label,
                         reactants=reactants,
                         products=products,
                         r_species=r_species,
                         p_species=p_species,
                         rmg_reaction=rmg_reaction,
                         multiplicity=multiplicity,
                         charge=charge,
                         species_list=species_list,
                         )
        self.id = None
