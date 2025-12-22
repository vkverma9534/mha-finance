# mha-finance
mha-finance is a free Python framework for Multi-Horizon Statistical Modeling of Financial Time Series. It focuses on regime characterization, risk-return estimation, and horizon-dependent dynamics.

## Objectives of the project:
1. Statistically characterize monthly asset returns (A statistical estimation, not prediction).
2. 





## Problem statement definition for each Objective

### 1. Statistically characterize monthly asset returns (A statistical estimation, not prediction).


 **1 The objective is to statistically characterize monthly asset returns using historical price       data, without predicting future prices.**

  *Given historical daily price data over a sufficiently long period*
  *(e.g., 5 years for monthly estimation), the system estimates:*
    
  - The average realized monthly return
  - The dispersion of monthly returns
  - The uncertainty associated with estimated mean**
        
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
      *Final output format for 1 month as example horizon*
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
        

           

    
  
