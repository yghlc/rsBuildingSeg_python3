#!/usr/bin/env bash

# put this file to ${training_data_root}/deleted
# move the deleted files back to original training data folder

mv *.geojson ../geojson/buildings/.

mv MUL_AOI* ../MUL/.

mv MUL-PanSharpen* ../MUL-PanSharpen/.

mv PAN* ../PAN/.

mv RGB-PanSharpen* ../RGB-PanSharpen/.