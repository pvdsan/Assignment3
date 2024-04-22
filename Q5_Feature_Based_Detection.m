% Define directory path and ROI path
framesDir = 'Random_Selected_Frames\\'; % Update this path
roiPath = 'roi.jpg';

% Load the ROI image and convert to grayscale
roiImage = imread(roiPath);
roiImageGray = rgb2gray(roiImage);

% Initialize SURF feature detector
detector = detectSURFFeatures(roiImageGray);
[roiFeatures, roiValidPoints] = extractFeatures(roiImageGray, detector);

% Get a list of files in the directory
files = dir(fullfile(framesDir, '*.jpg'));
numFiles = min(length(files), 10); % Process only the first 10 images

% Create a new figure for displaying matches
figure;
set(gcf, 'Position', [100, 100, 1200, 600]); % Adjust figure size as needed

% Loop through each image file
for i = 1:numFiles
    % Read image
    frame = imread(fullfile(framesDir, files(i).name));
    frameGray = rgb2gray(frame);
    
    % Detect and extract features from frame
    framePoints = detectSURFFeatures(frameGray);
    [frameFeatures, validFramePoints] = extractFeatures(frameGray, framePoints);
    
    % Match features between ROI and frame
    indexPairs = matchFeatures(roiFeatures, frameFeatures, 'MatchThreshold', 10.0, 'MaxRatio', 0.7);
    matchedRoiPoints = roiValidPoints(indexPairs(:, 1));
    matchedFramePoints = validFramePoints(indexPairs(:, 2));
    
    % Display the matched points
    subplot(2, 5, i);
    showMatchedFeatures(roiImageGray, frameGray, matchedRoiPoints, matchedFramePoints, 'montage');
    title(['Matches with Frame ', num2str(i)]);
    
    % Calculate the bounding box around matched points in the frame
    if ~isempty(matchedFramePoints)
        locations = matchedFramePoints.Location;  % Get locations of matched points in the frame
        minX = min(locations(:,1));
        maxX = max(locations(:,1));
        minY = min(locations(:,2));
        maxY = max(locations(:,2));
        width = maxX - minX;
        height = maxY - minY;
        
        % Draw the bounding box on the right half of the montage (where the frame is displayed)
        hold on;
        rectangle('Position', [minX + size(roiImageGray, 2), minY, width, height], 'EdgeColor', 'y', 'LineWidth', 2);
    end
end

% Adjust subplot spacing
sgtitle('SURF Feature Matching Results with Bounding Boxes');
tight_layout();
