
This project implements Gibbs sampling inference to LDA\(Latent Dirichlet Allocation\).

To-do:
1. Chenk convergence
2. speed up Gibbs sampling process

Reference:

@article{heinrich2005parameter,
  title={Parameter estimation for text analysis},
  author={Heinrich, G.},
  journal={Web: http://www.arbylon.net/publications/text-est.pdf},
  year={2005}
}

Note:
* The Gibbs sampling is very slow and it is hard to check convergence.
* The result is not very good; maybe because the corpus is not very large.
* The result can be very different in different runs.
