function Z = projectData(X_norm, U, K)
  Ureduce = U(:,1:K); %n*k
  Z = X_norm*Ureduce; %m*k
  end