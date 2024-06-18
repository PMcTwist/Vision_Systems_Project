% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);
subplot(2,2,1)
imshow(image)

% Split the image into its RGB components
redChannel = image(:,:,1);
greenChannel = image(:,:,2);
blueChannel = image(:,:,3);

% Save each component as a separate image
subplot(2,2,2)
imwrite(redChannel, 'red_component.jpg');
imshow(redChannel)
title('Red Component')
subplot(2,2,3)
imwrite(greenChannel, 'green_component.jpg');
imshow(greenChannel)
title('Green Component')
subplot(2,2,4)
imwrite(blueChannel, 'blue_component.jpg');
imshow(blueChannel)
title('Blue Component')
