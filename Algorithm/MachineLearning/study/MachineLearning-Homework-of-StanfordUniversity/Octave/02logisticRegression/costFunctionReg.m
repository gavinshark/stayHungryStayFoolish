function [cost, grad] = costFunctionReg(theta, X, y, lambda)
  [cost grad] = costFunction(theta, X, y);
  cost = lambda/2/length(y)*sum(theta(2:end).^2) + cost;
  grad = lambda/length(y)*theta.' + grad;  
 end