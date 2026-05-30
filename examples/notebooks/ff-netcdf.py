# # Frenchman Flat — MODFLOW 6 NetCDF Input and Output
#
# MODFLOW 6 can read model arrays from a NetCDF file instead of the
# traditional ASCII package files, and can write simulation results directly
# to NetCDF.  This notebook demonstrates both NetCDF formats supported by
# MODFLOW 6 and flopy4, using the Frenchman Flat regional groundwater model.

# ### Imports

import shutil
from pathlib import Path

import numpy as np
import xarray as xr

import flopy4
from flopy4.mf6.constants import FILL_DNODATA
from flopy4.mf6.enums import NetCDFFormat
from flopy4.mf6.utl.ncf import Ncf

# ### Configuration
#
# Change ``NPER``, ``NSTP``, and ``TSMULT`` to adjust the simulation length.
# ``NPER`` selects how many of the 33 available stress periods to simulate.

NPER = 3
NSTP = 15
TSMULT = 1.1

# ### Stress period schedule
#
# Full 33-period pumping history for the Frenchman Flat site; period lengths
# are in days.  Only the first ``NPER`` entries are used.

_PERLEN_ALL = [
    001.17707,
    000.84374,
    004.61527,
    000.41874,
    000.77499,
    077.29513,
    166.49999,
    364.99999,
    364.99999,
    365.99999,
    364.99999,
    364.99999,
    364.99999,
    365.99999,
    364.99999,
    364.99999,
    364.99999,
    365.99999,
    364.99999,
    364.99999,
    364.99999,
    139.40624,
    001.05207,
    297.99027,
    001.02221,
    320.06666,
    000.96735,
    356.89999,
    001.05346,
    376.02568,
    000.95485,
    331.56110,
    364.99999,
]

# ### Well pump rates
#
# Three distinct ``Welg`` packages.
# Rates are stored as sparse ``{period: {cellid: value}}`` dicts and converted
# to full ``(nper, nlay, nrow, ncol)`` arrays in the setup section below.

# Constant-rate pumping test
_Q_CRT_ALL = {
    0: {(1, 43, 43): -30992.50},
    1: {(1, 43, 43): 0.0},
    2: {(1, 43, 43): -30992.50},
    3: {(1, 43, 43): 0.0},
    4: {(1, 43, 43): -30992.50},
    5: {(1, 43, 43): 0.0},
}

# Subsurface leakage
_Q_LEAK_ALL = {
    0:  {(1, 43, 43): 1.0e-05},
    7:  {(1, 43, 43): 1.5e+03},
    8:  {(1, 43, 43): 2.65e+03},
    9:  {(1, 43, 43): 3.15e+03},
    10: {(1, 43, 43): 4.1e+03},
    11: {(1, 43, 43): 4.65e+03},
    12: {(1, 43, 43): 4.95e+03},
    13: {(1, 43, 43): 5.3e+03},
    14: {(1, 43, 43): 5.8e+03},
    16: {(1, 43, 43): 5.9e+03},
    17: {(1, 43, 43): 5.8e+03},
    19: {(1, 43, 43): 5.6e+03},
    20: {(1, 43, 43): 4.7e+03},
    22: {(1, 43, 43): 3.4e+03},
    23: {(1, 43, 43): 1.0e-05},
}

# Water-sampling extraction
_Q_SAMPLEQ_ALL = {
    0:  {(1, 43, 43): 0.0},
    22: {(1, 43, 43): -4981.90},
    23: {(1, 43, 43): 0.0},
    24: {(1, 43, 43): -4059.83},
    25: {(1, 43, 43): 0.0},
    26: {(1, 43, 43): -5678.75},
    27: {(1, 43, 43): 0.0},
    28: {(1, 43, 43): -5755.75},
    29: {(1, 43, 43): 0.0},
    30: {(1, 43, 43): -4117.58},
    31: {(1, 43, 43): 0.0},
}

# ### Derive time and well data from NPER

perlen = _PERLEN_ALL[:NPER]
nstp = [NSTP] * NPER
tsmult = [TSMULT] * NPER

time = flopy4.mf6.utils.time.Time(perlen=perlen, nstp=nstp, tsmult=tsmult)
nper = time.nper

q_crt     = {p: cells for p, cells in _Q_CRT_ALL.items()     if p < NPER}
q_leak    = {p: cells for p, cells in _Q_LEAK_ALL.items()    if p < NPER}
q_sampleq = {p: cells for p, cells in _Q_SAMPLEQ_ALL.items() if p < NPER}

