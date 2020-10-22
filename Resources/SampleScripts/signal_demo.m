% left & right bounds of time axis (in samples)
nL = 10;
nR = 10;
% create discrete-time vector
n = -nL:nR;
% processing
u = [zeros(1,nL), 1, ones(1,nR)]; % generate u[n]
subplot(3,1,1)
stem(n,u,'fill'); % plot u[n]
title('Unit step u[n]');
xlabel('Time (n)');
ylabel('Amplitude');

u4 = [zeros(1,nL+4), 1, ones(1,nR-4)]; % generate u[n-4]
subplot(3,1,2)
stem(n,u4,'fill'); % plot u[n-4]
title('Time-shifted Unit step u[n-4]');
xlabel('Time (n)');
ylabel('Amplitude');

x = u - u4; % generate u[n-4]
subplot(3,1,3)
stem(n,x,'fill'); % plot x[n]
title('Signal x[n]');
xlabel('Time (n)');
ylabel('Amplitude');