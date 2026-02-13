function fh3 = compute_fh3(Q, wYear)
 

if nargin < 2 || isempty(Q) || isempty(wYear)
    fh3 = NaN;
    return
end

validateattributes(Q,{'single','double'},{'real','vector'}, ...
    mfilename,'Q',1);

validateattributes(wYear,{'numeric'},{'vector'}, ...
    mfilename,'wYear',2);

Q     = Q(:);
wYear = wYear(:);

if numel(Q) ~= numel(wYear)
    error('Q and wYear must have the same length.')
end
 
medQ = median(Q,'omitnan');

if isnan(medQ) 
    fh3 = NaN;
    return
end

thresh = 3 * medQ;
 

wy = unique(wYear);
wy = wy(~isnan(wy));

if isempty(wy)
    fh3 = NaN;
    return
end

high_days = nan(numel(wy),1);

for i = 1:numel(wy)

    idx = wYear == wy(i);
    qy  = Q(idx);

    high_days(i) = sum(qy > thresh);

end

valid = high_days(~isnan(high_days));

if isempty(valid)
    fh3 = NaN;
else
    fh3 = mean(valid,'omitnan');
end

end
