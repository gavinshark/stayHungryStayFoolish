function [lambda_vec, error_train, error_val] = ...
    validationCurve(X_poly, y, X_poly_val, yval)    
    lambda_vec = [0,0.001,0.003,0.01,0.03,0.1,0.3,1,3,10];
    error_train = zeros(size(lambda_vec));
    error_val = zeros(size(lambda_vec));
  
  for i =1:size(lambda_vec,2)
    theta = trainLinearReg(X_poly, y, lambda_vec(i));%2*1
    error_train(i) = linearRegCostFunction(X_poly, y, theta, 0);
    error_val(i)  = linearRegCostFunction(X_poly_val, yval, theta, 0);
  end   
    
 end