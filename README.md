# Automated Reaction Kinetics Profiler

## Objective
To build an automated, programmatic pipeline that determines chemical reaction orders and rate constants directly from raw time-concentration data. This script replaces manual, error-prone Excel curve-fitting with a robust Python workflow. We will do a simple analysis on the rate order reactions for dinitrogen pentoxide,  N<sub>2</sub>O<sub>5</sub>, which decomposes to NO<sub>2</sub> and NO<sub>3</sub>.


## Source of Information
All values that I have used are random and not actual data, but ideas were received from the following website:
https://kinetics.nist.gov/kinetics/index.jsp . The following screenshots below shall show what to do to get to the following data we are interested to see:

<img width="1421" height="987" alt="image" src="https://github.com/user-attachments/assets/f043f35e-97ab-486f-9cea-e2d9d1f99b8c" />

<img width="1425" height="986" alt="image" src="https://github.com/user-attachments/assets/c6b71229-df65-4327-9b4a-99b0ccebd5a6" />

<img width="1421" height="993" alt="image" src="https://github.com/user-attachments/assets/25f95f8d-9c69-4215-a2c9-e850b13d94d8" />


## Methodology
The pipeline ingests raw instrumental data and applies mathematical transformations to test for Zero-Order ($[A]$), First-Order ($\ln[A]$), and Second-Order ($1/[A]$) kinetics. Using `scipy.stats.linregress`, the script automatically identifies the true reaction order by evaluating which integrated rate law yields the highest coefficient of determination ($R^2$). 

## Visual Validation
The script utilizes `matplotlib` to generate a side-by-side diagnostic plot, proving the mathematical output. As demonstrated below, the pipeline successfully identified the simulated $N_2O_5$ decomposition data as a First-Order reaction.

<img width="1439" height="1006" alt="image" src="https://github.com/user-attachments/assets/dc6ea304-3113-4965-8896-7bc726edc629" />


## Tech Stack
* **Data Processing:** `pandas`, `numpy`
* **Statistical Modeling:** `scipy`
* **Visualization:** `matplotlib`
