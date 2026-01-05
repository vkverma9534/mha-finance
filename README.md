# mha-finance
mha-finance is a free Python framework for Multi-Horizon Statistical Modeling of Financial Time Series. It focuses on regime characterization, risk-return estimation, and horizon-dependent dynamics.

## Objectives of the project:
1. Statistically characterize horizon-wise asset returns (A statistical estimation, not prediction).
2. Statistically characterize horizon-wise asset volatility.





## Problem statement definition for each Objective

### 1. Statistically characterize horizon-wise asset returns (A statistical estimation, not prediction).


 **1 The objective is to statistically characterize horizon-specific asset returns using historical price data, without predicting future prices.**

  *Given historical daily price data over a sufficiently long period*
  *(e.g., 5 years for monthly estimation), the system estimates:*
    
  - The average realized monthly return
  - The dispersion of horizon-specific returns
  - The uncertainty associated with estimated mean
        
   All estimates are descriptive and inferential, not predictive.

 **2 Scope of the Objective**

  *In scope* 
     
  - Statistical estimation 
  - Rolling window analysis
  - Return Characterization
  - Uncertainty quantification

  *Out of scope*

  - Price prediction
  - Trading strategies

 **3 Horizon based data span selection** 

  - *Intra-Day estimation*:-
  A 5 Minute interval data of 50 Days
      
  - *Weekly estimation*:-
  A daily interval data of 2 years
      
  - *Monthly estimation*:-
  A daily interval data of 5 years
      
  - *Annual estimation*:-
  A daily interval data of 15 years

 **4 Steps for achieving this objective**

* Step 1-- Data Ingestion
   
   Data Based on horizon is loaded and cleaned
     - Incomplete current-day records are removed.
       
     - Data is sorted chronologically.

* Step 2-- Return Construction
  
   Horizon-based log returns are computed from closing prices for each
   
   interval specified by the horizon selection (see 3):
  
     - Let P_t be the closing price on day t.

     - Declare horizon (H) based on selection of user 
             (eg. H=21 for Monthly horizon by user)
  
     - The return ending at at time t is:
                      r_t^(H) = log(P_t) - log(P_{t-H})
  
     This produces a time series of realized monthly returns.

* Step 3-- Rolling estimation window

  Rolling estimation window
  
   - W = Data Span for the horizon / Horizon Length.
     
   - Returns inside the window are assumed locally stationary.
     
   - This Window defines the data used for estimation.
  
   - Each rolling window defines the data used for statistical estimation.

* Step 4-- Statistical estimation
    
    Within Rolling Window
  
   - Mean horizon return (μ̂^(H))
       μ̂^(H) = (1 / W) * Σ r_t^(H)
       Represents the average realized Horizon return.
     
   - Return dispersion (sample Variance)
        D̂^(M) = (1 / (W − 1)) * Σ (r_t^(M) − μ̂^(M))²

        Represents the empirical dispersion of monthly returns 
        (not volatility modeling)

 **5 Output Structure**

  *Final output format for 1 month as example horizon*
  
    ReturnSummary(
        mean,                 # Estimated mean monthly return
        variance,             # Sample dispersion of monthly returns
        confidence_interval,  # Uncertainty of the mean
        window_used={
            "horizon": "monthly",
            "frequency": "daily",
            "lookback": "5 years",
            "effective_samples": 60
        }
    )

 **6 Concepts Involved**
      
  Concepts Of Finance
        
        Log returns
        Time horizons
        Rolling windows
        Non-stationarity
        Risk vs return (descriptive)
        
  Concepts of Statistics

        Sample Mean
        Sample Variance
        Confidence Interval
        Bootstrap inference
        Effective sample size
        
  *Machine learning is intentionally not used to avoid unjustified prediction*

  ### 2. Statistically characterize horizon-wise asset volatility (Statistically estimation of conditional variabilty).
  
   **1 The objective is to statistically characterize horizon-specific asset returns using historical price data, without predicting future volatility or market movements.**

  *Given historical daily price data over a sufficiently long period and at an appropriate sampling frequency,*
  *depending on horizon we must have long lookback window. The system estimates the recent conditional variability*
  *of returns, along with measures of uncertainty and stability.*

   Specifically, the framework estimates:
  - The realized or conditional volatility at a given horizon
  - The dispersion and variability of volatility estimates across rolling windows
  - Diagnostic measures indicating the stability or degradation of volatility estimatprs
        
   All estimates are descriptive and inferential, not predictive.
   
 **2 Scope of the Objective**

  *In scope* 
     
  - Statistical volatility estimation 
  - Rolling and window-based estimators
  - Horizon specific volatility Characterization
  - Uncertainty and stability diagnostics
  - Conditional and regime-aware volatility

  *Out of scope*

  - Volatility prediction or forecasting
  - Profit or risk optimization
  - Trading, hedging, or portfolio construction strategies
  - Automated decision-making or alerts

 **3 Horizon based data span selection** 

  - *Intra-Day estimation*:-
  A daily interval data of 70 Days
      
  - *Weekly estimation*:-
  A daily interval data of 2 years
      
  - *Monthly estimation*:-
  A daily interval data of 5 years
      
  - *Annual estimation*:-
  A daily interval data of 15 years

 **4 Steps for achieving this objective**

