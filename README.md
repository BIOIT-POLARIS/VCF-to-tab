# VCF-to-tab
Converts Variant Effect Predictor (VEP) VCF output to tab-delimited file.

```
$ python convert_vep_vcf_to_tsv_py3x.py -h
usage: convert_vep_vcf_to_tsv_py3x.py [-h] [-o OUTPUT_FILE] [-t] [-s] [-g]
                                      [-d TRANSCRIPT_DELIMITER]
                                      input_file

convert_vep_vcf_to_tsv_py3x.py: Converts VEP VCF output to tab-delimited file.

positional arguments:
  input_file            Name of VEP VCF input file to be converted to tab-
                        delimited format.

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT_FILE, --output_file OUTPUT_FILE
                        Name of file to which to output tab-delimited version
                        of input file. (Default: standard output.)
  -t, --expand_transcripts
                        Put each transcript in a separate row. (Default:
                        Combine all transcripts into a single row.)
  -s, --expand_samples  Put each sample in a separate row. (Default: Leave
                        each sample in a different column, in a single row.)
  -g, --expand_genotype
                        Separate genotype data into columns. Assumes colon
                        delimiter.(Default: Leave genotype data as is.)
  -d TRANSCRIPT_DELIMITER, --transcript_delimiter TRANSCRIPT_DELIMITER
                        Delimiter between transcript values in each category.
                        (Default: |) Has no effect when --expand_transcripts
                        is True.
```

