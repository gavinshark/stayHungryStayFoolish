function sim = gaussianKernel(x1, x2, sigma)
  diff = x1 - x2;
  diff_metric = sum(diff.^2);
  sim = exp(-diff_metric/2/(sigma^2));
  end