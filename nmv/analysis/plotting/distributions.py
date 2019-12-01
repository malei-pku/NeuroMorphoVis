####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This program is free software: you can redistribute it and/or modify it under the terms of the
# GNU General Public License as published by the Free Software Foundation, version 3 of the License.
#
# This Blender-based tool is distributed in the hope that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this program.
# If not, see <http://www.gnu.org/licenses/>.
####################################################################################################


import nmv.consts
import nmv.utilities



def plot_per_arbor_distribution(analysis_results,
                                morphology,
                                options,
                                figure_name=None,
                                x_label=None,
                                title=None,
                                add_percentage=False):

    # Plotting imports
    import numpy
    import seaborn
    import pandas
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.ticker import MaxNLocator

    plt.clf()

    # Import the fonts
    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

    # Adjust configuration
    seaborn.set_style("whitegrid")
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'regular'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['axes.titlesize'] = 15

    # Total number of arbors
    total_arbors = 0

    # X-axis data
    x_data = list()

    # Y-axis data
    y_data = list()

    # Colors
    colors = list()
    color_codes = ['axon', 'basal', 'apical']

    # Collecting the lists, Axon
    if analysis_results.axon_result is not None:
        x_data.append('Axon')
        y_data.append(analysis_results.axon_result)
        colors.append(color_codes[0])
        total_arbors += 1

    # Basal dendrites
    if analysis_results.basal_dendrites_result is not None:
        for i, result in enumerate(analysis_results.basal_dendrites_result):
            x_data.append('Basal Dendrite %d' % i)
            y_data.append(result)
            colors.append(color_codes[1])
            total_arbors += 1

    # Apical dendrite
    if analysis_results.apical_dendrite_result is not None:
        x_data.append('Apical Dendrite')
        y_data.append(analysis_results.apical_dendrite_result)
        colors.append(color_codes[2])
        total_arbors += 1

    # Construct the color palette
    hex_colors = [str(nmv.utilities.rgb_vector_to_hex(options.morphology.axon_color)),
                  str(nmv.utilities.rgb_vector_to_hex(options.morphology.basal_dendrites_color)),
                  str(nmv.utilities.rgb_vector_to_hex(options.morphology.apical_dendrites_color))]
    hex_color_list = lambda x: hex_colors[color_codes.index(x)]
    palette = list()
    for item in colors:
        palette.append(hex_color_list(item))

    # Construct the numpy arrays
    x = numpy.asarray(x_data)
    y = numpy.asarray(y_data)

    # Adjust the figure size
    plt.figure(figsize=(5, total_arbors * 0.5))

    # Plot the figure
    ax = seaborn.barplot(x=y, y=x, palette=palette)

    # Add percentage to the data
    if add_percentage:
        total_patches_width = []
        for i in ax.patches:
            total_patches_width.append(i.get_width())
        total_width = sum(total_patches_width)
        for i in ax.patches:
            ax.text(i.get_width(), i.get_y() + .5,
                    '  ' + str(round((i.get_width() / total_width) * 100, 2)) + '%', fontsize=10,
                    color='dimgrey')

    # Set figure parameters
    ax.set(xlabel=x_label, title=title)
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))

    # Save the figure
    plt.savefig('%s/%s-%s.pdf' % (options.io.analysis_directory,
                                  morphology.label,
                                  figure_name),
                bbox_inches='tight')

    # Close the figures
    plt.close()




