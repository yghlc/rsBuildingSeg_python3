%% convert all mat file to png, and the building is 1, background is 0
%Lingcao Huang, 22 April 2017

output_dir='/media/hlc/DATA/Data_lingcao/aws_SpaceNet/deeplab_exper/spacenet_rgb_aoi_2/features/deeplab_largeFOV/val/fc8';
output_dir = dir(fullfile(output_mat_folder, '*.mat'));

for i = 1 : numel(output_dir)
    if mod(i, 100) == 0
        fprintf(1, 'processing %d (%d)...\n', i, numel(output_dir));
    end
    
    matfile = fullfile(output_mat_folder, output_dir(i).name);

    deeplabMat2Png(matfile);
 
end