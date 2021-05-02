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
* Are any of the Python performance libraries like Cython or Numba useful in practise?

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

* C++ implementation was extracted from [DeepMSA](https://zhanglab.dcmb.med.umich.edu/DeepMSA/) package. No changes have been made to it.
* C implementation wast taken from [Prody](http://prody.csb.pitt.edu/_modules/prody/sequence/analysis.html#calcMeff). Once again the code was run as it is. 

## Results

In this section I display the results I got on my hardware. The implementations are extracted to separate notebooks for making this post bearable. While code might not be optimal, I did spend a significant amout of time trying to optimise the code. 

### Single threaded

| Code            | Threads | Time      |
| --------------- | ------- | --------- |
| [C++](https://zhanglab.dcmb.med.umich.edu/DeepMSA/) | 1       | 02:26.86  |
| [C](http://prody.csb.pitt.edu/_modules/prody/sequence/analysis.html#calcMeff) | 1       | 00:41.35  |
| [Pure Python](_notebooks/2020-04-05-gan-wgan.ipynb)   | 1       | ~7 hours* |
| [Numpy]()           | 1       | 00:32.51  |
| [Numba]()           | 1       | 00:26.63  |
| [Cython]()          | 1       | 00:32.43  |
| [Julia]()           | 1       | 04:51.00**|

\* Pure Python times were estimated on the timings I got on 100 sequences.

** I am quite sure that Julia can be faster and the developer is to blame for its poor performance.

The very first thing, Python is slow, very slow and if I would just compare Python vs C/C++ that would be the end of the story. However, the main strength of Python is its ecosystem. There are a lot of optimised libraries you can use (just to be clear, I have not tested all of them, only the ones I thought to be good to test) which improves performance drastically. In my case, Numpy, Cython and Numba implementations were faster than the C/C++, Numba being the fastest one (I have opted to use Fastmath option which sacrifices precision for speed, more about this in the notebook). In general, it seems that any optimized library could achieve C/C++ like performance.

### Multi threaded 

While you could try to optimize the performance of the algorithm till perfection, in practise relative optimized code that scales will be way faster than optimal one on single thread. You can see that in the table below. 

| Code            | Threads | Time     |
| --------------- | ------- | -------- |
| [Numpy]()       | 12      | 00:07.11 |
| [Numba]()       | 12      | 00:05.12 |
| [Tensroflow]()  | 12      | 00:39.88 |
| [Pytorch]()     | 12      | 00:39.14 |

Some notes: C and C++ implementation did not have support multi threaded execution. Numpy version utilized the multiprocessing library to do multithreading, while numba has built-in support for that. I skipped Julia and Cython due to time constraints. I have also introduced Tensorflow and Pytorch as my work is around developing deep learning models and I try to compare those frameworks whenever I have a chance. While Numba and Numpy performance was as expected - much faster on multiple threads (just to note: there is some overhead due to multithreading, but it is still worth scaling up), Tensorflow and Pytorch were both quite slow in comparison (I have to admit, not quite sure why). 

### With accelerator (GPU)

Nowadays, if you really want to go fast, you use accelerators such as GPU and TPU. While it requires to convert your code into the form that GPU likes (pretty much matrix multiplication), the gains sometimes are incredible. Even running on a mediocre GPU (Nvidia 1650GTX), I managed to have the best performance. What is more, Jax performance seems like out of this world, but I will cover the details of the implementations separately. 


| Code            | Threads | Time     |
| --------------- | ------- | -------- |
| [Tensorflow]()  | 1       | 00:06.10 |
| [Pytorch]()     | 1       | 00:08.05 |
| [JAX]()         | 1       | 00:00.13 |


## Conclusion

During this experiment I have not found anything that would be ground breaking or new. Nevertheless, I the findings are extremelly useful for myself. The main takeaways are:  

* Pure Python is slow.
* Optimised Python libraries can give you approximately C/C++ performance.
* Scaling to multiple threads or using GPU will give you the best performance. 
* Yet another thing which is not visible in the tables and is often overlooked is the solution itself. I have written some pieces several times to get these results (improving performance substantially). 

And if you were to ask me whether it is worth going to C/C++ for the performance reasons, I would say: unless you really need to squeeze every split of the second, you can stay in Python and be at least competitive with C/C++ performance, not to mention development/maintenance side of things. 

