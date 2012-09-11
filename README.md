
This project implements Gibbs sampling inference to LDA\(Latent Dirichlet Allocation\).

To-do:
* Chenk convergence
* speed up Gibbs sampling process

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

Topic modeling tools:
* David Blei's collection: http://www.cs.princeton.edu/~blei/topicmodeling.html
* Mallet from UMass: http://mallet.cs.umass.edu/
* Stanford Topic Modeling Toolbox: http://nlp.stanford.edu/software/tmt/tmt-0.4/
* Matlab Topic Modeling Toolbox by Mark Steyvers and Tom Griffiths: http://psiexp.ss.uci.edu/research/programs_data/toolbox.htm
* LDA-J : http://www.arbylon.net/projects/
* R package: [topicmodels](http://cran.r-project.org/web/packages/topicmodels/vignettes/topicmodels.pdf) and [Topic models in R](http://cran.uvigo.es/web/packages/topicmodels/vignettes/topicmodels.pdf)
* topic-modeling-tool(A grapical user interface tool based on Mallet): http://code.google.com/p/topic-modeling-tool/
