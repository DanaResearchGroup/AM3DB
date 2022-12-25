"""
AM3DB's reaction module.
"""
import os.path
from typing import TYPE_CHECKING, List, Optional

from arc.common import generate_resonance_structures, read_yaml_file, save_yaml_file
from arc.reaction import ARCReaction
from arc.rmgdb import determine_family
from arc.species.mapping import get_atom_indices_of_labeled_atoms_in_an_rmg_reaction, get_rmg_reactions_from_arc_reaction

from am3db.common import DATABASE_PATH
from am3db.user import get_user_from_file

if TYPE_CHECKING:
    from rmgpy.reaction import Reaction
    from arc.species import ARCSpecies


MAX_RXNS_PER_FILE = 500


class AMReaction(ARCReaction):
    """
    An AM3DB Reaction class.

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
        index (int, optional): The reaction ID in the database.

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

        index (int): The reaction ID in the database.
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
                 index: Optional[int] = None,
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
        self._index = index
        determine_family(reaction=self)
        self.approved_by = None
        self.rejected_by = None
        self.rejected_reasons = list()
        self.clustering = list()

    @property
    def index(self) -> Optional[int]:
        """The reaction ID"""
        if self._index is None and self.family is not None:
            family_files = get_all_family_files(self.family.label)
            if not len(family_files):
                self._index = 0
            else:
                max_fam_num, max_fam_file = -1, ''
                for family_file in family_files:
                    fam_num = int(family_file.split('.')[0].split('_')[-1])
                    if fam_num > max_fam_num:
                        max_fam_num = fam_num
                        max_fam_file = family_file
                if max_fam_file:
                    reactions = read_yaml_file(os.path.join(DATABASE_PATH, 'reactions', max_fam_file))
                    max_index = -1
                    for reaction in reactions:
                        if reaction['index'] > max_index:
                            max_index = reaction['index']
                    self._index = max_index + 1
        return self._index

    @index.setter
    def index(self, value):
        """Allow setting the reaction ID"""
        self._index = value

    def approve(self, name: str):
        """
        Approve the 3D atom-mapping of a Reaction.

        Args:
            name (str): The username of the reviewer.
        """
        user = get_user_from_file(name=name)
        if user is None:
            print(f'Not approving this reaction.')
            return
        self.approved_by = self.approved_by or list()
        if self.rejected_by is not None:
            if user.status.value == 'admin':
                self.rejected_by = None
        self.approved_by.append(user.name)

    def reject(self,
               name: str,
               reason: str,
               ):
        """
        Reject the 3D atom-mapping of a Reaction.

        Args:
            name (str): The username of the reviewer.
            reason (str): The reason for rejecting this reaction.
        """
        user = get_user_from_file(name=name)
        if user is None:
            print(f'Not rejecting this reaction.')
            return
        self.rejected_by = self.rejected_by or list()
        self.rejected_by.append(user.name)
        self.rejected_reasons.append(reason)

    def save(self, database_path: Optional[str] = None):
        """
        Save the Reaction object instance in the database.
        Atom_maps are saves as a list, their structure is List[List[List[int]]],
        entries of the first list are lists of atom-maps,
        each first list entry represents collection of equivalent atom-maps,
        all entries together represent the comprehensive orthogonal 3D atom-maps.
        """
        if self.family is None:
            print('Error: Cannot save a reaction without identifying its family.')
            return None
        set_up_folders()
        family_file_name = determine_family_filename_by_index(index=self.index, family=self.family.label)
        family_file_path = os.path.join(database_path or DATABASE_PATH, 'reactions', family_file_name)
        file_content = read_yaml_file(family_file_path) or dict()
        file_content[self.index] = self.as_db_dict()
        save_yaml_file(family_file_path, file_content)

    def as_db_dict(self):
        """A dictionary representation of the object for the database."""
        try:
            r_inchi_keys = [r.mol.to_inchi_key() for r in self.r_species]
        except:
            r_inchi_keys = list()
        try:
            p_inchi_keys = [p.mol.to_inchi_key() for p in self.p_species]
        except:
            p_inchi_keys = list()

        r_adjacency_lists, p_adjacency_lists = list(), list()
        if all(spc.mol is not None for spc in self.r_species):
            for spc in self.r_species:
                mols = generate_resonance_structures(spc.mol)
                r_adjacency_lists.append([mol.to_adjacency_list() for mol in mols or [spc.mol]])
        if all(spc.mol is not None for spc in self.p_species):
            for spc in self.p_species:
                mols = generate_resonance_structures(spc.mol)
                p_adjacency_lists.append([mol.to_adjacency_list() for mol in mols or [spc.mol]])

        reactant_index_dict, product_index_dict = None, None
        rmg_reactions = get_rmg_reactions_from_arc_reaction(arc_reaction=self, backend='ARC')
        if rmg_reactions is not None:
            for rmg_reaction in rmg_reactions:
                reactant_index_dict, product_index_dict = \
                    get_atom_indices_of_labeled_atoms_in_an_rmg_reaction(arc_reaction=self, rmg_reaction=rmg_reaction)

        for spc in self.r_species + self.p_species:
            spc.initial_xyz = spc.initial_xyz or spc.get_xyz()  # Important to initialize to get a 3D atom-map.
        r_xyz = [r.get_xyz() for r in self.r_species]
        p_xyz = [p.get_xyz() for p in self.p_species]
        atom_maps = self.atom_map
        if atom_maps is not None:
            atom_maps = [atom_maps] if isinstance(atom_maps[0], int) else atom_maps

        return {'multiplicity': self.multiplicity,  # int
                'charge': self.charge,  # int
                'r_inchi_keys': r_inchi_keys,  # List[str]
                'p_inchi_keys': p_inchi_keys,  # List[str]
                'r_adjacency_lists': r_adjacency_lists,  # List[List[str]], all rep. resonance structures per species
                'p_adjacency_lists': p_adjacency_lists,  # List[List[str]], all rep. resonance structures per species
                'r_xyz': r_xyz,  # List[dict]
                'p_xyz': p_xyz,  # List[dict]
                'r_rmg_labels': reactant_index_dict,  # Dict[str, int]
                'p_rmg_labels': product_index_dict,  # Dict[str, int]
                'atom_maps': atom_maps,  # List[List[int]]
                'clustering': self.clustering,  # List[List[int]]
                'approved_by': self.approved_by,  # List[str]
                'rejected_by': self.rejected_by,  # List[str]
                'rejected_reasons': self.rejected_reasons,  # List[str]
                }


def set_up_folders():
    """
    Set up the database folders upon first usage.
    """
    reactions_path = os.path.join(DATABASE_PATH, 'reactions')
    if not os.path.isdir(reactions_path):
        os.makedirs(reactions_path)


def get_all_family_files(family: str,
                         reactions_path: str = '',
                         ) -> List[str]:
    """
    Get all database files for a given family.

    Args:
         family (str): The family label.
         reactions_path (str, optional): The path to the database reactions folder.

    Returns:
        List[str]: The filenames representing this family in the database.
    """
    reactions_path = reactions_path or os.path.join(DATABASE_PATH, 'reactions')
    file_names, family_files = list(), list()
    for (_, _, files) in os.walk(reactions_path):
        file_names.extend(files)
        break  # Don't continue to explore subdirectories.
    for file_name in file_names:
        if family in file_name:
            family_files.append(file_name)
    return family_files


def determine_family_filename_by_index(index: int,
                                       family: str,
                                       ) -> str:
    """
    Determine the family filename in the database by the reaction ID.

    Args:
        index (int): The reaction ID in the database.
        family (str): The reaction family label.
    """
    num = int(index / MAX_RXNS_PER_FILE)
    return f'{family}_{num}.yml'
