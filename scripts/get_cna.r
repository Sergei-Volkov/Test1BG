library(facets)
# pileup_path <- commandArgs(trailingOnly = TRUE)
pileup_path <- "data/pileup.txt"
set.seed(1234)
rcmat <- readSnpMatrix(pileup_path)
xx <- preProcSample(rcmat)
# TODO: parameter cval can be adjusted based on "spider" plot
oo <- procSample(xx, cval = 400)
fit <- emcncf(oo)
# fit$purity
# fit$ploidy
# plotSample(x = oo, emfit = fit)
# logRlogORspider(oo$out, oo$dipLogR)
names(fit)
snp
