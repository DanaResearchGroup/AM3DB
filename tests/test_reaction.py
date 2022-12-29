#!/usr/bin/env python3
# encoding: utf-8

"""
AM3DB tests test_reaction module
"""

import os
import shutil

from arc.common import read_yaml_file
from arc.species import ARCSpecies

import am3db.reaction as reaction
from am3db.common import AM3DB_PATH
from am3db.reaction import AMReaction


def test_get_all_family_files():
    """Test the get_all_family_files() function."""
    test_data_path = os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions')
    family_files = reaction.get_all_family_files(family='H_Abstraction', reactions_path=test_data_path)
    assert family_files == ['H_Abstraction_0.yml']
    family_files = reaction.get_all_family_files(family='intra_H_migration', reactions_path=test_data_path)
    assert len(family_files) == 2
    assert 'intra_H_migration_0.yml' in family_files
    assert 'intra_H_migration_1.yml' in family_files
    family_files = reaction.get_all_family_files(family='R_Addition_MultipleBond', reactions_path=test_data_path)
    assert family_files == []


def test_determine_family_filename_by_index():
    """Test the determine_family_filename_by_index() function."""
    assert reaction.determine_family_filename_by_index(5, 'fam') == 'fam_0.yml'
    assert reaction.determine_family_filename_by_index(505, 'fam') == 'fam_1.yml'
    assert reaction.determine_family_filename_by_index(1005, 'fam') == 'fam_2.yml'


