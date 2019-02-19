function [pred] =  predictOneVsAll(all_theta, X)
  %all_theta:10*401
  %X:m*401
  X = [ones(size(X,1),1) X];%
  [a pred] =  max(X*all_theta',[], 2);
  end