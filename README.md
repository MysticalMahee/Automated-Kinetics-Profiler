# Automated Reaction Kinetics Profiler

## Objective
To build an automated, programmatic pipeline that determines chemical reaction orders and rate constants directly from raw time-concentration data. This script replaces manual, error-prone Excel curve-fitting with a clean Python workflow. We will do a simple analysis on the rate order reactions for dinitrogen pentoxide,  N<sub>2</sub>O<sub>5</sub>, which decomposes to NO<sub>2</sub> and NO<sub>3</sub>.


## Source of Information
All values that I have used are random and not actual data, but ideas were inspired from the following website:
https://kinetics.nist.gov/kinetics/index.jsp . The following screenshots below shall show what to do to get to the following data we are interested to see:

<img width="1421" height="987" alt="image" src="https://github.com/user-attachments/assets/f043f35e-97ab-486f-9cea-e2d9d1f99b8c" />

<img width="1425" height="986" alt="image" src="https://github.com/user-attachments/assets/c6b71229-df65-4327-9b4a-99b0ccebd5a6" />

<img width="1421" height="993" alt="image" src="https://github.com/user-attachments/assets/25f95f8d-9c69-4215-a2c9-e850b13d94d8" />


## Methodology
The pipeline ingests raw instrumental data and applies mathematical transformations to test for Zero-Order ($[A]$), First-Order ($\ln[A]$), and Second-Order ($1/[A]$) kinetics. Using `scipy.stats.linregress`, the script automatically identifies the true reaction order by evaluating which integrated rate law yields the highest coefficient of determination ($R^2$). 


<h2>Technical Highlights & Developer Notes</h2>

There are some parts of the code in which users can play and test around to see what will happen if some values are changed, and below I will show some main points that WILL matter.

<h3>Phase 1: Data Generation & Pre-Processing</h3>
<ul>
    <li>
        <strong><code>df_clean = df[df['concentration'] > 0].copy()</code></strong><br>
        <strong>Purpose:</strong> Filters out any negative concentrations (hence why the 51st value in the `scipy.stats.linregress` is not present). At the tail end of the reaction, simulated instrument noise can push near-zero concentration values below zero. Attempting to pass negative numbers into a natural log function ($\ln(x)$) throws a <code>NaN</code> error and crashes the regression model. 
        <br><strong>The <code>.copy()</code> function:</strong> This explicitly tells Pandas to allocate a new, isolated block of memory for the filtered data. Without it, Pandas tracks <code>df_clean</code> as a "view" of the original dataframe, which triggers a <code>SettingWithCopyWarning</code> when we attempt to append the new mathematical transformation columns later.
    </li>
    <li>
        <strong><code>time_s = np.linspace(0, 60, 60)</code></strong><br>
        <strong>Purpose:</strong> Defines the sampling window and data density. 
        <br><strong>The "Goldilocks" Principle:</strong> For a rate constant of $k = 0.06$ s⁻¹, the half-life is roughly $11.55$ seconds. A 60-second window captures ~5 half-lives, which is the physical chemistry gold standard for kinetic profiling. 
        <ul>
            <li><em>Too high (e.g., 1000 points over 1000s):</em> The chemical is entirely depleted by 100s. The remaining 900s would sample pure baseline instrument noise. Taking the natural log of baseline noise creates massive scatter, destroying the $R^2$ value.</li>
            <li><em>Too low (e.g., 10 points over 60s):</em> Yields insufficient data density to achieve statistical confidence in the linear regression. 60 points perfectly mimics a standard 1 Hz UV-Vis spectrometer acquisition rate.</li>
        </ul>
    </li>
    <li>
        <strong><code>np.random.seed(20)</code></strong><br>
        <strong>Purpose:</strong> Initializes the pseudo-random number generator for reproducibility. By locking the seed to a specific integer (like 20), the script applies the exact same sequence of simulated baseline noise on every execution. Changing this integer will apply a different noise distribution, which marginally shifts the data scatter and results in slightly different final $R^2$ values.
    </li>
</ul>

<hr>

### Phase 2: SciPy Analytics & Mathematical Derivations

#### 1. The Kinetic Transformations
Linear regression algorithms strictly calculate the fit of a straight line ($y = mx + c$). Because chemical concentrations decay exponentially, we use integration to mathematically straighten the data. Below are the derivations proving these transformations:

**Zero-Order Reaction (No Transformation)**
The rate is independent of concentration.

$$-\frac{d[A]}{dt} = k$$

$$\int_{[A]_0}^{[A]_t} d[A] = -k \int_{0}^{t} dt$$

$$[A]_t = -kt + [A]_0$$

*Plotting $[A]_t$ vs $t$ yields a straight line with slope $-k$.*

**First-Order Reaction (Natural Log Transformation)**
The rate is directly proportional to concentration.

