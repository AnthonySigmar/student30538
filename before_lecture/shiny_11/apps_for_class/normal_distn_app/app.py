from shiny import App, render, ui, reactive
from shinywidgets import render_altair, output_widget
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app_ui = ui.page_fluid(
    ui.panel_title("Histogram of 200 Draws from Normal with mean mu"),
    ui.input_slider("mu", "mean mu", 0, 100, 20), 
    ui.output_plot("my_hist"),
    ui.output_text_verbatim("my_sumstats")
)

def server(input, output, session):
    #@output_widget
    @render_altair #altair cannot display in shiny!
    #@render.plot
    def my_hist():
        #sample = np.random.normal(input.mu(), 20, 100)
        '''
        fig, ax = plt.subplots()
        ax.hist(sample(), bins=30, color='blue', alpha=0.7)
        return fig
        '''
        df = pd.DataFrame({'sample': sample()})
        chart = alt.Chart(df).mark_bar().encode(
            alt.X('sample:Q', bin=alt.Bin(maxbins=30)), 
            alt.Y('count()')  
        ).properties(
            title="Histogram of Normal Distribution"
        )
        
        return chart

    @render.text
    def my_sumstats():
        #sample = np.random.normal(input.mu(), 20, 100)
        min = np.min(sample())
        max = np.max(sample())
        median = np.median(sample())
        return "Min:" + str(min) + ", Median: " + str(median), ", Max: " + str(max)
    
    @reactive.calc
    def sample():
        return(np.random.normal(input.mu(), 20, 100))

app = App(app_ui, server)