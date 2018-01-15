function [sol,resultado] = avaliacao(sol,options)

load data dados target;

sol((sol < 0.05) & (sol > -0.05)) = 0;

hit = 0;
for i = 1:size(dados,1)
    D=reshape(dados(i,:),2,[])';
    index_line = D(:,1);
    quantity_line = D(:,2);
    for j = 1:size(index_line,1)
        
        word_index = index_line(j);
        
        if(word_index~=0)
          index_line(j) = sol(word_index);
        end
    end

    soma = index_line'*quantity_line;

    if soma >= 0.5
        somaL = 1;
    elseif soma <= -0.5
        somaL = -1;
    else
        somaL = 0;
    end
    
    if somaL == target(i)
        hit = hit + 1;
    end
end
resultado = hit*100/size(dados,1);
end
    
