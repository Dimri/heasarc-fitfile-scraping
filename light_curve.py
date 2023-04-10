import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
from datetime import datetime

from astropy.io import fits
from dtw import dtw
from utils import 
from detector.estimate_source_angles_detectors import angle_to_grb
from scipy.stats import poisson 
from dataclasses import dataclass



def dtw_distance_helper(reference, target):
    # distance metric
    manhattan_distance = lambda x, y : np.abs(x-y)
    
    # calculate distance

    d, cost_matrix , acc_cost_matrix, path = dtw(reference, target,
                                                dist=manhattan_distance)

    return d, cost_matrix, acc_cost_matrix, path

def get_dtw_distance(refGRB, tarGRB, show_plot=False):
    '''
    function to calculate DTW distance between reference and target
    light curve
        params : refGRB = reference light curve, GRB class object 
        params : tarGRB = target light curve, GRB class object 
        params : show_plot = shows DTW plot 
        returns : DTW distance between reference and target GRB
    '''
    
    reference = refGRB.get_photon_counts()
    target = tarGRB.get_photon_counts()

    d, _, acc_cost_matrix, path = dtw_distance_helper(reference, target)

    # visualizing the plot
    if show_plot:
        plot_dtw_distance(refGRB, tarGRB, acc_cost_matrix, path)
    
    return d


def plot_dtw_distance(refGRB, tarGRB, acc_cost_matrix, path):
    _, ax = plt.subplots()
    ax = sns.heatmap(acc_cost_matrix.T, cmap='gray', xticklabels=10, yticklabels=10)
    # invert yaxis to show origin at bottom left
    ax.invert_yaxis() 
    ax.plot(path[0], path[1], 'w')
    ax.set_title(f'{refGRB.name} vs {tarGRB.name}', {'fontsize':15})
    # axis labels
    ax.set_xlabel('Reference Light Curve', fontsize=14)
    ax.set_ylabel('Target Light Curve', fontsize=14)
    ax.axvline(refGRB.t90, color='r', label='Reference t90')
    ax.axhline(tarGRB.t90, color='b', label='Target t90')
    ax.legend()
    plt.show()






@dataclass(frozen=True)
class GRBData:
    name : str
    index : int
    refGRBname : str
    ra : float
    dec : float
    t90 : float
    binsize : float
    brightest_detector : str
    distance : float
    sigma : float