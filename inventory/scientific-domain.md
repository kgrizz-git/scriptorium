# Scientific & Domain Libraries

Last reviewed: 2026-08-23

Domain-specific Python libraries for EM/FDTD simulation, scientific computing, and related
fields. See `inventory/catalog-skills-agents.md` for agent skills that wrap these
(simulation-software-setup-run, etc.).

---

## EM & FDTD simulation

### meep (MIT)
https://github.com/NanoComp/meep

Full-featured FDTD electromagnetic simulator. CPU and GPU (CUDA) support; Python API;
handles dispersive materials, nonlinear media, S-parameters, eigenmode sources. The
primary open-source FDTD tool for photonics and antenna simulation.

```bash
pip install meep   # or conda install -c conda-forge meep
```

### openEMS
https://openems.de

Free, open-source FDTD simulator with MATLAB/Octave and Python interfaces. Strong
community; used in antenna and RF component design. Includes CSXCAD for geometry.

### fdtd (flaport)
https://github.com/flaport/fdtd

Pure-Python photonics FDTD library (PyTorch backend for GPU acceleration). Simpler
than meep; good for learning, 2D/3D photonic device prototyping, and differentiable
FDTD (gradient-based optimization). Minimal dependencies.

### gprMax
https://www.gprmax.com

3D FDTD for ground-penetrating radar (GPR) simulation. GPU-accelerated (CUDA). Use
for subsurface sensing, GPR signal modeling, and non-destructive testing simulation.

### scikit-rf
https://scikit-rf.org

RF/microwave engineering: S-parameters, network analysis, calibration, de-embedding,
TDR, and plotting. Pure Python; interoperates with touchstone files. Essential for
microwave circuit workflows that don't need full FDTD.

---

## General scientific computing

The baseline scientific Python stack — brief mentions only; assume these are available.

| Library | Purpose |
|---|---|
| numpy | ND arrays, linear algebra |
| scipy | Integration, optimization, signal processing, stats |
| sympy | Symbolic mathematics (see also `sympy` skill) |
| xarray | Labeled ND arrays, netCDF/HDF5 I/O, coordinates |
| polars | Fast DataFrames (Rust-backed; faster than pandas for large data) |
| pandas | DataFrames (familiar; slower than polars for bulk operations) |
| matplotlib / seaborn / plotly | Visualization |
| statsmodels | Econometrics, time series, statistical tests |
| pingouin | Statistical tests with effect sizes and power analysis |

## Equation discovery and interpretable dynamics

### KANDy
https://github.com/KindXiaoming/kandy

Combines Kolmogorov-Arnold Networks with Koopman-style lifts for discovering
interpretable ODEs, maps, and PDEs from data. Consider alongside SINDy-style approaches
when the project needs governing-equation discovery rather than black-box forecasting.

---

## Agent skills that wrap these libraries

From `inventory/catalog-skills-agents.md`:
- `simulation-software-setup-run` — FDTD, FEM, Monte Carlo solver setup
- `simulation-validation-and-interpretation` — V&V, UQ, results interpretation
- `math-physics-deriver` agent — symbolic derivation with meep/openEMS integration
- `exploratory-data-analysis` — data profiling and scientific-format handling
- `optimize-for-gpu` — GPU acceleration for numpy/scipy/FDTD workflows
