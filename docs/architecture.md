# AM3DB Architecture

The following describes how the database is designed and the attributes of reaction objects stored in it.

The AMReaction object stores the following arguments in the database:

- label (str): The reaction label.
- multiplicity  (int): The spin multipicity of the reaction potential energy surface.
- charge (int): The reaction potential energy surface net electric charge.
- r\_adjacency\_lists (List[List[str]]): all representative resonance structures per reactant.
- p\_adjacency\_lists (List[List[str]]): all representative resonance structures per product.
- r\_xyz (List[dict]): Entries represent cartesian coordinates per reactant.
- p\_xyz (List[dict]): Entries represent cartesian coordinates per products.
- r\_rmg\_label Dict[str, int]: The reactant atom indices identified by the RMG family recipe. 
- r\_rmg\_label Dict[str, int]: The product atom indices identified by the RMG family recipe.
- atom\_maps (List[List[int]]): A comprehensive list of possible atom-maps.
- clustering (List[List[int]]): Storing the indices of redundant atom-maps. 
- approved_by (List[str]): variable that represents name of person that approved reaction modeling.
- rejected\_by (List[str]): variable that represents name of person that rejected reaction modeling.
- rejected\_reasons (List[str]): variable that represents a comment explaining the reason for rejecting the reaction modeling.
