This is a repository for detecting CNA variants in tumor based on SNP data. 

**Build**

To run program you need to
* build Docker image `docker build -t <image name> ./`
* run Docker container `docker run --rm <image name> -p <path to pileup file> -v <path to vcf file with somatic mutations> -g <path to genes of interest (bed file of json file with genes names)>`
* `-g` argument is not required although preferable

CNA variants detection is done with a help of FACETS tool [1]. It was chosen based on few observations:
* Not all CNA variants detection tools estimate clonality in their calculations. FACETS does that.
* FACETS quantifies somatic CNA variants more accurately than other tools (Sclust, Sequenza, TITAN) [2].

**References**

[1] Shen R, Seshan VE. FACETS: allele-specific copy number and clonal heterogeneity analysis tool for high-throughput DNA sequencing. Nucleic Acids Res. 2016 Sep 19;44(16):e131. doi: 10.1093/nar/gkw520. Epub 2016 Jun 7. PMID: 27270079; PMCID: PMC5027494.

[2] Tanner G, Westhead DR, Droop A, Stead LF. Benchmarking pipelines for subclonal deconvolution of bulk tumour sequencing data. Nat Commun. 2021 Nov 4;12(1):6396. doi: 10.1038/s41467-021-26698-7. PMID: 34737285; PMCID: PMC8569188.