% Harris-Stephens Corner Detection Script

% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);

% Convert the image to grayscale if it is not already
if size(image, 3) == 3
    gray_image = rgb2gray(image);
else
    gray_image = image;
end

% Compute the image gradients
[Ix, Iy] = imgradientxy(double(gray_image));

% Compute products of derivatives at every pixel
Ix2 = Ix.^2;
Iy2 = Iy.^2;
Ixy = Ix .* Iy;

% Apply Gaussian smoothing to the derivative products
G = fspecial('gaussian', [7 7], 2);
Sxx = imfilter(Ix2, G);
Syy = imfilter(Iy2, G);
Sxy = imfilter(Ixy, G);

% Set the sensitivity factor and threshold
k = 0.04; % Sensitivity factor
threshold = 1e6; % Threshold for detecting corners

% Compute the Harris response for each pixel
R = (Sxx .* Syy - Sxy.^2) - k * (Sxx + Syy).^2;

% Find corners where R is above the threshold
corners = R > threshold;

% Perform non-maximum suppression
local_max = imregionalmax(R);
harris_corners = corners & local_max;

% Display the results
imshow(image);
hold on;
[rows, cols] = find(harris_corners);
plot(cols, rows, 'r*');
hold off;
