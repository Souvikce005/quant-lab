# Quant Lab - Simulation Stage Architecture Plan (Interest Rates Focus)

## Executive Summary
This plan defines the codebase architecture for **Phase 2 (Market Simulation)** of Quant Lab, specifically targeting **interest rate simulation** as the first deliverable. The architecture will follow a modular, extensible design enabling future additions of FX and credit spread simulations.

## Scope: Simulation Stage - Interest Rates Only

**In Scope:**
- Hull-White one-factor model implementation
- Market data ingestion and calibration
- Monte Carlo path generation
- Scenario cube construction (Scenario × Simulation Date × Risk Factor)
- Configuration management (YAML)

**Out of Scope (Later Phases):**
- FX rate simulation (GBM)
- Credit spread simulation (CIR)
- Multi-currency correlations
- Advanced pricing models (SABR, Heston)

---

## Proposed Directory Structure

```
quant-lab/
├── Simulation/
│   └── Rates/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── base.py                    # Abstract base classes
│       │   ├── hull_white.py              # Hull-White 1F model
│       │   └── validators.py              # Model validation utilities
│       ├── calibration/
│       │   ├── __init__.py
│       │   ├── calibrator.py              # Base calibrator
│       │   ├── hw_calibrator.py           # Hull-White calibration
│       │   └── optimization.py            # Optimization routines
│       ├── simulation/
│       │   ├── __init__.py
│       │   ├── engine.py                  # Monte Carlo engine
│       │   ├── path_generator.py          # Path generation logic
│       │   └── correlation.py             # Correlation matrix handling
│       ├── data/
│       │   ├── __init__.py
│       │   ├── market_data.py             # Market data container
│       │   ├── curve.py                   # Interest rate curves
│       │   └── loaders.py                 # Data loading utilities
│       ├── config/
│       │   ├── __init__.py
│       │   ├── schema.py                  # Configuration schemas (Pydantic)
│       │   └── default_config.yaml        # Default settings
│       └── tests/
│           ├── __init__.py
│           ├── test_models/
│           ├── test_calibration/
│           ├── test_simulation/
│           └── test_data/
├── Input_Data/
│   ├── market_data/
│   │   └── spot_rates.csv                # Initial curve data
│   ├── config/
│   │   └── simulation_config.yaml        # Simulation parameters
│   └── calibration/
│       └── calibration_data.csv          # Calibration instrument prices
└── tests/
    └── integration/
        └── test_simulation_end_to_end.py
```

---

## Core Architectural Components

### 1. **Data Layer** (`data/`)
Handles market data ingestion, curve construction, and storage.

**Components:**
- **`market_data.py`**: Container for yield curves, spot rates, and metadata
- **`curve.py`**: Interest rate curve representation (flat, interpolation methods)
- **`loaders.py`**: Load data from CSV, Excel, or APIs

**Interfaces:**
```python
class YieldCurve:
    """Represents a discount/forward curve"""
    - forward_rate(tenor: float) -> float
    - discount_factor(tenor: float) -> float
    - spot_rate(tenor: float) -> float

class MarketData:
    """Container for curves and calibration data"""
    - discount_curve: YieldCurve
    - foward_curves: Dict[str, YieldCurve]
    - volatility_surface: Optional
```

---

### 2. **Model Layer** (`models/`)
Implements mathematical models for interest rate dynamics.

**Base Architecture:**
```python
class StochasticModel(ABC):
    """Abstract base for all stochastic rate models"""
    
    @abstractmethod
    def calibrate(self, market_data: MarketData, config: ModelConfig) -> None
        """Fit model parameters to market data"""
    
    @abstractmethod
    def generate_paths(self, dates: np.ndarray, n_paths: int, 
                      seed: int) -> np.ndarray
        """Generate Monte Carlo paths"""

class HullWhiteOneFactor(StochasticModel):
    """Hull-White 1-factor model
    
    dr(t) = [θ(t) - α·r(t)]dt + σ·dW(t)
    
    Attributes:
        - alpha: Mean reversion speed
        - sigma: Volatility
        - theta: Time-dependent drift (fitted to curve)
    """
    
    Parameters to estimate:
    - alpha (mean reversion)
    - sigma (volatility)
```

**Key Methods:**
- `calibrate()`: Calibrate α and σ to cap/floor implied volatilities
- `generate_paths()`: Use Euler or exact discretization

---

### 3. **Calibration Layer** (`calibration/`)
Estimates model parameters from market data.

**Strategy:**
- **Input**: Swap rates, cap/floor prices, volatility term structures
- **Optimization Target**: Minimize pricing error on liquid instruments
- **Algorithm**: Scipy.optimize (Levenberg-Marquardt or differential evolution)

**Components:**
```python
class HullWhiteCalibrator:
    """Calibrates Hull-White parameters"""
    - objective_function()     # Pricing error to minimize
    - calibrate()              # Run optimization
    - sensitivity_analysis()   # Check stability
```

---

### 4. **Simulation Engine** (`simulation/`)
Generates correlated Monte Carlo paths.

