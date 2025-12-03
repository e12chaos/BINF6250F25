#script for downloading UTR data
#bedtools is required!
#!/bin/bash

# Set up Ensembl release and file names
RELEASE=110
GTF="Homo_sapiens.GRCh38.${RELEASE}.gtf.gz"
GENOME="Homo_sapiens.GRCh38.dna.primary_assembly.fa.gz"

# Download GTF annotation and genome FASTA
echo "Downloading GTF annotation..."
wget ftp://ftp.ensembl.org/pub/release-${RELEASE}/gtf/homo_sapiens/${GTF}

echo "Downloading genome FASTA..."
wget ftp://ftp.ensembl.org/pub/release-${RELEASE}/fasta/homo_sapiens/dna/${GENOME}

# Uncompress files
echo "Uncompressing files..."
gunzip ${GTF}
gunzip ${GENOME}

# Extract 5' UTR coordinates to BED format
echo "Extracting 5' UTR coordinates..."
awk '$3=="five_prime_utr"' Homo_sapiens.GRCh38.${RELEASE}.gtf | \
awk 'BEGIN{OFS="\t"} {print $1, $4-1, $5, "transcript_id:" $14 ";gene_id:" $10, ".", $7}' > five_prime_utr.bed

# Check if BED file was created and has content
if [ -s five_prime_utr.bed ]; then
    echo "Found $(wc -l < five_prime_utr.bed) 5' UTR features"
else
    echo "Warning: No 5' UTR features found!"
    exit 1
fi

# Extract 5' UTR sequences from genome using bedtools
echo "Extracting sequences with bedtools..."
bedtools getfasta -fi Homo_sapiens.GRCh38.dna.primary_assembly.fa \
    -bed five_prime_utr.bed \
    -s \
    -name \
    -fo human_five_prime_utrs.fa

echo "Done! Output saved to human_five_prime_utrs.fa"
echo "Total sequences: $(grep -c '^>' human_five_prime_utrs.fa)"
