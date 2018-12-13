# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 20:27:42 2018

@author: komal
"""

from pomegranate import *
Asia=DiscreteDistribution({ „True‟:0.5, „False‟:0.5 })

Tuberculosis=ConditionalProbabilityTable(
[[ 'True','True', 0.2],
['True', 'False', 0.8],
[ 'False', 'True', 0.01],
[ 'False', 'False', 0.98]], [asia])

Smoking = DiscreteDistribution({ „True‟:0.5, „False‟:0.5 })

Lung = ConditionalProbabilityTable(
[[ „True‟, „True‟, 0.75],
[„True‟, „False‟,0.25].
[ „False‟, „True‟, 0.02],
[ „False‟, „False‟, 0.98]], [ smoking])

Bronchitis = ConditionalProbabilityTable(
[[ „True‟, „True‟, 0.92],
[„True‟, „False‟,0.08].
[ „False‟, „True‟,0.03],
[ „False‟, „False‟, 0.98]], [ smoking])cl

Tuberculosis_or_cancer = ConditionalProbabilityTable(
[[ „True‟, „True‟, „True‟, 1.0],
[„True‟, „True‟, „False‟, 0.0],
[„True‟, „False‟, „True‟, 1.0],
[„True‟, „False‟, „False‟, 0.0],
[„False‟, „True‟, „True‟, 1.0],
[„False‟, „True‟, „False‟, 0.0],
[„False‟, „False‟ „True‟, 1.0],
[„False‟, „False‟, „False‟, 0.0]], [tuberculosis, lung])

Xray = ConditionalProbabilityTable(
        [[ „True‟, „True‟, 0.885],
[„True‟, „False‟, 0.115],
[ „False‟, „True‟, 0.04],
[ „False‟, „False‟, 0.96]], [tuberculosis_or_cancer])

dyspnea = ConditionalProbabilityTable(
[[ „True‟, „True‟, „True‟, 0.96],
[„True‟, „True‟, „False‟, 0.04],
[„True‟, „False‟, „True‟, 0.89],
[„True‟, „False‟, „False‟, 0.11],
[„False‟, „True‟, „True‟, 0.96],
[„False‟, „True‟, „False‟, 0.04],
[„False‟, „False‟ „True‟, 0.89],
[„False‟, „False‟, „False‟, 0.11 ]], [tuberculosis_or_cancer, bronchitis])

s0 = State(asia, name=”asia”)
s1 = State(tuberculosis, name=” tuberculosis”)
s2 = State(smoking, name=” smoker”)
network = BayesianNetwork(“asia”)
network.add_nodes(s0,s1,s2)
network.add_edge(s0,s1)
network.add_edge(s1.s2)
network.bake()
print(network.predict_probal({„tuberculosis‟: „True‟}))