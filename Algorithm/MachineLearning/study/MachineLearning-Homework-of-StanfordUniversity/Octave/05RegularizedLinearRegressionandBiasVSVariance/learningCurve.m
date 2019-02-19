function [error_train, error_val] = learningCurve(X, y, Xval, yval, lambda)
  %X,Xval:m/n*2
  %y,yval:m/n*1
  m=size(X,1);
  error_train = zeros(m,1);
  error_val = zeros(m,1);
  
  for i = 1:m
    theta = trainLinearReg(X(1:i,:), y(1:i,:), lambda);%2*1
    error_train(i) = linearRegCostFunction(X(1:i,:), y(1:i,:), theta, lambda);
    error_val(i)  = linearRegCostFunction(Xval, yval, theta, lambda);
  end
  
  end