print(
    f"NPER={nper}  NSTP={NSTP}  TSMULT={TSMULT}\n"
    f"  CRT active periods:     {sorted(q_crt)}\n"
    f"  Leak active periods:    {sorted(q_leak)}\n"
    f"  SampleQ active periods: {sorted(q_sampleq)}"
)

# ## Model Setup

# Grid and arrays
try:
    FF_ROOT = Path(__file__).parent
except NameError:
    FF_ROOT = Path.cwd()

DATA_ROOT = FF_ROOT.parent / "data" / "frenchman-flat" / "arrays"

workspace_mesh   = FF_ROOT / "ff-netcdf" / "netcdf_mesh"
workspace_struct = FF_ROOT / "ff-netcdf" / "netcdf_struct"

nlay, nrow, ncol = 10, 87, 87
shape = (nlay, nrow, ncol)

delr = np.array([
    2500.0, 2500.0, 2500.0, 2150.0, 1800.0, 1500.0, 1250.0, 1000.0,
    750.0,  750.0,  500.0,  500.0,  500.0,  500.0,  500.0,  350.0,  250.0,
    200.0,  150.0,  125.0,  100.0,  100.0,  100.0,  100.0,  100.0,   75.0,
     50.0,   50.0,   50.0,   50.0,   50.0,   30.0,   30.0,   15.0,   15.0,  13.5,
     10.0,    6.5,    5.0,    3.5,    2.5,    2.0,    1.5,    1.0,    1.5,   2.0,
      2.5,    3.5,    5.0,    6.5,   10.0,   13.5,   15.0,   15.0,   30.0,  30.0,
     50.0,   50.0,   50.0,   50.0,   50.0,   75.0,  100.0,  100.0,  100.0, 100.0,
    100.0,  125.0,  150.0,  200.0,  250.0,  350.0,  500.0,  500.0,  500.0, 500.0,
    500.0,  750.0,  750.0, 1000.0, 1250.0, 1500.0, 1800.0, 2150.0, 2500.0,
    2500.0, 2500.0,
])
delc = delr.copy()

_BOTM_ELEVATIONS = [-200.0, -400.0, -600.0, -800.0, -1050.0,
                    -1350.0, -1700.0, -2200.0, -2950.0, -3950.0]

k  = np.zeros(shape, dtype=float)
k33 = np.zeros(shape, dtype=float)
ss  = np.zeros(shape, dtype=float)
for l in range(nlay):
    pad = "000" if l < 9 else "00"
    k[l]   = np.loadtxt(DATA_ROOT / f"Array.MF-HydK_{pad}{l + 1}.txt")
    k33[l] = k[l] * 0.1
    ss[l]  = np.loadtxt(DATA_ROOT / f"Array.MF-HydS_{pad}{l + 1}.txt")

grid = flopy4.mf6.utils.grid.StructuredGrid(
    lenuni="meters",
    xoff=573309.700,
    yoff=4102552.000 - delr.sum(),
    nlay=nlay, nrow=nrow, ncol=ncol,
    top=np.zeros((nrow, ncol), dtype=float),
    botm=np.stack([np.full((nrow, ncol), v) for v in _BOTM_ELEVATIONS]),
    delr=delr, delc=delc,
    idomain=np.ones(shape, dtype=int),
    crs="EPSG:26911",
)

dims = {"nper": nper, "ncpl": nrow * ncol, **dict(grid.dataset.sizes)}

# Packages
dis = flopy4.mf6.gwf.Dis.from_grid(grid=grid)
ic  = flopy4.mf6.gwf.Ic(strt=0.0, dims=dims)
npf = flopy4.mf6.gwf.Npf(
    icelltype=np.zeros(shape, dtype=int), k=k, k33=k33, save_flows=True, dims=dims,
)
sto = flopy4.mf6.gwf.Sto(ss=ss, iconvert=0, dims=dims)
oc  = flopy4.mf6.gwf.Oc(
    budget_file=Path("ff-netcdf.cbc"),
    head_file=Path("ff-netcdf.hds"),
    save_head={0: "all"},
    save_budget={0: "last"},
    dims=dims,
)


def _q_to_array(q_dict: dict) -> np.ndarray:
    """Build a (nper, nlay, nrow, ncol) well-rate array from a sparse q-dict.

    Periods absent from ``q_dict`` are filled with ``FILL_DNODATA`` so MODFLOW
    treats those cells as inactive for those periods.
    """
    arr = np.full((nper, *shape), FILL_DNODATA, dtype=float)
    for p, cells in q_dict.items():
        for (la, ro, co), val in cells.items():
            arr[p, la, ro, co] = val
    return arr


