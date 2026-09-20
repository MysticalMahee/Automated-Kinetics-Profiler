# Automated-Kinetics-Profiler

## Objective
To build an automated, programmatic pipeline that determines chemical reaction orders and rate constants directly from raw time-concentration data. This script replaces manual, error-prone Excel curve-fitting with a clean Python workflow. 

## Methodology
The pipeline ingests raw instrumental data and applies mathematical transformations to test for Zero-Order ($[A]$), First-Order ($\ln[A]$), and Second-Order ($1/[A]$) kinetics reactions. Using `scipy.stats.linregress`, the script automatically identifies the true reaction order by evaluating which integrated rate law yields the highest coefficient of determination ($R^2$). 

## Visual Validation
The script utilizes `matplotlib` to generate a side-by-side diagnostic plot, proving the mathematical output. As demonstrated below, the pipeline successfully identified the simulated $N_2O_5$ decomposition data as a First-Order reaction.

![Kinetics Fit](Kinetics_Analysis_Result.png)

## Tech Stack
* **Data Processing:** `pandas`, `numpy`
* **Statistical Modeling:** `scipy`
* **Visualization:** `matplotlib`

## How to Run
1. Clone the repository.
2. Install dependencies via `pip install -r requirements.txt`.
3. Run `python kinetics_analyzer.py`. The script will output the calculated $R^2$ values to the terminal and generate the diagnostic plot.
