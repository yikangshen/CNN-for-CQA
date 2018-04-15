'''
Created on 2013-4-5

@author: hmwv1114
'''
import math

class Article(object):
    '''
    This is basic Article class
    '''


    def __init__(self):
        '''
        Constructor
        '''
        self.index = 0
        self.wordVect = {}
        self.totalWord = 0
        
    def add_distance(self, otherIndex, distance):
        self.distanceToOther.append([otherIndex, distance])
        
    def set_position(self, position):
        self.position = position
     
    @staticmethod    
    def measure_similarity(u, v, sim_func = None):
        '''
        Returns the textual similarity of file_a and file_b using chosen similarity metric
        'sim_func' defaults to cosine_sim if not specified
        Consumes file_a and file_b
        '''
        
        
        
        def cosine_sim(u, v):
            '''
            Returns the cosine similarity of u,v: <u,v>/(|u||v|)
            where |u| is the L2 norm
            '''
            div = (l2_norm(u) * l2_norm(v))
            if div == 0:
                return 0
            return dot_product(u, v) / (l2_norm(u) * l2_norm(v))
             
        def jaccard_sim(A, B):
            '''
            Returns the Jaccard similarity of A,B: |A \cap B| / |A \cup B|
            We treat A and B as multi-sets (The Jaccard coefficient is technically defined over sets)
            '''
            '''
            div = mag_union(A, B)
            if div == 0:
                return 0
            else:
                t = mag_intersect(A, B) / (float)(div)
                return t
            '''
            div = 2
            sumA = sum(A)
            sumB = sum(B)
            
            intersect = 0.0
            for term in A:
                if term in B: 
                    intersect += min(float(A[term]) / sumA, float(B[term]) / sumB)
            
            t = intersect / float(div)
            
            return t
             
        # --- Term-vector operations ---
        
        def sum(A):
            val = 0
            for term in A: val += A[term]
            
            return val
             
        def dot_product(v1, v2):
            '''Returns dot product of two term vectors'''
            val = 0.0
            for term in v1:
                if term in v2: val += v1[term] * v2[term]
            return val
             
        def l2_norm(v):
            '''Returns L2 norm of term vector v'''
            val = 0.0
            for term in v:
                val += v[term]**2
            val = math.sqrt(val)
            
            return val
             
        def mag_union(A, B):
            '''
            Returns magnitude of multiset-union of A and B
            '''
            val = 0
            for term in A: val += A[term]
            for term in B: val += B[term]
            
            return val
             
        def mag_intersect(A, B):
            '''
            Returns magnitude of multiset-intersection of A and B
            '''
            val = 0
            for term in A:
                if term in B: 
                    val += min(A[term], B[term])
            return val
        
        
        
        
        if sim_func == None: 
            sim_func = jaccard_sim  # default to cosine_sim
         
        t = sim_func(u, v)
        return t
        