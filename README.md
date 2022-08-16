# Analysis of nociceptive neurons reprogrammed from neuronal progenitor cells

## Calcium Imaging
For reprogramming, sensory progenitor cells are infected with a retroviral vector expressing Neurog1-Neurog2 and a red fluorescent protein (DsRed). Based on the DsRed signal, infected and not infected cells are distinguished. Calcium imaging was performed with Oregon Green 488 BAPTA-1 AM.
### functions.py
Provided are functions to read the calcium imaging videos and extract, normalize, and low-pass filter the signal traces based on regions of interest (ROIs). 
### CI Pipeline - Reaction of infected cells.ipynb
ROIs are perdicted with a deep learning model (StarDist2D) based on the DsRed (for infected cells) and Oregon Green 488 (for not infected cells) signal.
The ratios of infected and not infected cells that react to capsaicin or AITC were identified. A cell is counted as reacting ff the derivative of the low pass filtered signal reached a uniform threshold. Results are plotted and statistically analyzed.
