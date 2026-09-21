
import matplotlib.pyplot as plt
import seaborn as sns
import os

OUTPUT_DIR = r"d:\Data-Science-Project\outputs\phase2"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def setup_style():
    sns.set_theme(style="whitegrid", palette="muted")

def save_plot(fig, name):
    fig.savefig(os.path.join(OUTPUT_DIR, name), bbox_inches='tight', dpi=300)
