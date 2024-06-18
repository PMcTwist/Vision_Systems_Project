% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
input_image = imread(file_path);

% Convert input image to grayscale if it's RGB
if size(input_image, 3) == 3
    input_image = rgb2gray(input_image);
end

% Set the window size for local histogram equalization
window_size = 15;

% Initialize enhanced image
enhanced_image = zeros(size(input_image));

% Loop through each pixel of the input image
for i = 1:size(input_image, 1)
    for j = 1:size(input_image, 2)
        % Define the boundaries of the local window
        row_start = max(1, i - window_size);
        row_end = min(size(input_image, 1), i + window_size);
        col_start = max(1, j - window_size);
        col_end = min(size(input_image, 2), j + window_size);
        % Extract the local window
        window = input_image(row_start:row_end, col_start:col_end);

        % Perform histogram equalization on the local window
        enhanced_window = histeq(window, 256);

        % Assign the center pixel of the enhanced window to the output image
        enhanced_image(i, j) = enhanced_window(window_size+1, window_size+1);
    end
end

% Display the original and enhanced images
figure;
subplot(1,2,1);
imshow(input_image);
title('Original Image');
subplot(1,2,2);
imshow(enhanced_image, []);
title('Enhanced Image');
