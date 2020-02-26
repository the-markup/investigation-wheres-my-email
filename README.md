# How We Examined Gmail's Treatment of Political Emails
This repository contains code to reproduce the findings featured in our story, "[Swinging the vote?](https://www.themarkup.org/google-the-giant/2020/02/26/wheres-my-email)" from our series, [Google the Giant](https://themarkup.org/google-the-giant/).

Our methodology is described in "[How We Examined Gmail's Treatment of Political Emails](https://themarkup.org/google-the-giant/2020/02/26/show-your-work-wheres-my-email)".

The data for our analysis can be found in the `data` folder.

The Jupyter Notebooks for data preprocessing and analysis are avialble in the `notebooks` folder. Descriptions for each notebook are outlined in the Notebooks section below.

## Installation
Make sure you have Python 3.6+ installed, we used [Miniconda](https://docs.conda.io/en/latest/miniconda.html) to create a Python 3.8 environment.

Install Python packages:<br>
`pip install -r requirements.txt`

## Data
This folder contains all the data that was used, or created by our experiment. 

We have several folders used to organize the data:<br>

| Folder                | Description                                                                         |
|:----------------------|:------------------------------------------------------------------------------------|
| `data/input/`         | contains the data we used as input for the story.                                   |
| `data/intermediates/` | intermediate datasets created from the inputs.                                      |
| `data/outputs/`       | tables and appendix items created from intermediates.     

Here's a bit about the data:

#### data/input/newsletter_categories.csv
A spreadsheet we created to keep track of the 231 political entities we opted into for email notifications.

Data dictionary:

| Column    | Description                                                                                                                                                                |
|:----------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Name      | The name of the politcian or organization.                                                                                                                                 |
| Website   | The website we signed up for email updates or newsletters.                                                                                                                 |
| Email     | Our custom email alias used during sign up.                                                                                                                                |
| Category  | Our categorization of the email sender. Our categories: `Presidential candidate`,`House battleground campaign`, `House battleground official`, or `Advocacy organization`. |
| Entity_ID | A unique ID we created for each entity. The md5 hash of the Name and the Category.                                                                                         |

Links: [Formatted](https://github.com/the-markup/investigation-wheres-my-email/blob/master/data/input/newsletter_categories.csv) | [Raw](https://raw.githubusercontent.com/the-markup/investigation-wheres-my-email/master/data/input/newsletter_categories.csv)


#### data/input/open_rate_ratio_aggregated.csv
This is data that we processed of of Gmail email open rates relative to non-Gmail open dates. The input data was given to us by Change.org, CREDO Action, Democracy for America, and Sum of US and spans from January 2017 to March 2019.

Data dictionary:

| Column       | Description                                                                                                   |
|:-------------|:--------------------------------------------------------------------------------------------------------------|
| date         | A datetime representing one month of data formatted `"%Y-%m-%d"`                                              |
| ratio_gm_ngm | The ratio to Gmail to non Gmail open rates. <br>The calculation is in `notebooks/0-intro-to-the-story.ipynb`. |
| org          | The name of an organization.                                                                                  |

Links: [Formatted](https://github.com/the-markup/investigation-wheres-my-email/blob/master/data/input/open_rate_ratio_aggregated.csv) | [Raw](https://raw.githubusercontent.com/the-markup/investigation-wheres-my-email/master/data/input/open_rate_ratio_aggregated.csv)

#### data/input/google_takeout_mboxes_gzip/*.mbox.gz
The political emails from our experiment are saved here. This is a folder of gzipped mbox files, which were regularly exported from the inbox we set up for our experiment.

All available metadata fields for emails can be viewed in this JSON file:<br>
`data/input/mbox_email_example.json`

We exported the mbox files using Google takeout at least once every 30 days. The data in this folder spans from October 16th, 2019 to Febrary 12th 2020.

Get more context about why we collected this dataset from our [paper](https://themarkup.org/google-the-giant/2020/02/26/show-your-work-wheres-my-email).

We preprocess this data and merge it with `data/input/newsletter_categories.csv` to produce the next file:


#### data/intermediates/email_metadata_merged_with_newsletters.csv.gz
The clean dataset (N=5,134) our analysis uses. Each row represents one email.

Data dictionary:

| Column              | Description                                                                                                                                                                        |
|:--------------------|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| X-GM-THRID          | Gmail-created email header for thread ID of an email. Extracted from mbox files.                                                                                                   |
| X-Gmail-Labels      | A comma-delimited list of Gmail's classifications per email Extracted from mbox files.                                                                                             |
| Date                | The date the email was received. Extracted from mbox files.                                                                                                                        |
| Subject             | The email subject line. Extracted from mbox files.                                                                                                                                 |
| text                | The message body of an email. Processed from mbox files.                                                                                                                           |
| markup_id           | A unique identifier we create, based off an md5 hash of `X-GM-THRID` and `Date`.                                                                                                   |
| Category Personal   | Boolean column we set to 1 if this category was included in `X-Gmail-Labels`.                                                                                                      |
| Category Promotions | Boolean column we set to 1  if this category was included in `X-Gmail-Labels`.                                                                                                     |
| Category Updates    | Boolean column we set to 1 if this category was included in `X-Gmail-Labels`.                                                                                                      |
| Inbox               | Boolean column we set to 1  if this category was included in `X-Gmail-Labels`.                                                                                                     |
| Spam                | Boolean column we set to 1  if this category was included in `X-Gmail-Labels`.                                                                                                     |
| Primary             | Boolean column we set to 1  if "Inbox" is in `X-Gmail-Labels`, but not "Category Promotions", "Spam", or "Trash".                                                                  |
| From_Email          | The email address used to send us an email. Cleaned up from mbox metadata.                                                                                                         |
| From_Domain         | The domain of the email address used to send us an email.<br>Cleaned up from mbox metadata.                                                                                        |
| From_Name           | The name associated with the email address used to send us an email.<br>Cleaned up from mbox metadata.                                                                             |
| To_Email            | The email alias that a sender delivered an email to.<br>Also cleaned up from mbox metadata.                                                                                        |
| Name                | The name of the poltician or organization who we signed up for using our custom email alias.<br>Joined from `data/input/newsletter_categories.csv`, as are the last three columns. |
| Website             | Same field described in `data/input/newsletter_categories.csv`.                                                                                                                    |
| Category            | Same field described in `data/input/newsletter_categories.csv`.                                                                                                                    |
| Entity_ID           | Same field described in `data/input/newsletter_categories.csv`.                                                                                                                    |

Links: [Formatted](https://github.com/the-markup/investigation-wheres-my-email/blob/master/data/intermediates/email_metadata_merged_with_newsletters.csv.gz) | [Raw](https://github.com/the-markup/investigation-wheres-my-email/blob/master/data/intermediates/email_metadata_merged_with_newsletters.csv.gz?raw=true)

<hr>

## Notebooks
Follow the numeric prefix for the correct order of running each Jupyter notebook. Sometimes we use custom functions located in the `utils/` folder.

#### 0-intro-to-the-story.ipynb
This notebook reproduces the timeseries of Gmail open rates compared to non-Gmail open rates for several advocacy organizations plus Change.org, who sent us data. This is the tip that our story and experiment are based off of.

Links: [Github](https://github.com/the-markup/investigation-wheres-my-email/blob/master/notebooks/0-intro-to-the-story.ipynb) | [nbviewer](https://nbviewer.jupyter.org/github/the-markup/investigation-wheres-my-email/blob/master/notebooks/0-intro-to-the-story.ipynb)

#### 1-data-preprocessing.ipynb
This notebook walks through preprocessing and cleaning the mbox data we collected using our model Gmail account, and merging that data with `data/input/newsletter_categories.csv` to trace each email to the entity we originally signed up for.

Links: [Github](https://github.com/the-markup/investigation-wheres-my-email/blob/master/notebooks/1-data-preprocessing.ipynb) | [nbviewer](https://nbviewer.jupyter.org/github/the-markup/investigation-wheres-my-email/blob/master/notebooks/1-data-preprocessing.ipynb)

#### 2-analysis.ipynb
This notebook reproduces tables featured in our story and paper describing the experiment. This is where all the files in `data/output/` are generated.

Links: [Github](https://github.com/the-markup/investigation-wheres-my-email/blob/master/notebooks/2-analysis.ipynb) | [nbviewer](https://nbviewer.jupyter.org/github/the-markup/investigation-wheres-my-email/blob/master/notebooks/2-analysis.ipynb)


## Licensing
Copyright 2020, The Markup News Inc.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.