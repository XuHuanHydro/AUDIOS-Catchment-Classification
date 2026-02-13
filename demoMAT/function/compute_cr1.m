function EventRR = compute_cr1(Q, t, P, varargin)

if nargin < 3
    error('Not enough input arguments.')
end

ip = inputParser;

addRequired(ip,'Q',@(x)isnumeric(x)&&isvector(x))
addRequired(ip,'t',@(x)(isnumeric(x)||isdatetime(x))&&isvector(x))
addRequired(ip,'P',@(x)isnumeric(x)&&isvector(x))

addParameter(ip,'min_termination',8)
addParameter(ip,'min_duration',5)
addParameter(ip,'min_intensity_day',10)
addParameter(ip,'min_intensity_day_during',1)
addParameter(ip,'max_recessiondays',1)

parse(ip,Q,t,P,varargin{:})

opt = ip.Results;

Q = Q(:); P = P(:);

%% ---- timestep ----
if isnumeric(t)
    t = datetime(t,'ConvertFrom','datenum');
end

t = t(:);

timestep = hours(median(diff(t)));
 
%% EVENT SEPARATION  
 

P_day = P;

P_low = P_day <= opt.min_intensity_day_during;
P_low(1)=0;

chg = diff(P_low);
bg  = find(chg==1)+1;
eg  = find(chg==-1);

bg = bg(1:min(length(bg),length(eg)));

gaplen = eg-bg+1;

for k = find(gaplen < opt.min_termination/timestep)'
    P_low(bg(k):eg(k)) = 0;
end

potential = P_low==0;
chg = diff(potential);

bs = find(chg==1)+1;
es = find(chg==-1); 
if ~isempty(bs) && ~isempty(es)
    if es(1) < bs(1)
        es(1) = [];
    end
end

n = min(length(bs),length(es));
bs = bs(1:n);
es = es(1:n);

bs = bs(1:length(es));

valid = false(size(bs));

for i = 1:length(bs)

    durOK = es(i)-bs(i)+1 >= opt.min_duration/timestep;

    intOK = max(P_day(bs(i):es(i))) >= ...
            opt.min_intensity_day/(24/timestep);

    valid(i) = durOK && intOK;

end

stormarray = [bs(valid) es(valid)];

if isempty(stormarray)
    EventRR = NaN;
    return
end

%% ---- recession ----

stormarray(1:end-1,3) = ...
 min(stormarray(1:end-1,2)+opt.max_recessiondays*24/timestep,...
     stormarray(2:end,2)-1);

stormarray(end,3) = ...
 min(stormarray(end,2)+opt.max_recessiondays*24/timestep,length(P));

P_high = P_day > opt.min_intensity_day_during;

rec = zeros(size(stormarray,1),1);

for i=1:size(stormarray,1)

    idx = find(P_high((stormarray(i,2)+1):stormarray(i,3)),1);

    if ~isempty(idx)
        rec(i)=idx-1;
    else
        rec(i)=inf;
    end

end

stormarray(:,3) = min(stormarray(:,3),stormarray(:,2)+rec);
 
%% CR1
 

rr = nan(size(stormarray,1),1);

for i=1:size(stormarray,1)

    Psum = sum(P(stormarray(i,1):stormarray(i,3)));
    Qsum = sum(Q(stormarray(i,1):stormarray(i,3)));

    if Psum>0
        rr(i)=Qsum/Psum;
    end

end

EventRR = mean(rr,'omitnan');

end
