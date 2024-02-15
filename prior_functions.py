# Imports
import streamlit as st
import numpy as np
import pymc as pm
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import gaussian_kde

@st.cache_data # 👈 Add the caching decorator, make app run faster
def draw_samples_from_prior(dist: pm.Distribution, num_samples: int = 10_000,
                            seed=None, **kwargs) -> np.ndarray:
    """
    Draws samples from the prior distribution of a given PyMC distribution.

    This function creates a PyMC model with a single variable, drawn from the specified
    distribution, and then samples from the prior of this distribution.

    Parameters
    ----------
    dist : pm.Distribution
        The PyMC distribution from which to draw samples.
    num_samples : int, optional
        The number of samples to draw from the prior distribution. Default is 10,000.
    seed : int or None, optional
        The seed for the random number generator to ensure reproducibility. If None, 
        the results will vary between runs. Default is None.
    **kwargs
        Additional keyword arguments to pass to the distribution constructor.
        e.g. sigma for Normal, alpha and beta for Beta.
        See PyMC Distributions for more info: https://www.pymc.io/projects/docs/en/stable/api/distributions.html

    Returns
    -------
    np.ndarray
        An array of samples drawn from the specified prior distribution.
    """
    with pm.Model():

        # Define a variable with the given distribution
        my_dist = dist(name = "my_dist", **kwargs)
        
        # Sample from the prior distribution of the model
        draws = pm.draw(my_dist, draws=num_samples, random_seed=seed)
        
    # Return the drawn samples
    return draws

def plot_prior_distribution(draws, nbins=100, opacity=0.1, title="Prior Distribution - Visualised"):
    """
    Plots samples of a prior distribution as a histogram with a KDE (Kernel Density Estimate) overlay
    and a violin plot along the top too with quartile values.
    
    Parameters:
    - draws: numpy array of samples from prior distribution.
    - nbins: int, the number of bins for the histogram.
    - opacity: float, the opacity level for the histogram bars.
    - title: str, the title of the plot.
    """
    # Create the histogram using Plotly Express
    fig = px.histogram(draws, x=draws, nbins=nbins, title=title, 
                       labels={"x": "Value"}, histnorm='probability density', opacity=opacity,
                       marginal="violin", color_discrete_sequence=['#0047AB'])
    
    # Compute the KDE
    kde = gaussian_kde(draws)
    x_range = np.linspace(min(draws), max(draws), 500)
    kde_values = kde(x_range)
    
    # Add the KDE plot to the histogram figure
    fig.add_trace(go.Scatter(x=x_range, y=kde_values, mode='lines',
                              name='KDE', line_color="#DA70D6",
                              opacity=0.8))
    
    # Customize the layout
    fig.update_layout(xaxis_title='Value of Prior', yaxis_title='Density')
    
    # Return the plot
    return fig