% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);
J = imadjust(image,[],[],2);
imshowpair(image,J,"montage")
