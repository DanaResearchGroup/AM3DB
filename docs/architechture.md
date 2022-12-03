# as_db_dict() Method

as_db_dict is a method that returns a dict that represents row in the program DB.

- multiplicity:  (int)
- charge: variable that represents the molecule charge (int)
- r_adjacency_lists: variable that represents the reagents resonance structures per species (List[List[str]])
- p_adjacency_lists: variable that represents the products resonance structures per species (List[List[str]])
- r_xyz: variable that represents the reagents coordinates (List[dict])
- p_xyz: variable that represents the products coordinates (List[dict])
- r_rmg_labels
- p_rmg_labels
- atom_maps: variable that describes each atom place change in the reaction (List[List[List[int]]])
- approved_by: variable that represents name of person that approved reaction modeling (List[str])
- rejected_by: variable that represents name of person that rejected reaction modeling (List[str])
- rejected_reasons: variable that represents a comment explaining the reason for rejecting the reaction modeling (List[str])