def test_as_db_dict():
    """Test the as_db_dict() method."""
    rxn = AMReaction(r_species=[ARCSpecies(label='nC3H5', smiles='[CH2]CC')],
                     p_species=[ARCSpecies(label='iC3H5', smiles='C[CH]C')])
    content = rxn.as_db_dict()
    assert content == {'approved_by': None,
                       'atom_maps': content['atom_maps'],
                       'clustering': [],
                       'charge': 0,
                       'multiplicity': 2,
                       'p_adjacency_lists': [['multiplicity 2\n'
                                              '1  C u0 p0 c0 {3,S} {4,S} {5,S} {6,S}\n'
                                              '2  C u0 p0 c0 {3,S} {7,S} {8,S} {9,S}\n'
                                              '3  C u1 p0 c0 {1,S} {2,S} {10,S}\n'
                                              '4  H u0 p0 c0 {1,S}\n'
                                              '5  H u0 p0 c0 {1,S}\n'
                                              '6  H u0 p0 c0 {1,S}\n'
                                              '7  H u0 p0 c0 {2,S}\n'
                                              '8  H u0 p0 c0 {2,S}\n'
                                              '9  H u0 p0 c0 {2,S}\n'
                                              '10 H u0 p0 c0 {3,S}\n']],
                       'p_inchi_keys': ['HNUALPPJLMYHDK-UHFFFAOYSA-N'],
                       'p_rmg_labels': content['p_rmg_labels'],
                       'p_xyz': [{'coords': content['p_xyz'][0]['coords'],
                                  'isotopes': (12, 12, 12, 1, 1, 1, 1, 1, 1, 1),
                                  'symbols': ('C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H')}],
                       'r_adjacency_lists': [['multiplicity 2\n'
                                              '1  C u0 p0 c0 {2,S} {3,S} {4,S} {5,S}\n'
                                              '2  C u0 p0 c0 {1,S} {6,S} {7,S} {8,S}\n'
                                              '3  C u1 p0 c0 {1,S} {9,S} {10,S}\n'
                                              '4  H u0 p0 c0 {1,S}\n'
                                              '5  H u0 p0 c0 {1,S}\n'
                                              '6  H u0 p0 c0 {2,S}\n'
                                              '7  H u0 p0 c0 {2,S}\n'
                                              '8  H u0 p0 c0 {2,S}\n'
                                              '9  H u0 p0 c0 {3,S}\n'
                                              '10 H u0 p0 c0 {3,S}\n']],
                       'r_inchi_keys': ['OCBFFGCSTGGPSQ-UHFFFAOYSA-N'],
                       'r_rmg_labels': {'*1': 2, '*2': 0, '*3': 4},
                       'r_xyz': [{'coords': content['r_xyz'][0]['coords'],
                                  'isotopes': (12, 12, 12, 1, 1, 1, 1, 1, 1, 1),
                                  'symbols': ('C', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H')}],
                       'rejected_by': None,
                       'rejected_reasons': []}
    assert sorted(content['atom_maps'][0]) == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert sorted(list(content['p_rmg_labels'].keys())) == ['*1', '*2', '*3']

    rxn = AMReaction(r_species=[ARCSpecies(label='OH', smiles='[OH]'), ARCSpecies(label='NCC', smiles='NCC')],
                     p_species=[ARCSpecies(label='H2O', smiles='O'), ARCSpecies(label='NjCC', smiles='[NH]CC')])
    rxn.approved_by = ['user_1']
    rxn.rejected_by = ['user_2']
    rxn.rejected_reasons = ['Not sure']
    content = rxn.as_db_dict()
    assert content == {'approved_by': ['user_1'],
                       'atom_maps': [[0, 1, 3, 4, 5, 2, 6, 8, 7, 11, 9, 10]],
                       'clustering': [],
                       'charge': 0,
                       'multiplicity': 2,
                       'p_adjacency_lists': [['1 O u0 p2 c0 {2,S} {3,S}\n'
                                              '2 H u0 p0 c0 {1,S}\n'
                                              '3 H u0 p0 c0 {1,S}\n'],
                                             ['multiplicity 2\n'
                                              '1 N u1 p1 c0 {2,S} {9,S}\n'
                                              '2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}\n'
                                              '3 C u0 p0 c0 {2,S} {6,S} {7,S} {8,S}\n'
                                              '4 H u0 p0 c0 {2,S}\n'
                                              '5 H u0 p0 c0 {2,S}\n'
                                              '6 H u0 p0 c0 {3,S}\n'
                                              '7 H u0 p0 c0 {3,S}\n'
                                              '8 H u0 p0 c0 {3,S}\n'
                                              '9 H u0 p0 c0 {1,S}\n']],
                       'p_inchi_keys': ['XLYOFNOQVPJJNP-UHFFFAOYSA-N', 'RZRWAZWNUOVMAY-UHFFFAOYSA-N'],
                       'p_rmg_labels': {'*1': 3, '*2': 1, '*3': 0},
                       'p_xyz': [{'coords': content['p_xyz'][0]['coords'],
                                  'isotopes': (16, 1, 1),
                                  'symbols': ('O', 'H', 'H')},
                                 {'coords': content['p_xyz'][1]['coords'],
                                  'isotopes': (14, 12, 12, 1, 1, 1, 1, 1, 1),
                                  'symbols': ('N', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H')}],
                       'r_adjacency_lists': [['multiplicity 2\n'
                                              '1 O u1 p2 c0 {2,S}\n'
                                              '2 H u0 p0 c0 {1,S}\n'],
                                             ['1  N u0 p1 c0 {2,S} {9,S} {10,S}\n'
                                              '2  C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}\n'
                                              '3  C u0 p0 c0 {2,S} {6,S} {7,S} {8,S}\n'
                                              '4  H u0 p0 c0 {2,S}\n'
                                              '5  H u0 p0 c0 {2,S}\n'
                                              '6  H u0 p0 c0 {3,S}\n'
                                              '7  H u0 p0 c0 {3,S}\n'
                                              '8  H u0 p0 c0 {3,S}\n'
                                              '9  H u0 p0 c0 {1,S}\n'
                                              '10 H u0 p0 c0 {1,S}\n']],
                       'r_inchi_keys': ['TUJKJAMUKRIRHC-UHFFFAOYSA-N', 'QUSNBJAOOMFDIB-UHFFFAOYSA-N'],
                       'r_rmg_labels': {'*1': 2, '*2': 11, '*3': 0},
                       'r_xyz': [{'coords': content['r_xyz'][0]['coords'],
                                  'isotopes': (16, 1),
                                  'symbols': ('O', 'H')},
                                 {'coords': content['r_xyz'][1]['coords'],
                                  'isotopes': (14, 12, 12, 1, 1, 1, 1, 1, 1, 1),
                                  'symbols': ('N', 'C', 'C', 'H', 'H', 'H', 'H', 'H', 'H', 'H')}],
                       'rejected_by': ['user_2'],
                       'rejected_reasons': ['Not sure']}


def test_save():
    """Test the save() method."""
    shutil.copy(src=os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0.yml'),
                dst=os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0_back.yml'))

    rxn = AMReaction(r_species=[ARCSpecies(label='OH', smiles='[OH]'), ARCSpecies(label='NCC', smiles='NCC')],
                     p_species=[ARCSpecies(label='H2O', smiles='O'), ARCSpecies(label='NjCC', smiles='[NH]CC')])
    rxn.save(database_path=os.path.join(AM3DB_PATH, 'tests', 'data'))
    content = read_yaml_file(os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0.yml'))
    assert content[0]['atom_maps'] == [[0, 1, 3, 4, 5, 2, 6, 8, 7, 11, 9, 10]]
    assert content[0]['charge'] == 0
    assert content[0]['p_adjacency_lists'] == [['1 O u0 p2 c0 {2,S} {3,S}\n'
                                                '2 H u0 p0 c0 {1,S}\n'
                                                '3 H u0 p0 c0 {1,S}\n'],
                                               ['multiplicity 2\n'
                                                '1 N u1 p1 c0 {2,S} {9,S}\n'
                                                '2 C u0 p0 c0 {1,S} {3,S} {4,S} {5,S}\n'
                                                '3 C u0 p0 c0 {2,S} {6,S} {7,S} {8,S}\n'
                                                '4 H u0 p0 c0 {2,S}\n'
                                                '5 H u0 p0 c0 {2,S}\n'
                                                '6 H u0 p0 c0 {3,S}\n'
                                                '7 H u0 p0 c0 {3,S}\n'
                                                '8 H u0 p0 c0 {3,S}\n'
                                                '9 H u0 p0 c0 {1,S}\n']]
    assert content[0]['r_inchi_keys'] == ['TUJKJAMUKRIRHC-UHFFFAOYSA-N', 'QUSNBJAOOMFDIB-UHFFFAOYSA-N']

    os.remove(os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0.yml'))
    shutil.copy(src=os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0_back.yml'),
                dst=os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0.yml'))
    os.remove(os.path.join(AM3DB_PATH, 'tests', 'data', 'reactions', 'H_Abstraction_0_back.yml'))


def test_p_number_from_am_index():
    """Test the _p_number_from_am_index() method"""
    rxn_1 = AMReaction(r_species=[ARCSpecies(label='CH3', smiles='[CH3]'), ARCSpecies(label='CH4', smiles='C')],
                       p_species=[ARCSpecies(label='CH4', smiles='C'), ARCSpecies(label='CH3', smiles='[CH3]')])
    assert rxn_1.atom_map[0] == 5
    assert rxn_1.atom_map[4] == 0
    assert rxn_1._p_number_from_am_index(0) == 1
    assert rxn_1._p_number_from_am_index(4) == 0

    rxn_2 = AMReaction(r_species=[ARCSpecies(label='pentadiene', smiles='C=CCC=C'),
                                  ARCSpecies(label='decalin_rad', smiles='C1CC[C]2CCCCC2C1')],
                       p_species=[ARCSpecies(label='decalin', smiles='C1CCC2CCCCC2C1'),
                                  ARCSpecies(label='pentadieneyl', smiles='C=C[CH]C=C')])
    assert rxn_2._p_number_from_am_index(0) == 1















































