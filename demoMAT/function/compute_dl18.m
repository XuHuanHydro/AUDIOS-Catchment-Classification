function dl18 = compute_dl18(Q, wYear)
 

if nargin < 2 || isempty(Q) || isempty(wYear)
    dl18 = NaN;
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

 

wy = unique(wYear);
wy = wy(~isnan(wy));

if isempty(wy)
    dl18 = NaN;
    return
end

zero_days = nan(numel(wy),1);

for i = 1:numel(wy)

    idx = wYear == wy(i);
    qy  = Q(idx);

    zero_days(i) = sum(qy == 0);    

end

valid = zero_days(~isnan(zero_days));

if isempty(valid)
    dl18 = NaN;
else
    dl18 = mean(valid,'omitnan');
end

end
