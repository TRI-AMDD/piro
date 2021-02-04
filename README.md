## *piro:* rational planning of solid-state synthesis routes for inorganics

_piro_ is a recommendation system for navigation and planning of synthesis of 
inorganic materials based on classical nucleation theory 
and semi-empirical, data-driven approximations to its parts. Currently it
works with Materials Project data via its Rester API.

- _piro_ creates synthesis reaction planning plots for target polymorphs under a specific set of thermodynamic conditions and precuror library, where favorable routes are those that are (nearly) Pareto optimal in terms of two metrics: nucleation barrier and phase-selection. 

- _piro_ allows retrosynthetic analysis of target inorganic materials to generate a synthesis reaction tree.
(i.e. laying out the reaction pathways necessary to arrive at the target from practical/purchasable reagents/starting materials)

- _piro_ supports generation of interactive plots and a web-UI for easy-navigation.
