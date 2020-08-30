import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import refresh


def determine_bias(dir_graphs, lo_cutoff, hi_cutoff,
                   to_refresh=False, produce_est=False, produce_plots=False, show_plots=True):
    print("Starting determine bias:")
    print("\tdir_graphs=" + dir_graphs)
    print("\tlo_cutoff=" + str(lo_cutoff))
    print("\thi_cutoff=" + str(hi_cutoff))
    print("\tto_refresh=" + str(to_refresh))
    print("\tproduce_est=" + str(produce_est))
    print("\tproduce_plots=" + str(produce_plots))
    print("\tshow_plots=" + str(show_plots) + "\n\n")

    if to_refresh:
        refresh.refresh_data()

    print("Starting setup\n")
    grades = pd.read_csv("grades.csv")

    grades_est = grades.copy()
    grades_est.insert(0, "created_est", 0)

    sums = np.zeros((9, 9))
    counts = np.zeros((9, 9))

    avg = grades["Average"]

    # get rid of everything except grader's grades
    i = 0
    for col in grades.columns:
        if i < 5 or i > 13:
            grades.pop(col)
        i += 1


    ind_examples = []
    for x in range(9):
        ind_examples.append([])
        for y in range(9):
            ind_examples[x].append([])

    # get list of graders & size of dataframe
    graders = grades.columns
    num_apps = grades.shape[0]

    grader_dict = dict()
    for x in range(graders.size):
        grader_dict.update({graders[x]: x})

    diff_dict = dict()
    for grader in graders:
        diff_dict.update({grader: []})


    print("First pass through data, taking diff of each similar grade\n")
    # for each application
    for x in range(num_apps):
        # check if app is above avg barrier
        if avg[x] != '#DIV/0!' and (float(avg[x]) < lo_cutoff or float(avg[x]) > hi_cutoff):
            continue

        # get application from that row
        row = grades.loc[x]

        # if there are more than 7 NaNs, skip
        num_nans = row.isna().sum()
        if num_nans > 7:
            continue

        # for each grader, if their grade for that isn't nan
        for grader in graders:
            if np.isnan(row[grader]):
                continue

            # for each other grader, if they aren't the same person or their grade isn't nan
            for other_grader in graders:
                if other_grader == grader or np.isnan(row[other_grader]):
                    continue
                sums[grader_dict[grader]][grader_dict[other_grader]] += row[grader] - row[other_grader]
                diff_dict[grader].append(row[grader] - row[other_grader])
                ind_examples[grader_dict[grader]][grader_dict[other_grader]].append(row[grader] - row[other_grader])
                counts[grader_dict[grader]][grader_dict[other_grader]] += 1

    print("Crunching numbers\n")
    # get array of standard deviations for each person
    std_dev_arr = np.zeros(9)
    for grader in graders:
        std_dev_arr[grader_dict[grader]] = np.std(np.array(diff_dict[grader]))

    # get count matrix that we can divide by - replace 0's with 1's
    div_counts = counts
    div_counts[div_counts == 0] = 1

    # divide sum by counts to get bias
    average_biases = sums / div_counts
    average_biases = np.around(average_biases, 3)

    bias_frame = pd.DataFrame(average_biases, columns=graders, index=graders)

    print("Second pass through data this is totally efficient haha (actually tho we need the averages so go away)\n")
    # create predictions
    # for each application in grades_est
    for x in range(num_apps):
        # check if app is within avg barrier
        if avg[x] != '#DIV/0!' and (float(avg[x]) < lo_cutoff or float(avg[x]) > hi_cutoff):
            continue

        row = grades.loc[x]

        num_nans = row.isna().sum()
        if num_nans >= 9:
            continue

        # for each grader
        for grader in graders:
            if not np.isnan(row[grader]):
                continue

            running_score = 0
            running_count = 0

            # for each other grader, if they aren't the same person or their grade isn't nan
            for other_grader in graders:
                if other_grader == grader or np.isnan(row[other_grader]):
                    continue

                # add to running score the average bias between graders times the count of apps they graded together
                running_score += (average_biases[grader_dict[grader]][grader_dict[other_grader]] + row[other_grader]) \
                    * counts[grader_dict[grader]][grader_dict[other_grader]]

                # add to running count the count of how many times this was influenced
                running_count += counts[grader_dict[grader]][grader_dict[other_grader]]
            grades_est.at[x, grader] = running_score/running_count
            grades_est.at[x, "created_est"] = 1

    if produce_est:
        print("Saving csv")
        grades_est.to_csv(dir_graphs + "csv/est_" + str(lo_cutoff) + "_" + str(hi_cutoff) + ".csv")
        print("Finished saving csv\n")

    print("More number crunching kill me\n")
    std_devs = np.zeros((9, 9))
    for x in range(9):
        for y in range(9):
            examples = np.array(ind_examples[x][y])
            if examples.size > 1:
                std_devs[x][y] = examples.std()

    std_devs_rounded = np.around(std_devs, 3)
    below_zero = std_devs_rounded - np.abs(average_biases)

    print("plot time ooga booga \n")
    # create matplotlib figure
    fig = plt.figure(frameon=False, figsize=(9, 12))

    colors = np.ones((9, 9), dtype=(float, 3))
    counts_ratio = counts / (counts.max() * 2)

    colors[:, :, 0] -= counts_ratio
    colors[:, :, 1] -= counts_ratio

    # find running sum of everyone's trials, get standard dev diff arrs
    avg_start = sums.sum(axis=1)
    avg = avg_start / counts.sum(axis=1)

    ax = fig.add_subplot(311)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_title("Row - Col average score")

    colors2 = np.ones((9, 9), dtype=(float, 3))
    colors2_ratio = np.abs(below_zero) / (np.abs(below_zero).max() * 2)

    colors2[:, :, 0] -= colors2_ratio
    for x in range(9):
        for y in range(9):
            if below_zero[x][y] < 0:
                colors2[x, y, 1] -= colors2_ratio[x][y]
            else:
                colors2[x, y, 2] -= colors2_ratio[x][y]

    ax.table(
        cellText=average_biases,
        cellColours=colors,
        rowLabels=graders.to_numpy(),
        colLabels=graders.to_numpy(),
        loc="center",
        label="A = rows, B = cols"
    )

    ax = fig.add_subplot(312)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
    ax.set_title("Row - Col std devs")
    ax.table(
        cellText=std_devs_rounded,
        cellColours=colors2,
        rowLabels=graders.to_numpy(),
        colLabels=graders.to_numpy(),
        loc="center",
        label="A = rows, B = cols"
    )

    ax = fig.add_subplot(313)
    ax.set_title("Weighted avg diff between you and everyone for apps w/ avg scores btwn " +
                 str(lo_cutoff) + " - " + str(hi_cutoff))
    bar = ax.bar(graders.to_numpy(), avg, yerr=std_dev_arr, capsize=5)
    ax.yaxis.grid(True)
    size_sum = counts.sum(axis=1)

    def auto_label(rects):
        """Attach a text label above each bar in *rects*, displaying its height."""

        cnt = 0
        bbox_props = dict(boxstyle="round,pad=0.2", fc="white", ec="k", lw=2)

        for rect in rects:
            height = rect.get_height()
            if height > 0:
                ax.annotate(
                    '{height:.3f}'.format(height=height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 6),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom', color='black', bbox=bbox_props
                )
                ax.annotate(
                    str(size_sum[cnt]),
                    xy=(rect.get_x(), 0),
                    xytext=(0, -3),
                    textcoords="offset points",
                    ha='left', va='top', color='black', fontsize='x-small'
                )
            else:
                ax.annotate(
                    '{height:.3f}'.format(height=height),
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, -6),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='top', color='black', bbox=bbox_props
                )
                ax.annotate(
                    str(size_sum[cnt]),
                    xy=(rect.get_x(), 0),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='left', va='bottom', color='black', fontsize='x-small'
                )
            cnt += 1

    auto_label(bar)
    if show_plots:
        print("showing plot")
        plt.show()
    if produce_plots:
        print("saving plot")
        plt.savefig(dir_graphs + "png/plots_" + str(lo_cutoff) + "_" + str(hi_cutoff) + ".png")
        print("plot saved!")
    print("\n\n\n")