**Core Logic:**
```python
class MonteCarloEngine:
    """Main simulation orchestrator"""
    
    def run_simulation(
        self,
        model: StochasticModel,
        market_data: MarketData,
        config: SimulationConfig
    ) -> ScenarioCube:
        """
        Generate scenario cube: [n_scenarios, n_dates, n_factors]
        """
        - Initialize random number generator (seeded)
        - Generate paths using model.generate_paths()
        - Discount paths to construct zero curve
        - Return structured scenario object
```

**Output Structure:**
```python
class ScenarioCube:
    """Structured output container"""
    - scenarios: np.ndarray [n_scenarios, n_dates, n_factors]
    - dates: np.ndarray [n_dates]
    - spot_date: datetime
    - metadata: Dict (seed, model params, config)
```

---

### 5. **Configuration Layer** (`config/`)
Manages all simulation parameters with schema validation.

**Configuration File (YAML):**
```yaml
simulation:
  spot_date: 2024-01-01
  simulation_horizon_years: 10
  n_simulation_dates: 41  # T+0, T+1Q, ..., T+10Y
  n_paths: 1000
  random_seed: 42

model:
  type: "hull_white_1f"
  parameters:
    alpha: null          # To be calibrated
    sigma: null          # To be calibrated
    calibration_target: "atm_volatility"

calibration:
  instruments:
    - type: "cap"
      strike: 0.025
      tenor: 5
      market_price: 0.015
    - type: "floor"
      strike: 0.015
      tenor: 5
      market_price: 0.008
  
  optimization:
    method: "levenberg_marquardt"
    tolerance: 1e-6
    max_iterations: 1000

data:
  curve_file: "Input_Data/market_data/spot_rates.csv"
  interpolation: "cubic_spline"
```

**Validation (Pydantic):**
```python
class SimulationConfig(BaseModel):
    spot_date: datetime
    simulation_horizon_years: int = Field(gt=0)
    n_simulation_dates: int = Field(gt=1)
    n_paths: int = Field(gt=100)
    random_seed: int
```

---

## Data Flow Diagram

```
Input Data (YAML/CSV)
    ↓
Configuration Layer (schema validation)
    ↓
Market Data Layer (curve construction)
    ↓
Calibration Layer (estimate parameters)
    ↓
Stochastic Model (Hull-White with fitted params)
    ↓
Simulation Engine (Monte Carlo paths)
    ↓
Scenario Cube Output [n_scen × n_dates × n_factors]
```

---

## Design Principles Applied

| Principle | Implementation |
|-----------|-----------------|
| **Modularity** | Each component (models, calibration, simulation) operates independently with clean interfaces |
| **Extensibility** | Abstract base classes (`StochasticModel`) enable adding GBM/CIR without modifying simulation engine |
| **Reproducibility** | Seeded RNG + versioned config → identical results |
| **Testability** | Each component testable in isolation; integration tests validate end-to-end flow |
| **Traceability** | Scenario cube metadata preserves model params, seed, calibration results |

---

## Implementation Sequence (Phase 2 Todos)

### Tier 1: Foundation (Critical Path)
1. **Data structures & I/O**
   - Market data containers (`curve.py`, `market_data.py`)
   - Configuration schema & loader (`config/schema.py`, `config/loaders.py`)

2. **Hull-White model**
   - Base model class (`models/base.py`, `models/hull_white.py`)
   - Theoretical properties

3. **Calibration**
   - Basic calibrator stub (`calibration/hw_calibrator.py`)
   - Optimization loop for α, σ

### Tier 2: Engine
4. **Monte Carlo engine**
   - Path generator (`simulation/path_generator.py`)
   - Scenario cube construction (`simulation/engine.py`)

5. **Integration**
   - End-to-end workflow
   - Config-driven execution

### Tier 3: Quality
6. **Testing**
   - Unit tests for each component
   - Integration tests

---

## Technology Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Numerical** | NumPy, SciPy | Fast vectorized operations |
| **Optimization** | scipy.optimize | Robust parameter estimation |
| **Data** | Pandas, Parquet | Efficient storage/querying of scenarios |
| **Config** | Pydantic, YAML | Type-safe schema validation |
| **Testing** | Pytest | Comprehensive unit + integration testing |
| **Visualization** | Matplotlib, Plotly | Path visualization, diagnostics |

---

## Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Calibration unstable | Use differential_evolution (global optimizer) + bounds on α, σ |
| Monte Carlo convergence slow | Implement Sobol quasi-random sequences as alternative to pseudorandom |
| Numerical precision | Use double precision; validate Euler vs exact discretization |
| Future extensibility pain | Abstract `StochasticModel` class; clear interface contracts |

---

## Success Criteria (Phase 2)

✅ **Deliverables:**
- Market risk factors can be simulated using calibrated Hull-White model
- Scenario cube structure follows specifications
- Configuration-driven end-to-end workflow

✅ **Code Quality:**
- Type hints throughout
- Docstrings for all public methods

✅ **Reproducibility:**
- Identical seed + config → identical output
- All assumptions documented

---

## Assumptions & Future Considerations

**Assumptions:**
- Interest rates follow Hull-White dynamics (realistic for typical rates markets)
- No smile/skew in cap/floor volatilities (flat vol surface assumed)
- Single currency initially (no FX correlations)

**Future Extensions (Not in This Phase):**
- Multi-factor Hull-White (HW2F, HW3F)
- G2++ model
- Stochastic volatility (SABR)
- Multi-currency correlation matrix

