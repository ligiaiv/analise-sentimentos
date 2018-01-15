function [] = import_dados

    load data dados target;
    
    linha = dados(1,:);
    linha
    D=reshape(linha,2,[])';
    
    index_line = D(:,1)
    quantity_line = D(:,2)
    for j = 1:size(index_line,1)
        index_line(j) = sol(index_line(j));
    end
    index_line

end