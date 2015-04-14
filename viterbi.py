# -*- coding: utf-8 -*-
"""
Created on Wed Apr 08 16:34:09 2015

@author: heshenghuan
"""

import copy

class Viterbi:
    def __init__(self):
        self.state = {}
        self.observe = {}
        self.state_size = 0
        self.obs_size = 0
        self.trans = []
        self.emits = []
        self.init_prb = []
        
    def load_modle(self, state_set, obs_set, trans, emits, init_prb):
        self.state = copy.deepcopy(state_set)
        self.observe = copy.deepcopy(obs_set)
        self.trans = copy.deepcopy(trans)
        self.emits = copy.deepcopy(emits)
        self.init_prb = copy.deepcopy(init_prb)
        self.state_size = len(self.state)
        self.obs_size = len(self.observe)
        
        print "load model done!"
        print "state set:"
        print self.state
        print "observe set:"
        print self.observe
        print "inital prb:"
        print self.init_prb
        print "trans:"
        print self.trans
        print "emits:"
        print self.emits
    
    def decode(self, obs):
        obs_len = len(obs)
        prb, prb_max = 0., 0.
        toward = list()
        back = list()
        
        for i in range(obs_len):
            toward.append([])
            back.append([])
            for j in range(self.state_size):
                toward[i].append(0.)
                back[i].append(0)
            
        #run viterbi
        for s in range(self.state_size):
            toward[0][s] = self.init_prb[s] * self.emits[s][obs[0]]
            back[0][s] = -1
        
        for t in range(1, obs_len):
            for s in range(self.state_size):
                prb_max = 0.
                state_max = 0
                for i in range(self.state_size):
                    prb = toward[t-1][i] * self.trans[i][s] * self.emits[s][obs[t]]
                    if prb > prb_max:
                        prb_max = prb
                        state_max = i
                toward[t][s] = prb_max
                back[t][s] = state_max
        
        prb_max = 0.0
        state_max = 0
        for s in range(self.state_size):
            prb = toward[obs_len-1][s]
            if prb > prb_max:
                prb_max = prb
                state_max = s
        
        best_path = []
        best_path.append(state_max)
        j = obs_len-1
        while j >= 1:
            pre_state = back[j][best_path[0]]
            best_path.insert(0, pre_state)
            j -= 1
        
        path = self.state[best_path[0]]
        for p in range(1,len(best_path)):
            path += '->' + self.state[best_path[p]]
        return prb_max, path
        
if __name__ == '__main__':
    viterbi = Viterbi()
    state = {0:"Healthy",1:"Fever"}
    obs_state = {0:"Dizzy",1:"Cold",2:"Normal"}
    trans = [[0.7, 0.3], [0.6, 0.4]]
    emits = [[0.1, 0.4, 0.5], [0.6, 0.3, 0.1]]
    init_prb = [0.6, 0.4]
    viterbi.load_modle(state, obs_state, trans, emits, init_prb)
    prb, path = viterbi.decode([2,0,2])
    print "Max prb:",prb
    print "Path:",path
#    for item in path:
#        print state[item],