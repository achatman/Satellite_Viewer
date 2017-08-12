# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 17:13:26 2017

@author: Andrew
"""

import requests
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np

def get_orbit_params(idnum):
  s = requests.Session()  
  
  login_url = "https://www.space-track.org/ajaxauth/login"
  payload = {"identity": "andrew.chatman9@gmail.com", "password": "GZkys4iyCRHz3PfbFsKbE4rkOSLpBg"}
  r = s.post(login_url, data = payload)
  print("Login:", r.status_code, r.reason)
  
  query_url = "https://www.space-track.org/basicspacedata/query/class/tle/limit/1/format/json/NORAD_CAT_ID/" + str(idnum)
  r = s.get(query_url)
  print("Query:", r.status_code, r.reason)
  
  return r.json()[0]

def get_mult_orbits(sat_arr):
  s = requests.Session()
  login_url = "https://www.space-track.org/ajaxauth/login"
  payload = {"identity": "andrew.chatman9@gmail.com", "password": "GZkys4iyCRHz3PfbFsKbE4rkOSLpBg"}
  r = s.post(login_url, data = payload)
  print("Login:", r.status_code, r.reason)
  
  query_url = "https://www.space-track.org/basicspacedata/query/class/tle_latest/ORDINAL/1/format/json/NORAD_CAT_ID/"
  for g in sat_arr:
    query_url += str(g) + ','
  query_url = query_url[:-1]
  r = s.get(query_url)
  print("Query:", r.status_code, r.reason)
  
  return r.json()

# a - semi-major axis
# e - eccentricity
# i - inclination
# Ω - right ascension of ascending node
# ω - argument of perigee
def cartesianEllipse(a,e,i,Ω,ω):
  ν = np.linspace(-1 * np.pi, np.pi, 100)
  r = a*(1-e**2) / (1 + e*np.cos(ν))
  i *= np.pi / 180
  Ω *= np.pi / 180
  ω *= np.pi / 180
  X = r*(np.cos(Ω)*np.cos(ω + ν) - np.sin(Ω)*np.sin(ω + ν)*np.cos(i))
  Y = r*(np.sin(Ω)*np.cos(ω + ν) + np.cos(Ω)*np.sin(ω + ν)*np.cos(i))
  Z = r*np.sin(ω + ν) * np.sin(i)
  return [X,Y,Z]


fig = plt.figure()
ax = fig.add_subplot('111', projection='3d')
ax.set_aspect('equal')
#Draw Earth
φ = np.linspace(0, 2 * np.pi, 100)
θ = np.linspace(0, np.pi, 100)
r = 6371
x = r * np.outer(np.cos(φ), np.sin(θ))
y = r * np.outer(np.sin(φ), np.sin(θ))
z = r * np.cos(θ)
ax.plot_surface(x, y, z, color = 'g')
#add sats
sats = []
with open('HEO.txt', mode = 'r') as r:
  for line in r:
    sats.append(line.strip())
print("nSats:", len(sats))
data = get_mult_orbits(sats)
for i in range(len(data)):
  params = data[i]
  orbit = cartesianEllipse(float(params["SEMIMAJOR_AXIS"]),
                           float(params["ECCENTRICITY"]),
                           float(params["INCLINATION"]),
                           float(params["RA_OF_ASC_NODE"]),
                           float(params["ARG_OF_PERICENTER"]))
  ax.plot(*orbit, label = 'parametric curve')
lower_lim = min(ax.get_xlim()[0], ax.get_ylim()[0], ax.get_zlim()[0])
upper_lim = max(ax.get_xlim()[1], ax.get_ylim()[1], ax.get_zlim()[1])
ax.set_xlim(lower_lim, upper_lim)
ax.set_ylim(lower_lim, upper_lim)
ax.set_zlim(lower_lim, upper_lim)
plt.show()