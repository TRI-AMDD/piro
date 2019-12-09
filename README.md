## **rxn** Reaction recommender for the synthesis of inorganic compounds

**WIP**

_rxn_ is a recommendation system for navigation of synthesis of 
inorganic materials based on classical nucleation theory 
and semi-empirical, data-driven approximations to its parts. Currently it
works with Materials Project data via its Rester API.

_rxn_ should in principle allow retrosynthetic analysis of target inorganic materials 
(i.e. laying out all the reaction steps necessary to arrive at the target). This is currently in progress.

Currently rxn creates interactive plots where the best selective routes for a target polymorph
are the ones closer to the lower left corner. There is Pareto optimality, but often the "good" reactions
can be differentiated from the "bad" relatively easily by visual inspection.

This is an example generated for the synthesis of a layered Li2MnO3 compound:
![Example - Li2MnO3](https://github.awsinternal.tri.global/murat-aykol/rxn/raw/master/rxn/files/Example1%20-%20Li2MnO3.png)

We can zoom into the lower left corner to inspect the most promising reactions:
![Example - Li2MnO3](https://github.awsinternal.tri.global/murat-aykol/rxn/raw/master/rxn/files/Example2%20-%20Li2MnO3.png)