def plot_min_avg_max_per_arbor_distribution(minimum_results,
                                            average_results,
                                            maximum_results,
                                            morphology,
                                            options,
                                            figure_name=None,
                                            x_label=None,
                                            title=None,):
    # Plotting imports
    import numpy
    import seaborn
    import pandas
    import matplotlib.pyplot as plt
    from matplotlib import font_manager
    from matplotlib.ticker import MaxNLocator

    plt.clf()

    # Import the fonts
    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    font_list = font_manager.createFontList(font_files)
    font_manager.fontManager.ttflist.extend(font_list)

    # Adjust configuration
    seaborn.set_style("whitegrid")
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'regular'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['axes.titlesize'] = 15

    # X-axis data
    x_data = list()

    # Y-axis data
    y_min_data = list()
    y_avg_data = list()
    y_max_data = list()

    # Collecting the lists, Axon
    if minimum_results.axon_result is not None:
        x_data.append('Axon')
        y_min_data.append(minimum_results.axon_result)
        y_avg_data.append(average_results.axon_result)
        y_max_data.append(maximum_results.axon_result)

        #colors.append(color_codes[0])
        #total_arbors += 1

    # Basal dendrites
    number_basals = len(minimum_results.basal_dendrites_result)
    if minimum_results.basal_dendrites_result is not None:
        for i in range(number_basals):
            x_data.append('Basal Dendrite %d' % i)
            y_min_data.append(minimum_results.basal_dendrites_result[i])
            y_avg_data.append(average_results.basal_dendrites_result[i])
            y_max_data.append(maximum_results.basal_dendrites_result[i])

            #colors.append(color_codes[1])
            #total_arbors += 1

    # Apical dendrite
    if minimum_results.apical_dendrite_result is not None:
        x_data.append('Apical Dendrite')
        y_min_data.append(minimum_results.apical_dendrite_result)
        y_avg_data.append(average_results.apical_dendrite_result)
        y_max_data.append(maximum_results.apical_dendrite_result)

        #colors.append(color_codes[2])
        #total_arbors += 1


    print(x_data)
    print(y_min_data)
    print(y_avg_data)
    print(y_max_data)
    pass


def plot_distribution(distribution,
                      tilte,
                      normalized=False,
                      color='b'):
    import os
    import numpy as np
    import seaborn as sns
    import pandas as pd
    import matplotlib
    import matplotlib.pyplot as plt


    from matplotlib import font_manager as fm, rcParams
    fpath = '%s/%s' % (nmv.consts.Paths.FONTS_DIRECTORY, 'arial.ttf')

    prop = fm.FontProperties(fname=fpath)

    fm.findSystemFonts(fontpaths=nmv.consts.Paths.FONTS_DIRECTORY,
                       fontext='ttf')

    sns.set(color_codes=True)

    font_dirs = [nmv.consts.Paths.FONTS_DIRECTORY]
    font_files = fm.findSystemFonts(fontpaths=font_dirs)
    font_list = fm.createFontList(font_files)
    fm.fontManager.ttflist.extend(font_list)


    sns.set_style("whitegrid")
    plt.rcParams['axes.grid'] = 'False'
    plt.rcParams['font.family'] = 'Arial'
    #plt.rcParams['font.monospace'] = 'Regular'
    #plt.rcParams['font.style'] = 'normal'

    plt.rcParams['axes.linewidth'] = 0.0
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.labelweight'] = 'bold'
    plt.rcParams['xtick.labelsize'] = 10
    plt.rcParams['ytick.labelsize'] = 10
    plt.rcParams['legend.fontsize'] = 10
    plt.rcParams['figure.titlesize'] = 10
    plt.rcParams['axes.titlesize'] = 10

    # Convert the distribution list to a numpy array
    np_distribution = np.array(distribution)

    # Adjust the Y-axis format
    # plt.gca().yaxis.set_major_formatter(PercentFormatter(xmax=xmax, symbol=' %'))

    # Set the title
    plt.title('Samples')

    # Plot the histogram
    sns.distplot(np_distribution, color='r',kde=False, hist=True, norm_hist=normalized,
                 hist_kws={"color": color, "lw": 0.5},
                 kde_kws={"color": color, "lw": 0.5})

    plt.savefig('%s/neuromorphovis-output/%s-plot.pdf' % (os.path.expanduser('~'), tilte), dpi=150)

    # Close figure to reset
    plt.close()


####################################################################################################
# @plot_analysis_results
####################################################################################################
def plot_analysis_results(analysis_results):

    if analysis_results.apical_dendrite_result is not None:
        plot_distribution(analysis_results.apical_dendrite_result, 'apical-dendrite')

    if analysis_results.basal_dendrites_result is not None:
        for i, basal_dendrite_result in enumerate(analysis_results.basal_dendrites_result):
            plot_distribution(basal_dendrite_result, 'basal-dendrite-%d' % i)

    if analysis_results.axon_result is not None:
        plot_distribution(analysis_results.axon_result, 'axon')
