% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);

% Convert to grayscale if necessary
if size(image, 3) == 3
    image = rgb2gray(image);
end

% Calculate histogram
histogram = imhist(image);

% Calculate normalized histogram
num_pixels = numel(image);
normalized_histogram = histogram / num_pixels;

% Display original image
subplot(2, 1, 1);
imshow(image);
title('Original Image');

% Display histogram
subplot(2, 2, 3);
bar(histogram);
title('Histogram');
xlabel('Pixel Intensity');
ylabel('Frequency');

% Display normalized histogram
subplot(2, 2, 4);
bar(normalized_histogram);
title('Normalized Histogram');
xlabel('Pixel Intensity');
ylabel('Normalized Frequency');