welg_crt     = flopy4.mf6.gwf.Welg(
    filename="ff-netcdf.crt.welg",
    q=_q_to_array(q_crt),
    print_input=True, print_flows=True, save_flows=True, dims=dims,
)
welg_leak    = flopy4.mf6.gwf.Welg(
    filename="ff-netcdf.leak.welg",
    q=_q_to_array(q_leak),
    print_input=True, print_flows=True, save_flows=True, dims=dims,
)
welg_sampleq = flopy4.mf6.gwf.Welg(
    filename="ff-netcdf.sampleQ.welg",
    q=_q_to_array(q_sampleq),
    print_input=True, print_flows=True, save_flows=True, dims=dims,
)

gwf = flopy4.mf6.gwf.Gwf(
    dis=dis, ic=ic, npf=npf, sto=sto, oc=oc,
    wel=[welg_crt, welg_leak, welg_sampleq],
    dims=dims,
)

# Solver and simulation
ims = flopy4.mf6.Ims(
    print_option="summary",
    complexity="moderate",
    outer_dvclose=0.01,
    outer_maximum=50,
    under_relaxation="DBD",
    under_relaxation_theta=0.9,
    under_relaxation_kappa=0.0001,
    under_relaxation_gamma=0.0,
    under_relaxation_momentum=0.0,
    inner_dvclose=0.00001,
    rclose=flopy4.mf6.Ims.Rclose(inner_rclose=0.1),
    inner_maximum=100,
    linear_acceleration="bicgstab",
    number_orthogonalizations=0,
    reordering_method=None,
    models=["ff-netcdf"],
)

tdis = flopy4.mf6.simulation.Tdis.from_time(time)

sim = flopy4.mf6.simulation.Simulation(
    name="ff-netcdf",
    tdis=tdis,
    models={"ff-netcdf": gwf},
    solutions={"ims": ims},
    workspace=workspace_mesh,
)

# ## Layered-Mesh NetCDF (UGRID)
#
# MODFLOW reads array inputs from a UGRID-compliant NetCDF file.  Head results
# are written to an output mesh NetCDF file.
#
# QGIS: Layer > Add Layer > Add Mesh Layer
# ArcGIS Pro does not support the UGRID format.

# ### Configure NetCDF file paths
#
# Input and output NetCDF files are configured:
#
# - ``netcdf_input_file`` — path to the NC file flopy4 writes.
# - ``netcdf_mesh2d_file`` — path to the NC file MODFLOW writes.

workspace_mesh.mkdir(parents=True, exist_ok=True)

gwf.netcdf_input_file = workspace_mesh / "ff-netcdf.input.nc"
gwf.netcdf_mesh2d_file = Path("ff-netcdf.nc")  # relative; MODFLOW writes here
gwf.netcdf_structured_file = None

# ### Build and attach the NCF subpackage

dis.ncf = Ncf.from_grid(grid, NetCDFFormat.LAYERED_MESH)
dis.ncf.filename = workspace_mesh / "ff-netcdf.dis.ncf"

print(f"NCF wkt (first 80 chars): {dis.ncf.wkt[:80]}...")

# ### Build and write the NetCDF input model

nc_model = flopy4.mf6.netcdf.NetCDFModel.from_model(
    gwf,
    netcdf_format=NetCDFFormat.LAYERED_MESH,
    grid=grid,
    time=time,
)
nc_model.to_netcdf(gwf.netcdf_input_file)

# ### Inspect the input NetCDF
#
# Before running, look at what flopy4 wrote.

ds_in = xr.open_dataset(gwf.netcdf_input_file, decode_times=False)
print("Global attributes:")
for attr, val in ds_in.attrs.items():
    s = str(val)
    print(f"  {attr}: {s[:90]}{'…' if len(s) > 90 else ''}")
print(f"\nDimensions: {dict(ds_in.sizes)}")
print(f"\nVariables:  {list(ds_in.data_vars)}")
ds_in.close()

# ### Write the MODFLOW input files
#
# NetCDF supported writes are managed via a context object.

with flopy4.mf6.write_context.WriteContext(use_netcdf=True):
    sim.write()

# ### Inspect the written MODFLOW input
#
# Show NetCDF integration into the MODFLOW text input.

# Model name file — the two NetCDF declarations:
print("ff-netcdf.nam (NetCDF-relevant lines):")
for line in (workspace_mesh / "ff-netcdf.nam").read_text().splitlines():
    if line.strip().upper().startswith("NETCDF"):
        print(f"  {line.strip()}")

# NCF subpackage file — the full file (WKT truncated for readability):
print("\nff-netcdf.dis.ncf:")
for line in dis.ncf.filename.read_text().splitlines():
    print(f"  {line[:95]}{'…' if len(line) > 95 else ''}")

