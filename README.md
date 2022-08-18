# Analysis neuronal progenitor derived neurons 

## Calcium Imaging
For reprogramming, sensory progenitor cells are infected with a retroviral vector expressing Neurog1-Neurog2 and a red fluorescent protein (DsRed). Based on the DsRed signal, infected and not infected cells are distinguished. Calcium imaging was performed with Oregon Green 488 BAPTA-1 AM.

"functions.py":
Provided are functions to read the calcium imaging videos and extract, normalize, and low-pass filter the signal traces based on regions of interest (ROIs). 

"CI Pipeline - Reaction of infected cells.ipynb":
ROIs are perdicted with a deep learning model (StarDist2D) based on the DsRed (for infected cells) and Oregon Green 488 (for not infected cells) signal.
The ratios of infected and not infected cells that react to capsaicin or AITC were identified. A cell is counted as reacting when the derivative of the low-pass filtered signal reaches a uniform threshold. Results are plotted and statistically analyzed.


## Patch Clamp
Current clamp and voltage clamp experiments were performed to analyze electrophysiological properties of induced neurons compared to naive sensory neurons. Data were acquired using a HEKA EPC-10 USB patch-clamp amplifier controlled by the PatchMaster software (HEKA Electronic). Data was exported to ASCII files (without headers) with Fitmaster (HEKA Electronic) and can be imported into python numpy arrays with the Sweep class (sweep.py). Specific functions of voltage clamp (voltage_clamp.py) and current clamp (actionpotential.py, ap_trains.py) are added to the parent Sweep class.

### Current Clamp
"RMP.ipynb":
Extraction of resting membrane potentials (RMPs). Results are saved in a json file.

"AP_Single.ipynb":
Analysis of single action potentials (APs) elicited by increasing 3 ms pulses. Extracted are 'firing_threshold', 'amplitude_max', 'amplitude_min', 'spike_width_0mV', and 'spike_width' of the first first elicited AP. Results are saved in a json file. Example APs are plotted.

"Trains.ipynb":
Analysis of trains of APs elicited by increasing 300 ms pulses. Additionally to single AP parameters, the rheobase and the number and frequency of APs are determined. Results are saved in a json file. An exemplary AP train is plotted. 

"VC_currents.ipynb":
Extraction and plotting of voltage clamp inward and outward currents measured before switching to current clamp. Results are saved in a json file. 

"Plot_results.ipynb":
Results are imported from the json files, plotted, and statistically analyzed. 

"PC_parameters_all.xlsx":
Patch clamp parameters of all patched cells.

### Voltage Clamp
"example TTX on-thesis.ipynb":
Example on how to read and plot voltage clamp data (e.g. IV curve or signal traces). Original data is provided in the "2022-06-01_001_1" folder.

"TTX res. currents.ipynb":
IV-curves and quantification of TTX resistant currents.
