function [ra1, ra3] = compute_ra1_ra3(Q)
 
if nargin < 1 || isempty(Q)
    ra1 = NaN;
    ra3 = NaN;
    return
end

validateattributes(Q,{'single','double'},{'real','vector'}, ...
    mfilename,'Q',1);

Q = Q(:);

 
dQ = diff(Q);

pos = dQ(dQ > 0);
neg = dQ(dQ < 0);

if isempty(pos)
    ra1 = NaN;
else
    ra1 = mean(pos,'omitnan');
end

if isempty(neg)
    ra3 = NaN;
else
    ra3 = mean(neg,'omitnan');
end

end
