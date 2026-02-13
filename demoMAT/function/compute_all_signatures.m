function S = compute_all_signatures(Q,P,date)
 

if nargin < 2 || isempty(Q) || isempty(date)
    error('Q and date are required inputs.')
end

Q = Q(:);
date = date(:);

validateattributes(Q, {'single','double'}, {'real','vector'}, mfilename,'Q',1);
validateattributes(date, {'datetime'}, {'vector'}, mfilename,'date',2);

if numel(Q) ~= numel(date)
    error('Q and date must have the same length.')
end

if nargin < 3 || isempty(P)
    P = NaN(size(Q));
else
    P = P(:);
    validateattributes(P, {'single','double'}, {'real','vector'}, mfilename,'P',3);
    if numel(P) ~= numel(Q)
        error('P must have the same length as Q.');
    end
end
 

monthv = uint16(month(date));
dayv   = uint16(day(date));
yearv  = year(date);
wYear=uint16(yearv)+uint16((monthv>=10));
 

%%  

S = struct();
 
S.MA2 = compute_ma2(Q);
 
S.DH5 = compute_dh5(Q, wYear);
 
S.DL18 = compute_dl18(Q, wYear);
 
S.FH3 = compute_fh3(Q, wYear);
 
[S.RA1, S.RA3] = compute_ra1_ra3(Q);
 
try
    S.CR1 = compute_cr1(Q, date, P);
catch
    S.CR1 = NaN;
    warning('CR1 calculation failed, returning NaN.');
end
 
S.TA2 = compute_ta2(Q, monthv, dayv);
end
