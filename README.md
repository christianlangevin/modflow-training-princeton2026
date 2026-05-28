![alt](images/header.png)

[![CI](https://github.com/christianlangevin/modflow-training-princeton2026/actions/workflows/ci.yml/badge.svg)](https://github.com/christianlangevin/modflow-training-princeton2026/actions/workflows/ci.yml)

# MODFLOW 6 and FloPy: Take Your Modeling Skills to the Next Level
Training materials for the [MODFLOW 6 and FloPy workshop](https://igwmc.princeton.edu/groundwater-modeling-and-more/short-courses-more/#MODFLOW-6-and-FloPy) offered at the [2026 Groundwater Modeling and More Conference](https://igwmc.princeton.edu/groundwater-modeling-and-more/) at Princeton University.  

Presentations from the workshop will be provided as a GitHub Release, and can be accessed [here](https://github.com/langevin-usgs/modflow-training-princeton2026/releases).

## Location and Dates
* Princeton University
* June 5-6, 2026

## Course Description
MODFLOW 6 is the current version of MODFLOW released and supported by the USGS.  The program is under active development by the short course instructors and the broader hydrologic community.  This short course introduces participants to MODFLOW 6 and its growing simulation capabilities.  For each topic included in the short course, there will be a short lecture on the underlying concepts and implementation followed by a live demonstration.  Live demonstrations will use the Python language, Jupyter Notebooks, and the FloPy Package to create, run, and post-process MODFLOW 6 simulations. 

The following topics will be covered during the short course.
*	Getting started with MODFLOW 6 and FloPy
*	Mesh generation with FloPy
*   Coupling models using exchanges
*	Parallel MODFLOW 6 simulations
*	Advanced packages (Multi-Aquifer Well, Streamflow Routing, Lake, Unsaturated Zone Flow, Water Mover, and Compaction and SUBsidence)
*	Particle tracking with MODFLOW 6
*   Solute and heat transport
*	Variable-density flow
*	XT3D multi-point flux approximation for modeling aquifers with full three-dimensional anisotropy
*	MODFLOW Application Programming Interface (API) for coupling models, creating custom MODFLOW packages, and controlling MODFLOW during a simulation
*   NetCDF and FloPy 4

## Intended Audience
This course is suited for groundwater modelers interested in learning about the USGS version of MODFLOW, its newer capabilities, and how to use FloPy to create and run simulations.  For attendees wanting to run live demonstrations, instructions for installing the required software on a laptop computer (Windows, Mac, and Linux operating systems will be supported) are provided [here](./setup.md).  No previous experience with FloPy or Python is required, however, participants without any Python experience may benefit from additional preparation prior to the class.

## Instructors
* Wes Bonelli, University Corporation for Atmospheric Research
* Joe Hughes, INTERA Incorporated
* Chris Langevin, S.S. Papadopulos & Associates, Inc.
* Josh Larsen, US Geological Survey
* Sorab Panday, GSI Environmental Inc.
* Alden Provost, US Geological Survey
* Michael Reno, University Corporation for Atmospheric Research
* Martijn Russcher, Deltares

## Agenda

The following tentative agenda is based on a start time each morning of 8:30 AM and an ending time each day of 5:00 PM.

### Friday, June 5, 2026

|Time      |Topic                            |Lead                        |
|----------|---------------------------------|----------------------------|
| 8:30 AM  |Introductions and Overview       |Langevin                    |
| 9:15 AM  |First FloPy Model                |Hughes                      |
|10:30 AM  |--*BREAK*--                      | --                         |
|11:00 AM  |Mesh generation with FloPy       |Larsen                      |
|12:00 PM  |--*LUNCH*--                      | --                         |
| 1:15 PM  |Multi-Model Coupling             |Langevin/Russcher           |
| 1:45 PM  |Parallel MODFLOW                 |Russcher/Hughes/Larsen      |
| 2:45 AM  |--*BREAK*--                      | --                         |
| 3:00 PM  |Advanced Flow Packages           |Hughes                      |
| 4:00 PM  |Particle Tracking in MODFLOW 6   |Bonelli/Provost                      |
| 5:00 PM  |ADJOURN                          |                            |

### Saturday, June 6, 2026

|Time      |Topic                            |Lead                        |
|----------|---------------------------------|----------------------------|
| 8:30 AM  |Solute and Heat Transport        | Langevin/Panday            |
| 9:30 AM  |Variable Density Flow            | Langevin/Panday            |
|10:30 AM  |--*BREAK*--                      | --                         |
|10:45 AM  |XT3D                             | Provost                    |
|11:30 AM  |MODFLOW API                      | Hughes/Russcher/Larsen     |
|12:15 PM  |--*LUNCH*--                      | --                         |
| 1:30 PM  |MODFLOW API (cont)               | Hughes/Russcher/Larsen     |
| 3:00 AM  |--*BREAK*--                      | --                         |
| 3:30 PM  |NetCDF and FloPy 4               | Bonelli/Reno/Larsen        |
| 4:30 PM  |Future Directions and Wrapup     | All                        |
| 5:00 PM  |ADJOURN                          |                            |


## Software Installation and Course Materials

This workshop consists of jupyter notebooks that use FloPy to create, run, and post-process MODFLOW models.  In order for workshop attendees to follow along and run the notebooks, software must be installed prior to the workshop.  Instructions for setting up the class environment is provided in [setup.md](./setup.md).


## Groundwater Modeling and More 2026

This workshop is part of the [Groundwater Modeling and More Conference](https://igwmc.princeton.edu/groundwater-modeling-and-more/).

![alt](images/Final-logo-2026.png)
