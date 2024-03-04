# spectra_entropy
Tool to calculate spectra entropy to measure the complexity of ms spectra

# Abstract
The diversity and complexity of the microbiome's genomic landscape are not always mirrored in its proteomic profile. Despite the anticipated proteomic diversity, observed complexities of microbiome sample are often lower than expected. Two main factors contribute to this discrepancy: bioinformatics challenges in metaproteomics identification and limitations in mass spectrometry's detection sensitivity. The study introduces a novel approach to evaluating sample complexity directly at the mass spectrum level rather than relying on peptide identifications. When analyzing under identical mass spectrometry conditions, microbiome samples displayed significantly higher complexity, as evidenced by the spectral entropy and number of peptide features, compared to single-species samples. The research provides solid evidence for the complexity of microbiome in proteomics indicating the optimization potential of the bioinformatics workflow.


This tool is based on python and used to calculate spectral entropy. 
Please convert mass spectrometry raw data into .ms1 using the MSconvert (https://proteowizard.sourceforge.io/download.html), then input .ms1 file to "Spectral Entropy calculator".
The output file contains the following columns:
1.Spectra entropy
2.Normalized spectra entropy
3.Number of peaks, TIC(total ion chromatogram)
4.Retention time (RT)
5.Scan number
6.Base Peak Mass (BPM)



