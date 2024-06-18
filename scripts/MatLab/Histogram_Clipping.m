% Select Image
file_path = uigetfile('*.jpg', 'Select an Image File!')

% Load an image
image = imread(file_path);

% Compute histogram
[occurrences, bins] = imhist(image);

% Sort histogram occurrences in descending order
[sorted_occurrences, idx] = sort(occurrences, 'descend');

% Calculate the cumulative sum
cumulative_sum = cumsum(sorted_occurrences);

% Find the threshold index
threshold_index = find(cumulative_sum >= 0.99 * sum(occurrences), 1);

% Select the top 90% most occurred intensities
selected_bins = bins(idx(1:threshold_index));
selected_occurrences = sorted_occurrences(1:threshold_index);

% Create a copy of the original image
modified_image = image;

% Initialize a logical mask
mask = false(size(image));

% Find the indices of pixels whose bins were removed
for i = 1:numel(bins)
    if ~ismember(bins(i), selected_bins)
        mask = mask | (image == bins(i)); % Update the mask
    end
end

% Set the pixel values at removed indices to zero
modified_image(mask) = 0;

% Plot original image and histogram
figure;

% Original Image
subplot(2, 2, 1);
imshow(image);
title('Original Image');

% Original Histogram
subplot(2, 2, 2);
bar(bins, occurrences, 'hist');
title('Original Histogram');
xlabel('Intensity');
ylabel('Occurrences');
xlim([0, 255]);

% Plot modified image and histogram
% Modified Image
subplot(2, 2, 3);
imshow(modified_image);
title('Modified Image');

% Modified Histogram
subplot(2, 2, 4);
bar(selected_bins, selected_occurrences);
title('Modified Histogram (90% most occurred intensities)');
xlabel('Intensity');
ylabel('Occurrences');
xlim([0, 255]);
