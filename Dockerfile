FROM python:3.10

# install latest R version
RUN apt-get update && apt-get install -y --no-install-recommends bedtools build-essential r-base r-base-dev

# install FACETS package and additional package for easier interpretation of results
RUN R -e "install.packages('remotes')"
RUN R -e "remotes::install_github('mskcc/facets')"

ARG PATH="/root/miniconda3/bin:${PATH}"
ENV PATH="/root/miniconda3/bin:${PATH}"
RUN wget \
    https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh \
    && mkdir /root/.conda \
    && bash Miniconda3-latest-Linux-x86_64.sh -b \
    && rm -f Miniconda3-latest-Linux-x86_64.sh \
    && conda config --add channels defaults \
    && conda config --add channels bioconda \
    && conda config --add channels conda-forge
RUN conda install -y -c bioconda cnv_facets

COPY requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app


# TODO: part below exists only because CNA_genes is a .json file with gene names and not .bed with their coordinates
# TODO: so we need to download hg38 annotation and create .bed file by finding genes coordinates in annotation
# install BEDOPS
RUN wget https://github.com/bedops/bedops/releases/download/v2.4.41/bedops_linux_x86_64-v2.4.41.tar.bz2
RUN tar jxvf bedops_linux_x86_64-v2.4.41.tar.bz2
RUN cp bin/* /usr/local/bin
# download hg38 annotation
RUN wget ftp://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_human/release_38/gencode.v38.annotation.gff3.gz \
    | gunzip --stdout - \
    | awk '$3 == "gene"' - \
    | convert2bed -i gff - \
    > /app/data/genes.bed


ENTRYPOINT ["python3", "-u", "/app/scripts/analysis.py"]