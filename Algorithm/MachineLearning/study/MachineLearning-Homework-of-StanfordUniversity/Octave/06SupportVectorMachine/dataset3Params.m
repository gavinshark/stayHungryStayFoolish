function [C, sigma] = dataset3Params(X, y, Xval, yval)
  C = 1;
  sigma = 0.3;  
  C_vec = [0.01 0.03 0.1 0.3 1 3 10 30]';
  sigma_vec = [0.01 0.03 0.1 0.3 1 3 10 30]';
  
  error_val = zeros(length(C_vec),length(sigma_vec));
  error_train = zeros(length(C_vec),length(sigma_vec));

  for i = 1:length(C_vec)
    for j = 1:length(sigma_vec)
       model = svmTrain(X, y, C_vec(i), @(x1,x2) gaussianKernel(x1, x2, sigma_vec(j)));
       predictions = svmPredict(model, Xval);
       error_val(i,j) = mean(double(predictions ~= yval));
      end
    end
  
  [minval, ind] = min(error_val(:));
  [I,J]=ind2sub([size(error_val,1) size(error_val,2)], ind);
  C = C_vec(I)
  sigma = sigma_vec(J)
  
  end