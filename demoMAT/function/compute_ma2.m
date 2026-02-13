function ma2 = compute_ma2(Q)

 
if nargin < 1 || isempty(Q)
    ma2 = NaN;
    return
end

validateattributes(Q,{'single','double'},{'real','vector'}, ...
    mfilename,'Q',1);

Q = Q(:);   % force column vector
 

if all(isnan(Q))
    ma2 = NaN;
else
    ma2 = median(Q,'omitnan');
end

end