---
toc: true
layout: post
description: Summary of performance analysis done of Meff algorithm.
categories: [markdown]
title: Performance comparison of Meff algorithm
---

# Performance comparison of Meff algorithm



## Setup

The task used to evaluate the performance various languages and libraries is meff -  the number of effective sequences in the MSA. 
The alogrithm is quite simple: the input is a list of equal length sequences, we need to calculate how many effectively unique seqeunces there are. 
In order to do so, firstly we need to calcualate pairwise identities (what percentage of sequence is matching) and if the identity is higher than 
chosen threshold, we cluster them together. As a result we get how many sequences are similar to the one of interest and this number determines the weight 
of the sequences towards the final result. 

Pseudo code looks like this: 

```
for seq1 in seqs:
  for seq2 in seqs:
    if count_mathes(seq1, seq2) > threshold:
      weight +=1
  meff += 1/weight
  
meff = meff/(len(seq1)^0.5)
```

While code codes not look complex, the complexity is O(n^2) which does not scale well (later we will see how to make it O(n log(n))). I will use the MSA which consists 
of 10000 sequences of length 683.


## Baselines

For baseline we will use C and C++ implementations

### C++ implementation

C++ implementation was extracted from https://zhanglab.dcmb.med.umich.edu/DeepMSA/ package. No changes have been made to it.

### C implemnentation
C implementation wast taken from http://prody.csb.pitt.edu/_modules/prody/sequence/analysis.html#calcMeff. Once again the code was run as it is. 

## Results

