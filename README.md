# Bias Visualizer & Application Predictor
## 1. Overview
Fair warning: this is a direct product of nothing but my hyperfixation on solving a problem that didn't need a solution.

For a club that I am in at USC, there are 9 people on the e-board who need to grade applications.
As I am the director of  membership, I am in charge of setting up a fair system to grade said apps.
There are 100-200 apps that come in every semester, and as we are all busy college students, we do not have time to read
every single app.
Therefore, we read five apps, then skip four, all of us on a different cycle.
This creates a system where the same five people read every ninth app in a circular fashion.

Each grader grades an app on a 1 - 5 scale based on a rubric I developed.
But alas, rubrics are not extensive, and people were giving different results that puzzled me.

This got me thinking, what if one person is meaner or nicer than the rest of the graders?
I'm not gonna bore you with my thought process until how I got to making this script, but I ended up here.

I made this visualization & prediction script to:
1. determine relative biases between graders
2. use those biases in order to predict scores that non-graders would give applications
3. determine whether there is a __significant__ difference between graders
4. show these relevant statistics in a meaningful manner
5. develop a customizable framework to estimate differently based on different applications & situations


## 2. Data Privacy
There are lots of applications, and I was too lazy to keep copying over the data,
so I linked it to the club's Google account. 
However, a side effect of this is that there is literally no trace of the application or data!
Anyone in the club that wants this taken down for the sake of transparency please let me know.
I really, highly doubt that there'll be people investigating my github for club secrets.
If I do upload an example down the road, I will remove traces of names.


## 3. Data/Code Explanation
### 3.1 How to run
Anyone in the club that wants the API key to reuse the code, follow these instructions 
(you have to have access to the google account):
https://developers.google.com/sheets/api/quickstart/python

You'll need to edit refresh.py to get it to run with the new API key.

If you don't belong to the club, don't judge my code too harshly. 
Change it as you will, I'm really not too attached to it.

Change the variables at the top of runner.py to change the settings, 
I explained in the comments what each one does. The most important ones are the `lo_cutoff` and `hi_cutoff`
variables in the parameters of `determine_bias`. These will filter the analysis to only scores with an average
between these values. Make sure to keep this range small: graders grade differently depending on what range of scores
it belongs to.

### 3.2 Data Visualization
For any two graders that graded the same app, I took `grader_score - other_grader_score`.
These differences are put into a 9 x 9 matrix of average differences, and also a 9 x 9 matrix of
number of times the graders intersected in giving a score.

The first table you will see in the .png outputs are averages of this difference.
Each value represents the average of each  `grader_row - grader_col`,
and the color intensity represents the number of times they gave a similar score.

The next table you will see is the standard deviations of every pair of graders' differences.
If it has a green background, the pair difference's average plus or minus 
the standard deviation's range intersects zero.
This basically means the difference is not statistically significant in my view.
Next, if it has a blue background, the pair difference's average plus or minus 
the standard deviation's range does not intersect zero.
This means that the pairing's difference is statistically significant.
The strength of the background is how far away the difference of the absolute value and average is from zero.

If there is a relatively strong blue color in both tables in the same position, this is an example
of those two people's biases being significant, as the bias listed in the first table has lots of examples to back the
average up, and the mean is more than one standard deviation away from 0.
However, this likely won't be the case. Instead, I believe a single blue color in the second graph is enough
indication of bias, provided the respective value in the first table is is not 0. 
This means that given the same application, you could predict one person gives a higher score than the other.

The last graph is a weighted sum of all the biases. While it's not a super thorough metric,
it's interesting to see how people's relative biases are different compared with the group at large.
There are additional error bars representing standard deviation for each person.

### 3.3 CSV Explanation
One of the reasons I wanted to make this program was to predict people's grades based on other people's scores.
The output for the csv is exactly this. For every place in the grading data that doesn't have a value,
I use a weighted average of the scores each grader gives plus their respective bias to come up with an estimated value.

Any score that is changed will have a created_est value of 1, and any application that didn't fall within the 
lo/hi filter set in runner.py will have a create_est value of 0.

## 4. In Practice
I will update this section after the recruitment process finishes. At this point, we grade applications to select people
above a certain threshold to interview. I highly recommend anyone using this to be inclusive about results, meaning
only use my code to accept people who might've had a better chance with different graders 
instead of people who would've had a worse chance with different graders.

## 5. Future Development
I will most likely work on this project again in the winter. I want to develop a neural network with more parameters
than just the other scores - e.g. major/year of applicant, length of applicant responses, maybe even some NLP.

I want to add more parameters to the filters as well. Right now, I have a filter that only judges scores based on
their average at the moment, but I think this could be expanded to major, year, etc.

In terms of visualization, I think I need to do more work next semester to get a plot about the difference between
the estimated average values and previous average values for each application. I ran out of time this year.