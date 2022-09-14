% Scanning Rates
% Connor McKinney
% 8-30-2022
% This program is an evaluation tool to see what rotation rates we need
clc
clear
close all
% Distance to the closest point of the flight path in meters
standoff_dist = 5; % m

% Projectile speed in meters per second
% Google says a nerf gun fires at 21 m/s
projectile_speed = 21; % m/s

% Scan ratio
scan_ratio = projectile_speed/standoff_dist;

% The angular range of the optic in degrees
angular_range = 60; % degrees

% Framerate of camera
framerate = 100;

% Control system update rate
controlrate = 1000;

%time_step
time_step = 0.0001;

% --------------------------------------- %

% define theta at initial conditions
start_angle = angular_range/2;

% Opposite side of the triangle from theta at initial conditions
start_dist = standoff_dist*tand(start_angle);

% Total time of tracking
total_time = start_dist * 2/projectile_speed;

frametime = 1/framerate;
controltime = 1/controlrate;

total_frames = total_time/frametime

total_control_updates = total_time/controltime

% Time vector
time = 0:time_step:total_time;

% Tracks the position of the projectile
current_dist = start_dist-time.*projectile_speed;
current_theta = rad2deg(atan(current_dist/standoff_dist));

% Checking my math
theta_eqn = polyfit(time, current_theta, 8);
theta_deriv = polyder(theta_eqn);
theta_deriv_vals = polyval(theta_deriv, time);

alpha_eqn = polyder(theta_deriv);
alpha_eqn_vals = -1*polyval(alpha_eqn, time);
%



d_theta = abs( rad2deg( (-projectile_speed.*cosd(current_theta).^2)./standoff_dist));

d_theta_max = max(d_theta); 

% Max is also the following calculation
% abs( rad2deg( (-projectile_speed.*cosd(0).^2)./standoff_dist)));
% Max is also roughly rad2deg(scan_ratio) if the projectile's velocity is
% constant.


fprintf("Standoff Dist(m)    Velocity(m/s)    Scan Ratio(rad/s)\n")  
fprintf("    %.4f            %.4f             %.4f\n\n", standoff_dist, ...
    projectile_speed, scan_ratio)

fprintf("Max Rotation Rate(deg/s)    Time of Flight(s)\n")
fprintf("      %.4f                    %.4f\n\n", d_theta_max, total_time)

hold all
plot(time, d_theta)
ylabel("See legend for units")
xlabel("Time (s)")
plot(time, current_theta)
%plot(total_time/2, d_theta_max, "xr")
plot(time, alpha_eqn_vals)
legend("Rotation Rate (Deg/s)", "Theta (Deg)", "Alpha (Deg/s^2)")
hold off