$$-\frac{d[A]}{dt} = k[A]$$

$$\int_{[A]_0}^{[A]_t} \frac{1}{[A]} d[A] = -k \int_{0}^{t} dt$$

$$\ln[A]_t = -kt + \ln[A]_0$$

*Plotting $\ln[A]_t$ vs $t$ yields a straight line with slope $-k$.*

**Second-Order Reaction (Reciprocal Transformation)**
The rate is proportional to the square of the concentration.

$$-\frac{d[A]}{dt} = k[A]^2$$

$$\int_{[A]_0}^{[A]_t} \frac{1}{[A]^2} d[A] = -k \int_{0}^{t} dt$$

$$-\left( \frac{1}{[A]_t} - \frac{1}{[A]_0} \right) = -kt$$

$$\frac{1}{[A]_t} = kt + \frac{1}{[A]_0}$$

*Plotting $1/[A]_t$ vs $t$ yields a straight line with slope $k$.*

<h4>2. The Regression Pipeline</h4>
<ul>
    <li>
        <strong><code>time_s = df_clean["time"]</code></strong><br>
        <strong>Purpose:</strong> Isolates the independent variable (X-axis) directly from the filtered dataset, ensuring the length of the time array perfectly matches the cleaned concentration arrays.
    </li>
    <li>
        <strong><code>zero_fit = linregress(time_s, df_clean["zero_order"])</code></strong> (and subsequent fits)<br>
        <strong>Purpose:</strong> Executes an Ordinary Least Squares (OLS) regression on all three kinetic models simultaneously to determine the slope, intercept, and correlation.
    </li>
    <li>
        <strong><code>zero_r_squared = zero_fit.rvalue ** 2</code></strong><br>
        <strong>Purpose:</strong> <code>linregress</code> returns Pearson's correlation coefficient ($r$). Squaring it gives the coefficient of determination ($R^2$), representing the percentage of data variance strictly explained by the linear model.
    </li>
    <li>
        <strong><code>print(f"... {zero_r_squared:.4f}")</code></strong><br>
        <strong>Purpose:</strong> The <code>:.4f</code> forces Python to format the floating-point output to exactly 4 decimal places, adhering to analytical chemistry reporting standards.
    </li>
    <li>
        <strong><code>best_fit = max(...)</code> and Decision Logic</strong><br>
        <strong>Purpose:</strong> This acts as the automated decision engine. Because the correct integrated rate law perfectly straightens the decay curve, the script logically deduces that the model with the $R^2$ closest to 1.0 represents the true reaction order.
    </li>
</ul>

<hr>

<h3>Phase 3: Matplotlib Visualization</h3>
<ul>
    <li>
        <strong><code>fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))</code></strong><br>
        <strong>Purpose:</strong> Initializes a Figure object (the overall canvas) and creates an array of three distinct Axes objects (subplots) arranged in 1 row and 3 columns. The <code>figsize=(15, 5)</code> ensures the output is properly scaled for a README image without squashing the data.
    </li>
</ul>

<h4>Anatomy of a Subplot Block</h4>
<pre><code>ax1.scatter(time_s, df_clean['zero_order'], color='red', alpha=0.6, label='Simulated Data')
zero_line = zero_fit.slope * time_s + zero_fit.intercept
ax1.plot(time_s, zero_line, color='black', linestyle='--', label='Fit')
ax1.set_title(f"Zero Order\nR² = {zero_r_squared:.4f}")
ax1.set_xlabel("Time (s)")
ax1.set_ylabel("[N2O5]")
ax1.legend()
</code></pre>
<ul>
    <li><strong><code>ax1.scatter(...)</code>:</strong> Plots the raw laboratory data as individual points. <code>alpha=0.6</code> adds transparency so overlapping points remain visible.</li>
    <li><strong><code>zero_line = ...</code>:</strong> Mathematically constructs the theoretical trendline using the classical $y = mx + c$ equation derived from the SciPy regression.</li>
    <li><strong><code>ax1.plot(...)</code>:</strong> Overlays the calculated trendline onto the scattered data.</li>
    <li><strong><code>ax1.set_title(...)</code> & labels:</strong> Injects the dynamically calculated $R^2$ values directly into the chart header and applies standard SI unit labels to the axes.</li>
</ul>



## Visual Validation
The script utilizes `matplotlib` to generate a side-by-side diagnostic plot, proving the mathematical output. As demonstrated below, the pipeline successfully identified the simulated $N_2O_5$ decomposition data as a First-Order reaction.

<img width="1439" height="1006" alt="image" src="https://github.com/user-attachments/assets/dc6ea304-3113-4965-8896-7bc726edc629" />


## Tech Stack
* **Data Processing:** `pandas`, `numpy`
* **Statistical Modeling:** `scipy`
* **Visualization:** `matplotlib`
