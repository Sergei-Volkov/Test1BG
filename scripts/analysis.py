import argparse
import json
from pathlib import Path
import subprocess

from logger import get_module_logger

logger = get_module_logger(__name__)


def find_cna(pileup_path: Path) -> ...:
    subprocess.run(
        ("cnv_facets.R", "-p", str(pileup_path), "-o", Path.cwd() / "data" / "cnv")
    )
    subprocess.run(("ls", "data"), capture_output=True)


# TODO: 2 functions below exist to convert .json file containing a list of genes to .bed with coordinates
def get_gene_names(genes_path: Path) -> list[str]:
    with open(genes_path) as f:
        genes_data = json.load(f)
        return genes_data["genes"]


def create_cna_genes_bed(genes_path: Path) -> None:
    with open("gene_names.tmp", "w") as f:
        gene_names = get_gene_names(genes_path)
        for name in gene_names:
            f.write(name + "\n")
    with open(genes_path.parent / (str(genes_path.stem) + ".bed"), "w") as f:
        subprocess.run(
            ("grep", "-Fwf", "gene_names.tmp", str(Path.cwd() / "data" / "genes.bed")),
            stdout=f,
        )
    subprocess.run(("rm", "gene_names.tmp"))


# GOI = genes of interest
def intersect_vcf_with_goi(genes_path: Path, vcf_path: Path) -> None:
    with open(vcf_path.parent / (str(vcf_path.stem) + "-intersect.vcf"), "w") as f:
        subprocess.run(
            ("bedtools", "intersect", "-a", str(vcf_path), "-b", str(genes_path)),
            stdout=f,
        )


def read_vcf(vcf_path: Path) -> ...:
    ...


def main(pileup_path: Path, vcf_path: Path, genes_path: Path | None) -> None:
    # TODO: template for transformation .json -> .bed
    if genes_path is not None and genes_path.suffix == ".json":
        logger.info("Creating .bed file for provided genes list")
        create_cna_genes_bed(genes_path)
        genes_path = genes_path.parent / (str(genes_path.stem) + ".bed")

    if genes_path is not None:
        logger.info("Intersecting VCF with genes of interest")
        intersect_vcf_with_goi(genes_path, vcf_path)
    vcf_intersect_path = vcf_path.parent / (str(vcf_path.stem) + "-intersect.vcf")
    subprocess.run(("cp", str(vcf_path), str(vcf_intersect_path)))

    find_cna(pileup_path)
    ...


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Data files required for CNA variants search."
    )
    parser.add_argument(
        "-p", "--pileup", help="Path to pileup file.", type=Path, required=True
    )
    parser.add_argument(
        "-v",
        "--vcf",
        help="Path to .vcf file with somatic mutations.",
        type=Path,
        required=True,
    )
    parser.add_argument(
        "-g",
        "--genes",
        help="Path to .bed (or .json {'genes': [...]}) file with genes of interest.",
        type=Path,
    )

    logger.info("Parsing arguments")
    args = parser.parse_args()

    main(args.pileup, args.vcf, args.genes)
