#!/bin/bash

# put this file to ${training_data_root}
# deleted folder need to be created first

id=$(cat rasterToWrite.txt | tail -c 17 | tr -dc '0-9')
echo $id

#id=4047

cd geojson/buildings
mv *g${id}.* ../../deleted/.

cd ../..
cd MUL
mv *g${id}.* ../deleted/.

cd ..
cd MUL-PanSharpen
mv *g${id}.* ../deleted/.

cd ..
cd PAN
mv *g${id}.* ../deleted/.

cd ../RGB-PanSharpen
mv *g${id}.* ../deleted/.

