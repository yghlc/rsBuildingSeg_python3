% convert mat file to png, and the building is 1, background is 0
%Lingcao Huang, 22 April 2017

function deeplabMat2Png(matfile)
    [pathstr,name,ext] = fileparts(matfile);
    png_file = strcat(name,'.png');
    save_png =  fullfile(pathstr,png_file);
    
    %load('colormap_building.mat');
    
    data = load(matfile);
    raw_result = data.data;
    raw_result = permute(raw_result, [2 1 3]);
    
    img_row = 650;%size(img, 1);
    img_col = 650;%size(img, 2);
    
    result = raw_result(1:img_row, 1:img_col, :);

    is_argmax = 0;
    if ~is_argmax
      [~, result] = max(result, [], 3);
      result = uint8(result) - 1;
    else
      result = uint8(result);
    end
   
    %imshow(result,[0,1])
    %imwrite(result, colormap, save_png);
    result(find(result==1)) = 255;
    imwrite(result, save_png);
    
end