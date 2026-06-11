# Biogas Upgrading Technology Selector

## Overview

This repository contains a Python-based decision-support tool for selecting suitable biogas upgrading technologies based on plant scale, feedstock source, and intended end use.

The tool evaluates the following upgrading technologies:

* Membrane Separation
* Pressure Swing Adsorption (PSA)
* Water Scrubbing
* Chemical Absorption (Amine)
* Cryogenic Separation

The selection is based on:

* Plant scale (m³/h of raw biogas)
* Feedstock source
* Required methane purity
* Technology compatibility
* Relative upgrading cost
* Energy consumption
* Methane slip

## Requirements

* Python 3.8 or higher

No external Python packages are required.

## Installation

Download or clone this repository.

## Running the Program

Run:

python biogas_selector.py

Then enter:

1. Plant scale
2. Feedstock source
3. End-use application

The program will provide:

* Recommended technologies
* Relative costs
* Achievable methane purity
* Energy consumption
* Methane slip
* Full technology comparison table

## Example Applications

The tool can be used for:

* Agricultural biogas plants
* Sewage treatment plants
* Landfill gas projects
* Food waste digestion facilities

## Citation

If you use this software in academic work, please cite the associated journal publication.

## Author

Andy

## Disclaimer

This tool is intended for research and educational purposes. Actual technology selection should consider site-specific technical, economic, and regulatory factors.
