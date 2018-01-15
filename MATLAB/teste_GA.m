function [x,endPop,bestSols,trace] = teste_GA()

addpath 'gaot'

%saida
%x --> vetor com os melhores parametros encontrados. (ultimo elemento eh o resultado obtido)
%bestSols --> mostra os individuos que obteram melhora do resultado
%trace --> mostra a evolucao dos individuos ao longo das geracoes
%endPop --> mostra a populacao final 

%3 parâmetros: maximização da função avaliação
load data dados target;

max_index = max(dados(:))
param(1:max_index,1) = -2; %limite inferior do param 1 e 2 
param(1:max_index,2) = 2; %limite superior do param 1 e 2 

%clear data

[x,endPop,bestSols,trace]=ga(param,'avaliacao');
end





