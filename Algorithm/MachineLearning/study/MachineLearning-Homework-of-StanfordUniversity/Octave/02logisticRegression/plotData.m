function plotData(X, y)
  Index1 = find(y==1);
  Index0 = find(y==0);
  plot(X(Index1,1), X(Index1, 2), 'k+', 'LineWidth', 2, 'MarkerSize', 7);
  hold on
  plot(X(Index0,1), X(Index0, 2), 'ko', 'MarkerFaceColor', 'y', 'MarkerSize', 7);
  
  end