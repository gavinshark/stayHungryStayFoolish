function [epsilon F1] = selectThreshold(yval, pval)
  stepsize = (max(pval) - min(pval)) / 1000;
  epsilon_matrix = min(pval):stepsize:max(pval);
  F1_matrix = zeros(size(epsilon_matrix));
  m = length(yval);
  for i = 1:length(epsilon_matrix)
    epsilon_tmp = epsilon_matrix(i);
    predict_arr = pval < epsilon_tmp;
    tp = sum(predict_arr.^yval);
    fp = sum(predict_arr.^(yval==0));
    fn = sum(predict_arr.^(yval==1));
    prec = tp/(tp+fp);
    rec = tp/(tp+fn);
    F1_matrix(i) = 2*prec*rec/(prec+rec);    
    end
    
    [F1 minidx] = max(F1_matrix);
    epsilon = epsilon_matrix(minidx);
  end