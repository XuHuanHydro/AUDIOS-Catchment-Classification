function ta2 = compute_ta2(Q, month, day)

if nargin < 3 || isempty(Q) || isempty(month) || isempty(day)
    ta2 = NaN;
    return
end

validateattributes(Q,{'single','double'},{'real','vector'}, ...
    mfilename,'Q',1);

validateattributes(month,{'numeric'},{'vector','integer'}, ...
    mfilename,'month',2);

validateattributes(day,{'numeric'},{'vector','integer'}, ...
    mfilename,'day',3);

Q     = Q(:);
month = month(:);
day   = day(:);

n = numel(Q);

if n ~= numel(month) || n ~= numel(day)
    error('Q, month, and day must have the same length.')
end



meanQ = mean(Q,'omitnan');

if isnan(meanQ) || meanQ <= 0
    ta2 = NaN;
    return
end

%%

epsv = eps;

if meanQ < 1
    bounds = (([0.10;0.25;0.50;0.75;1.00; ...
        1.25;1.50;1.75;2.00;2.25] - 1) ...
        * -0.9 + 1) .* log10(meanQ + epsv);
else
    bounds = [0.10;0.25;0.50;0.75;1.00; ...
        1.25;1.50;1.75;2.00;2.25] .* log10(meanQ);
end

logQ  = log10(Q + epsv);

levels = sort(bounds(:));
edges  = [-Inf; levels; Inf];

binIdx = discretize(logQ,edges);

%%

dateStr = num2str([month,day],'%02d_%02d');

[Mat,~,~,dateLabels] = crosstab(binIdx,dateStr);

% remove Feb-29 if present
feb29 = strcmp(dateLabels,'02_29');

if any(feb29)
    Mat(:,feb29) = [];
end

if isempty(Mat) || all(Mat(:) == 0)
    ta2 = NaN;
    return
end

%%
X = sum(Mat,1);
Y = sum(Mat,2);
Z = sum(X);

if Z == 0
    ta2 = NaN;
    return
end

pX  = X(X>0) ./ Z;
HX  = -sum(pX .* log10(pX));

pY  = Y(Y>0) ./ Z;
HY  = -sum(pY .* log10(pY));

pXY = Mat(Mat>0) ./ Z;
HXY = -sum(pXY .* log10(pXY));

Hmax = log10(11);

ta2 = 1 - (HXY - HX) ./ Hmax;

% numeric safety
ta2 = max(0,min(1,ta2));

end
