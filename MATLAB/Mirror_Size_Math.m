close all
clear
clc

% ------------------------- %

z_pos = 0:1:90; % deg
x_pos = 0:1:90; % deg

dist_from_mirror = 0.2; %m

mirror_size_z = 0.2; %m
mirror_size_x = 0.1; %m

target_fov = 53; % deg

% ------------------------------ %

apparent_x_size = mirror_size_x.*cosd(x_pos); % m
apparent_z_size = mirror_size_z.*cosd(z_pos); % m


z_fov = atand((apparent_z_size/2)/dist_from_mirror) * 2; % deg
x_fov = atand((apparent_x_size/2)/dist_from_mirror) * 2; % deg

plot(z_pos, z_fov)


