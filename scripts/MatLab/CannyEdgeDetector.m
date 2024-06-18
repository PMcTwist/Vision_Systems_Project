% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);

% Convert to grayscale if necessary
if size(image, 3) == 3
    image_gray = rgb2gray(image);
else
    image_gray = image;
end

% Step 1: Noise Reduction (Gaussian Blur)
blurred = imgaussfilt(image_gray, 1);

% Step 2: Gradient Calculation (Sobel Operator)
gradient_x = imfilter(double(blurred), fspecial('sobel')');
gradient_y = imfilter(double(blurred), fspecial('sobel'));
magnitude = sqrt(gradient_x.^2 + gradient_y.^2);

% Step 3: Non-maximum Suppression
angle = atan2d(gradient_y, gradient_x);
suppressed = magnitude;
[rows, cols] = size(suppressed);
for i = 2:rows-1
    for j = 2:cols-1
        if (angle(i,j) <= 22.5 && angle(i,j) >= -22.5) || (angle(i,j) >= 157.5) || (angle(i,j) <= -157.5)
            if (magnitude(i,j) <= magnitude(i,j-1)) || (magnitude(i,j) <= magnitude(i,j+1))
                suppressed(i,j) = 0;
            end
        elseif (angle(i,j) >= 22.5 && angle(i,j) <= 67.5) || (angle(i,j) <= -112.5 && angle(i,j) >= -157.5)
            if (magnitude(i,j) <= magnitude(i-1,j+1)) || (magnitude(i,j) <= magnitude(i+1,j-1))
                suppressed(i,j) = 0;
            end
        elseif (angle(i,j) > 67.5 && angle(i,j) < 112.5) || (angle(i,j) < -67.5 && angle(i,j) > -112.5)
            if (magnitude(i,j) <= magnitude(i-1,j)) || (magnitude(i,j) <= magnitude(i+1,j))
                suppressed(i,j) = 0;
            end
        elseif (angle(i,j) >= 112.5 && angle(i,j) <= 157.5) || (angle(i,j) <= -22.5 && angle(i,j) >= -67.5)
            if (magnitude(i,j) <= magnitude(i-1,j-1)) || (magnitude(i,j) <= magnitude(i+1,j+1))
                suppressed(i,j) = 0;
            end
        end
    end
end

% Step 4: Double Thresholding
low_threshold = 30;
high_threshold = 100;
strong_edges = suppressed > high_threshold;
weak_edges = (suppressed >= low_threshold) & (suppressed <= high_threshold);

% Step 5: Edge Tracking by Hysteresis
edges = strong_edges;
for i = 2:rows-1
    for j = 2:cols-1
        if weak_edges(i,j)
            if any(edges(i-1:i+1, j-1:j+1))
                edges(i,j) = 1;
            end
        end
    end
end
edges = uint8(edges * 255);

% Display the images
subplot(2, 3, 1);
imshow(image_gray);
title('Original Image');

subplot(2, 3, 2);
imshow(blurred, []);
title('Blurred Image');

subplot(2, 3, 3);
imshow(magnitude, []);
title('Gradient Magnitude');

subplot(2, 3, 4);
imshow(suppressed, []);
title('Non-maximum Suppression');

subplot(2, 3, 5);
imshow(strong_edges);
title('Strong Edges');

subplot(2, 3, 6);
imshow(edges);
title('Final Edges');
