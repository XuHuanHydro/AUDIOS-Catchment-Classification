function cls = classify_by_tree(AllSig)

TA2  = AllSig.TA2;
CR1  = AllSig.CR1;
FH3  = AllSig.FH3;
DH5  = AllSig.DH5;
MA2  = AllSig.MA2;
DL18 = AllSig.DL18;

 

if TA2 <= 0.608

    % ===== Left branch =====
    if CR1 <= 0.23

        if FH3 <= 92.292
            cls = 2;
        else
            cls = 1;
        end

    else
        % CR1 > 0.23

        if TA2 <= 0.421

            if DH5 <= 7.48

                if FH3 <= 60.153
                    cls = 5;
                else
                    cls = 4;
                end

            else
                cls = 6;
            end

        else
            % TA2 > 0.421

            if MA2 <= 2.2
                cls = 4;
            else
                cls = 6;
            end

        end
    end

else
    % ===== Right branch =====

    if DL18 <= 97.375

        if CR1 <= 0.404
            cls = 3;
        else
            cls = 4;
        end

    else
        cls = 1;

    end
end

end
