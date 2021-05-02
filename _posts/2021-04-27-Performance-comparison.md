---
toc: true
layout: post
description: Summary of performance analysis done of the number of effective sequences algorithm.
categories: [markdown]
title: Performance comparison of the number of effective sequences algorithm
---
# Performance comparison of the number of effective sequences algorithm

## Introduction

From time to time I hear something along the lines 'we should rewrite this in C to improve performance'. I always was sceptical about this idea, but I have not had any practical experience to be able to give a concrete example. During the process of making this post I explored the performance difference of one algorithm
written in different ways including C and C++. The main questions I was intrigued about were:
* How much faster is C/C++ in practise if I were to rewrite code?
* Does the gain justify the effort?
* Are any of the python performance libraries like Cypthon or Numba useful in practise?

Note: a one example is not enough to draw any solid conclusions, but when it resonates with what you heard before that is at least reassuring. 

I hope this will be yet another performance comparison which in combination with all other ones will be helpful to make a decision in your particular case. 

## Algorithm to be tested

The algorithm used to evaluate performance is the [number of effective sequences](https://academic.oup.com/bioinformatics/article/36/7/2105/5628221) (Nf) in the MSA.
The algorithm is quite simple: the input is a list of equal length sequences, we need to calculate how many effectively unique sequences there are (a single number).
In order to do so, firstly we need to calculate pairwise identities (what percentage of sequence is matching) and if the identity is higher than
chosen threshold, we cluster them together. The inverse of cluster size gives you a weight of the sequence. A sum of weights is the Nf. Intuitively, if all sequences are similar, you will get one cluster, hence the Nf will be 1, at the other end of the spectrum, if all sequences are completely different, cluster sizes will be 1, hence the Nf will be equal to the number of sequences.  We have the normalization term at the end to normalize by sequence length. 

Pseudo code looks like this:

```
for seq1 in seqs:
  for seq2 in seqs:
    if count_mathes(seq1, seq2) > threshold:
      weight +=1
  meff += 1/weight
 
meff = meff/(len(seq1)^0.5)
```

Code complexity is O(n^2) which means it does not scale well (later we will see how to make it O(n log(n))). 

## Setup

To perform testing I used the MSA which consists of 10000 sequences of length 683. The hardware used was: Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz 16GB RAM + Nvidia 1650GTX. 

Note: the results might vary wildly depending of the hardware you have. It is good to keep that in mind when analysing results. 


## Baselines

For baseline I used C and C++ implementations. As I do not consider myself an expert in C or C++ I borrowed existing implementations from existing sources:

* C++ implementation was extracted from (DeepMSA)[https://zhanglab.dcmb.med.umich.edu/DeepMSA/] package. No changes have been made to it.
* C implementation wast taken from (Prody)[http://prody.csb.pitt.edu/_modules/prody/sequence/analysis.html#calcMeff]. Once again the code was run as it is. 

## Results

In this section I display the results I got on my hardware. The implementations are extracted to separate notebooks for making this post bearable. While code might not be optimal, I did spend a significant amout of time trying to optimise the code. 

### Single threaded

| Code            | Threads | Time      |
| --------------- | ------- | --------- |
| C++             | 1       | 02:26.86  |
| C               | 1       | 00:41.35  |
| Pure Python     | 1       | ~7 hours[^1] |
| Numpy           | 1       | 00:32.51  |
| Cypthon         | 1       | 00:32.43  |
| Numba           | 1       | 00:26.63  |
| Julia           | 1       | 04:51.00**|

[^1] Pure python times were estimated on the timings I got on 100 sequences. 
** I am quite sure that Julia can be faster and the developer it to blame for its poor performance. 


### Multi threaded 

| Core            | Threads | Time     |
| --------------- | ------- | -------- |
| Numpy           | 12      | 00:07.11 |
| Numba           | 12      | 00:05.12 |
| Tensroflow      | 12      | 00:39.88 |
| Pytorch         | 12      | 00:39.14 |

### With accelerator (GPU)

| Core            | Threads | Time     |
| --------------- | ------- | -------- |
| Tensorflow      | 1       | 00:06.10 |
| Pytorch         | 1       | 00:08.05 |
| JAX             | 1       | 00:00.13 |

