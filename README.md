## Description  
Repository containing various scripts used in my URSA project on Latin Squares.  
**backtracking.py:** uses the standard backtracking method to check for squares with no transversals  
**backtrackingCount.py:** uses the standard backtracking method to check for squares with no transversals, counts minimum amount of transversals found  
**deltaVerification.py:** uses the delta construction outlined by Wanless and Webb to verify that a transversal exists through every entry in a given square  
**findTransversals.py:** uses the backtracking method to find all transversals of a given square  
**markov.py:** uses the Jacobsen & Matthews method of generating Latin Squares to check for squares with no transversals  
**markovCount.py:** uses the Jacobsen & Matthews method of generating Latin Squares to find the minimum amount of transversals  
**transversalDecomposition.py:** algorithm to see if there is a full decomposition of transversals for a given square  

## References
Wanless, I.M., Webb, B.S. The Existence of Latin Squares without Orthogonal Mates. Des Codes Crypt 40, 131–135 (2006). https://doi.org/10.1007/s10623-006-8168-9
Mark T. Jacobson and Peter Matthews, "Generating uniformly distributed random Latin squares", Journal of Combinatorial Designs, 4 (1996). https://doi.org/10.1002/(SICI)1520-6610(1996)4:6%3C405::AID-JCD3%3E3.0.CO;2-J
The SageMath Developers. (2025). SageMath (Version 10.7.beta0) [Computer software].  https://doi.org/10.5281/zenodo.8042260
