function features = emailFeatures(word_indices)
  features = zeros(1899,1);
  for i = 1:length(word_indices)
    features(word_indices(i)) = 1;
  end
  end