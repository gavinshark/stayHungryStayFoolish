function [U, S] = pca(X_norm)
  % X_norm-m*n
  Xcorr = X_norm'*X_norm; %n*n
  %SVD
  [U S V] = svd(Xcorr);
  end