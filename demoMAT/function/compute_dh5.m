function dh5 = compute_dh5(Q, wYear)
 

 
if nargin < 2 || isempty(Q) || isempty(wYear)
    dh5 = NaN;
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
    dh5 = NaN;
    return
end

annual_max90 = nan(numel(wy),1);

for i = 1:numel(wy)

    idx = wYear == wy(i);
    qy  = Q(idx);

    if numel(qy) < 90
        continue
    end

    ma90 = movmean(qy,90,'Endpoints','discard');

    annual_max90(i) = max(ma90,[],'omitnan');

end

valid = annual_max90(~isnan(annual_max90));

if isempty(valid)
    dh5 = NaN;
else
    dh5 = mean(valid,'omitnan');
end

end
