# Paired mapping calibration

`assets/material-library/wilton-flatweave-01/paired-mappings.json` is the source of truth for the three verified mapping sets. Each set contains a design, matching product overview, and matching macro detail. The design in sample 01 was originally misnamed as an AI physical image; it is a design source.

Use the pairs to calibrate only the shared Wilton-flatweave visual system: product-directional bundle rows, fine interlacing visibility, low relief, wrapped binding, camera family, and scale. The current design source remains the only authority for current motifs and colours.

Before changing the visual parameters, run `python scripts/validate_paired_mappings.py`. For a material change, inspect two pairs while calibrating and reserve the third for a leave-one-out review. A leave-one-out review is visual evidence, not a model-training claim.
