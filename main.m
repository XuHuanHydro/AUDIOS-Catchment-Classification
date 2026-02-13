%% This demonstrates how to read a CSV file containing a single catchment to calculate class.
 
clear;clc;close all
 
T = readtable('.\demoData\Basin_ID1.csv');
sig=compute_all_signatures(T.Q, T.P, T.date);
Class= classify_by_tree(sig);


disp('The catchment is classified as:')
disp(Class)
%% This demonstrates how to read a MAT file containing multiple catchments to calculate classes.
clear;

load('.\demoData\multipleBasin.mat')
SigTable = table();
nBasin=height(BasinTS);
 
for jj = 1:nBasin 
    Q    = BasinTS.Q{jj};
    P    = BasinTS.P{jj};
    date = BasinTS.date{jj};

    S = compute_all_signatures(Q, P, date);

    SigTable = [SigTable; struct2table(S)];
end
  
SigTable.Basin = BasinTS.Basin;
SigTable = movevars(SigTable,'Basin','Before',1);

for jj = 1:nBasin
    Class(jj,1) = classify_by_tree(table2struct(SigTable(jj,:)));
end

disp('The top ten catchments are classified as follows:')
disp(Class(1:10))