* Step 1-- Data Ingestion
   
   Data Based on horizon is loaded and cleaned
     - Incomplete current-day records are removed.
       
     - Data is sorted chronologically.

* Step 2-- Return Series construction

  Volatility estimation is performed on returns, not prices.
    - Let Pt denote the closing price at time t.
      
    - Log returns are consrtructed at the base sampling frequency:
          rt = log(Pt)-log(Pt-1)
  This produces a time series of realized returns, which serves as the
  input for volatility estimation.

  (Note: The return frequency is decoupled from estimation horizon. Higher
  frequency returns may be used to characterize lower-frequency volatility.)]

* Step 3-- Rolling estimation window

  A rolling estimation window is defined to support conditional and adaptive
  estimation
    - Let W denote the number of observations in the rolling window.
    - Window length is determined by:
       - hoizon selection
       - required historical depth
    - Returns within each window are assumed locally stationary.

* Step 4-- Statistical volatility estimation

  Within each rolling window,, volatility is estimated using statistical estimators, 
  not predictive models

  Typical estimators include:
  - Sample varince
      σ^2 = (1\(W-1))*∑(rt-rˉ)^2
  - Rolling standard deviation
      σ = (σ^2)^(1/2)
  - Exponentially Weighted Moving Average (EWMA)
      σ(t)^2 = λσ(t-1)^2 + (1-λ)r(t)^2

  These estimators characterize recent conditional variability. not future risk.

* Step 5-- Volatility uncertainty and dispersion analysis

  Beyond point estimation, the framework evaluates uncertainty and robustness of
  volatility estimates.
    - Dispersion of volaility estimates across windows
    - Sensitivity to window length
    - Temporal smoothness or clustering behavior

  This step quantifies how stable or unstable volatility estimates are over time.

* Step 6-- Stabilty diagnostics

  Stability diagnostics are computed to assess whether volatility assumptions remain valid.

    - Detection of abrupt changes in variability
    - Parameter drift (for conditional estimators)
    - Breakdown of local stationary assumptions

  These diagnostics flag instability but do not trigger automated actions.

**5 Output construction and delivery**

  For each horizon and evaluation point, the framewok outputs a structured volatility
  summary:
  
    - Estimated volatility level
    - Associated uncertainty measures
    - Stability indicators
    - Metadata:
        - horizon
        - window size
        - estimator used
        - data span
        
  This output is descriptive, interpretable, and reproducible.
  
 **6 Concepts Involved**
      
  Concepts Of Finance
        
            Log-returns  
            Realized volatility  
            Conditional volatility  
            Volatility clustering  
            Volatility persistence  
    

        
  Concepts of Statistics

            Squared returns  
            Rolling variance  
            Rolling standard deviation  
            Exponentially weighted moving averages (EWMA)  
            Sensitivity to window length  