# IC package — shows array data replaced by the NETCDF keyword:
ic_path = next(workspace_mesh.glob("*.ic"))
print(f"\n{ic_path.name}:")
print(ic_path.read_text())

# ### Run the simulation

sim.run(verbose=True)

# ### Load and inspect results
#
# Head comes back as a UGRID ``UgridDataArray``; the GRB provides mesh
# connectivity.  Budget terms are keyed by name in a ``UgridDataset``.

head_mesh = flopy4.mf6.utils.open_hds(
    workspace_mesh / "ff-netcdf.nc",
    workspace_mesh / "ff-netcdf.dis.grb",
)
cbc_mesh = flopy4.mf6.utils.open_cbc(
    workspace_mesh / "ff-netcdf.cbc",
    workspace_mesh / "ff-netcdf.dis.grb",
)

print(f"Head dimensions : {dict(head_mesh.sizes)}")
print(f"Budget variables: {list(cbc_mesh.data_vars)}")

# ## CF-Structured NetCDF
#
# QGIS: Layer > Add Layer > Add Raster Layer
# ArcGIS Pro: Geoprocessing > Make Multidimensional Raster Layer

# ### Configure NetCDF file paths for CF-structured output
#
# - ``netcdf_input_file`` — path to the NC file flopy4 writes.
# - ``netcdf_structured_file`` — path to the NC file MODFLOW writes.

workspace_struct.mkdir(parents=True, exist_ok=True)
sim.workspace = workspace_struct

gwf.netcdf_input_file = workspace_struct / "ff-netcdf.input.nc"
gwf.netcdf_mesh2d_file = None
gwf.netcdf_structured_file = Path("ff-netcdf.nc")

# ### Build and attach the NCF subpackage
#
# For CF-structured output the NCF carries a WKT CRS string, consistent
# with the LAYERED_MESH format.

dis.ncf = Ncf.from_grid(grid, NetCDFFormat.STRUCTURED)
dis.ncf.filename = workspace_struct / "ff-netcdf.dis.ncf"

print(f"NCF wkt (first 80 chars): {dis.ncf.wkt[:80]}...")

# ### Build and write the NetCDF input model
#
# No ``netcdf_format`` argument — defaults to ``NetCDFFormat.STRUCTURED``.

nc_model = flopy4.mf6.netcdf.NetCDFModel.from_model(gwf, grid=grid, time=time)
nc_model.to_netcdf(gwf.netcdf_input_file)

# ### Inspect the input NetCDF

ds_in = xr.open_dataset(gwf.netcdf_input_file, decode_times=False)
print("Global attributes:")
for attr, val in ds_in.attrs.items():
    s = str(val)
    print(f"  {attr}: {s[:90]}{'…' if len(s) > 90 else ''}")
print(f"\nDimensions: {dict(ds_in.sizes)}")
print(f"\nVariables:  {list(ds_in.data_vars)}")
ds_in.close()

# ### Write the MODFLOW input files

with flopy4.mf6.write_context.WriteContext(use_netcdf=True):
    sim.write()

print("\nff-netcdf.nam (NetCDF-relevant lines):")
for line in (workspace_struct / "ff-netcdf.nam").read_text().splitlines():
    if line.strip().upper().startswith("NETCDF"):
        print(f"  {line.strip()}")

# ### Run the simulation

sim.run(verbose=True)

# ### Load and inspect results
#
# Head comes back as a plain ``xr.DataArray`` with ``(time, layer, row, col)``
# dimensions; the GRB provides the structured grid geometry.  Budget terms are
# keyed by name in an ``xr.Dataset``.

head_struct = flopy4.mf6.utils.open_hds(
    workspace_struct / "ff-netcdf.nc",
    workspace_struct / "ff-netcdf.dis.grb",
)
cbc_struct = flopy4.mf6.utils.open_cbc(
    workspace_struct / "ff-netcdf.cbc",
    workspace_struct / "ff-netcdf.dis.grb",
)

print(f"Head dimensions : {dict(head_struct.sizes)}")
print(f"Budget variables: {list(cbc_struct.data_vars)}")

# ## Comparing the Two Formats
#
# The two runs should produce identical head values:

head_mesh_last   = head_mesh.isel(time=-1, layer=0)
head_struct_last = head_struct.isel(time=-1, layer=0)

print(
    f"Layer 1 head at final time step — "
    f"mesh:       min={float(head_mesh_last.min()):.3f}  "
    f"max={float(head_mesh_last.max()):.3f}"
)
print(
    f"Layer 1 head at final time step — "
    f"structured: min={float(head_struct_last.min()):.3f}  "
    f"max={float(head_struct_last.max()):.3f}"
)


