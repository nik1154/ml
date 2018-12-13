# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 12:14:56 2018

@author: komal
"""

class Holder:
    factors={} #Initialize an empty dictionary
    attributes = () #declaration of dictionaries parameters with an arbitrary length
    def __init__(self,attr): #
        self.attributes = attr
        for i in attr:
            self.factors[i]=[]
    def add_values(self,factor,values):
        self.factors[factor]=values


class CandidateElimination:
    Positive={} #Initialize positive empty dictionary
    Negative={} #Initialize negative empty dictionary

    def __init__(self,data,fact):
        self.num_factors = len(data[0][0])
        self.factors = fact.factors
        self.attr = fact.attributes
        self.dataset = data
    #print self.attr
    def run_algorithm(self):
    # print self.dataset
        G = self.initializeG()
        S = self.initializeS()
        print("initialize General",G)
        print("initialize Specific",S)
        for trial_set in self.dataset:
            if self.is_positive(trial_set): #if trial set/example consists of positive examples
                G = self.remove_inconsistent_G(G,trial_set[0]) #remove inconsitent data from the general
                S_new = S[:] #initialize the dictionary with no key-value pair
                print(S_new)
                for s in S:
                    if not self.consistent(s,trial_set[0]):
                        S_new.remove(s)
                        generalization = self.generalize_inconsistent_S(s,trial_set[0])
                        generalization = self.get_general(generalization,G)
                        if generalization:
                            S_new.append(generalization)
                    S = S_new[:]
                    S = self.remove_more_general(S)
                    print(S)
                else:
                    S = self.remove_inconsistent_S(S,trial_set[0]) #remove inconsitent data from the specific
                    G_new = G[:] #initialize the dictionary with no key-value pair (dataset can take any value)
                    print(G_new)
                    for g in G:
                        if self.consistent(g,trial_set[0]):
                            G_new.remove(g)
                            specializations = self.specialize_inconsistent_G(g,trial_set[0])
                            specializations = self.get_specific(specializations,S)
                            if specializations != []:
                                G_new += specializations
                        G = G_new[:]
                        print(G)
                        G = self.remove_more_specific(G)
            print(S)
            print(G)
    
    def initializeS(self):
        S = tuple(['-' for factor in range(self.num_factors)]) #6 constraints in the vector
        return [S]
    
    def initializeG(self):
        G = tuple(['?' for factor in range(self.num_factors)]) # 6 constraints in the vector
        return [G]
    
    def is_positive(self,trial_set):
        if trial_set[1] == 'Y':
            return True
        elif trial_set[1] == 'N':
            return False
        else:
            raise TypeError("invalid target value")
            
    def is_negative(self,trial_set):
        if trial_set[1] == 'N':
            return False
        elif trial_set[1] == 'Y':
            return True
        else:
            raise TypeError("invalid target value")
    
    
    def match_factor(self,value1,value2):
        if value1 == '?' or value2 == '?':
            return True
        elif value1 == value2 :
            return True
        return False
    
    def consistent(self,hypothesis,instance):
        for i,factor in enumerate(hypothesis):
            if not self.match_factor(factor,instance[i]):
                return False
            return True
    
    def remove_inconsistent_G(self,hypotheses,instance):
        G_new = hypotheses[:]
        for g in hypotheses:
            if not self.consistent(g,instance):
                G_new.remove(g)
        return G_new
            
            
    def remove_inconsistent_S(self,hypotheses,instance):
        S_new = hypotheses[:]
        for s in hypotheses:
            if self.consistent(s,instance):
                S_new.remove(s)
        return S_new
        
    def remove_more_general(self,hypotheses):
        S_new = hypotheses[:]
        for old in hypotheses:
            for new in S_new:
                if old!=new and self.more_general(new,old):
                    S_new.remove[new]
        return S_new
                
    def remove_more_specific(self,hypotheses):
        G_new = hypotheses[:]
        for old in hypotheses:
            for new in G_new:
                if old!=new and self.more_specific(new,old):
                    G_new.remove[new]
        return G_new
                
    def generalize_inconsistent_S(self,hypothesis,instance):
        hypo = list(hypothesis) 
        for i,factor in enumerate(hypo):
            if factor == '-':
                hypo[i] = instance[i]
            elif not self.match_factor(factor,instance[i]):
                hypo[i] = '?'
        generalization = tuple(hypo) # convert list back to tuple for immutability
        return generalization
    
    def specialize_inconsistent_G(self,hypothesis,instance):
        specializations = []
        hypo = list(hypothesis) # convert tuple to list for mutability
        for i,factor in enumerate(hypo):
            if factor == '?':
                values = self.factors[self.attr[i]]
                for j in values:
                    if instance[i] != j:
                        hyp=hypo[:]
                        hyp[i]=j
                        hyp=tuple(hyp) # convert list back to tuple for immutability
                        specializations.append(hyp)
        return specializations
    
    
    def get_general(self,generalization,G):
        for g in G:
            if self.more_general(g,generalization):
                return generalization
        return None
    
    def get_specific(self,specializations,S):
        valid_specializations = []
        for hypo in specializations:
            for s in S:
                if self.more_specific(s,hypo) or s==self.initializeS()[0]:
                    valid_specializations.append(hypo)
        return valid_specializations
    
    def exists_general(self,hypothesis,G):
        for g in G:
            if self.more_general(g,hypothesis):
                return True
        return False
    
    def exists_specific(self,hypothesis,S):
        for s in S:
            if self.more_specific(s,hypothesis):
                return True
        return False
    
    def get_version_space(self,specific,general, VS=None):
        while self.get_order(VS):
            for hypothesis in VS[:]:
                hypo = list(hypothesis) # convert tuple to list for mutability
                for i,factor in enumerate(hypo):
                    if factor != '?':
                        hyp=hypo[:]
                        hyp[i]='?'
                        if self.exists_general(hyp,general)and self.exists_specific(hyp,specific):
                            VS.append(tuple(hyp))
        return VS
    
    def get_order(self,hypothesis):
        pass
    
    def more_general(self,hyp1,hyp2):
        hyp = list(zip(hyp1,hyp2))
        for i,j in hyp:
            if i == '?':
                continue
            elif j == '?':
                if i != '?':
                    return False
                elif i != j:
                    return False
                else:
                    continue
        return True
    
    def more_specific(self,hyp1,hyp2):
        return self.more_general(hyp2,hyp1)
        dataset=[(('sunny','warm','normal','strong','warm','same'),'Y'),(('sunny','warm','high','strong','warm','same'),'Y'),(('rainy','cold','high','strong','warm','change'),'N'),(('sunny','warm','high','strong','cool','change'),'Y')]
        #print((dataset[0][1]))
        attributes =('Sky','Temp','Humidity','Wind','Water','Forecast')
        f = Holder(attributes)
        f.add_values('Sky',('sunny','rainy','cloudy')) #sky can be sunny rainy or cloudy
        f.add_values('Temp',('cold','warm')) #Temp can be sunny cold or warm
        f.add_values('Humidity',('normal','high')) #Humidity can be normal or high
        f.add_values('Wind',('weak','strong')) #wind can be weak or strong
        f.add_values('Water',('warm','cold')) #water can be warm or cold
        f.add_values('Forecast',('same','change')) #Forecast can be same or change
        a = CandidateElimination(dataset,f)
        a.run_algorithm()


