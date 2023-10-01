# Coding

# Exercise 6 (b). Average case analysis by exhaustive search over all instances

# Given an instance of the Stable Marriage problem with 4 men and 4 women, we want to perform an exhaustive average case analysis. Specifically, what is the expected number of proposals men are going to make in the Gale-Shapley algorithm?

# To compute the average number of proposals, we ask you to run the G-S algorithm over all the possible instances with womens' preferences fixed.  

# -  Fill the function *instance_generator* so that it returns a dictionary and a float value. For the dictionary, the keys should be the number of proposals made by the G-S algorithm, and the value the number of instances that yield this specific number of proposals. For example d[k]=m, would mean that m problem instances resulted in k proposals in total.  The float value is the average number of proposals from this dictionary. How does it compare to the maximum and minimum number of proposals? 

# For the final submission, do not add anything outside the instance_generator function, except package import. Only upload this .py file on the gradescope.


# This is the Gale-Shapley algorithm we shared on Github. We modified it so now it returns the number of proposals made instead of a stable matching.
from itertools import permutations, product
from collections import defaultdict

def gale_shapley(men_preferences, women_preferences):
    n = len(men_preferences)

    # Initialize empty matching
    matching = [-1] * n
    free_men = list(range(n))
    proposal_happened = set()

    preference_rank = [[0]*n for _ in range(n)]
    for woman in range(n):
        for rank, man in enumerate(women_preferences[woman]):
            preference_rank[woman][man] = rank

    while free_men:
        man = free_men.pop(0)
        man_preferences = men_preferences[man]
        

        for woman in man_preferences:
            # If woman is unmatched, match her with the man
            if woman not in matching:
                matching[man] = woman
                proposal_happened.add((man, woman))
                break
            else:
                if (man,woman) in proposal_happened:
                    continue
                proposal_happened.add((man, woman))
                # Find the current partner of the woman
                current_partner = matching.index(woman)

                # constant time lookup in this way
                if preference_rank[woman][man] < preference_rank[woman][current_partner]:
                    # Unmatch the current partner
                    matching[current_partner] = -1
                    free_men.append(current_partner)

                    # Match the new man
                    matching[man] = woman
                    break
    return len(proposal_happened)


def instance_generator(women_preference):
    n = len(women_preference)
    
    # empty dictionary to be used later
    proposals_count = defaultdict(int)

    men_permutations = list(permutations(range(n))) #4! permutations of men pref
    all_combinations = list(product(men_permutations, repeat=4)) #(4!)^4 combinations of those 4! permutations

    for men_pref in all_combinations:
        prop = gale_shapley(list(men_pref), women_preference)
        proposals_count[prop] += 1

    average_proposals = sum(k * v for k, v in proposals_count.items()) / len(all_combinations)

    return proposals_count, average_proposals
    
    """
	:women_preference: A list of lists that describe each women's preference
	:return: A tuple (Dict, float). See details at the beginning of this file. 
	"""
	# TODO: your code goes here
	# pass
    
# This is an example of the input. 
def toy_test():
	women_preference = [[0,1,2,3],[2,1,0,3],[3,1,2,0],[3,2,1,0]]
	print(instance_generator(women_preference))

toy_test()