# Ask Parallel Works

This repository contains the source code for the Ask Parallel Works platform, which allows users to utilize an AI-assistant interface, built using GPT-3.5-turbo and Streamlit, to help customers use and navigate the Parallel Works platform.

This project uses the Natural Language Processing (NLP) Word2Vec and Term Frequency-Inverse Document Frequency (TF-IDF) Machine Learning models to conduct a full Semantic Search of the Parallel Works documentation found [here](https://docs.parallel.works/).

The code then retrieves the most relevant documents from Parallel Works Documentation, summarizes them, and returns them to you for your convenience. It will also provide direct links to the aformentioned pages, should you like to read the relevant pages yourself.

### Instructions

There are two ways of using this interface:

#### Option 1 (Recommended): Use the DVC Wrapper workflow to run Ask PW on the Parallel Works platform

To run Ask PW on the Parallel Works platform, please follow these instructions:

1. Login to your account on the Parallel Works platform.
2. Run the `DVC Wrapper` workflow; you will be brought to an interface. Enter the following:
    1. Select the activate resource you would like to use to run `Ask PW`.
    2. Under `Repository Name`, enter `pw-semantic-search`.
    3. Under `Github Username`, enter `abarnea`.
    4. Under `DVC Remote Storage Name`, enter `storage`.
    5. Under `ML Model Setting`, select `Run Script`.
        - If, for some reason, you would like to re-train the Ask PW ML models, you would instead select `Train Model` and skip Step 6.
            - Note that you would require `push` access to the PW `demoworkflows-bucket` remote cloud storage bucket.
        - For Ask PW, this option is run internally whenever the Parallel Works Documentation is updated in order to keep the Ask PW ML models updated for your use. The models are automatically re-trained and re-pushed to cloud storage, so that pulling the models on your end will always download the most up-to-date semantic search models.
    6. Under `Script to Run`, enter `run_app.sh`.
    7. Press `Execute` at the top right corner.
3. The workflow will now run in its entirety on your selected resource. Once it is done, you will be able to select the blue "eye" icon next to the workflow, which will open up a Streamlit UI in your web browser.**

<b>**NOTE:</b> This feature is still under construction. Currently, you are unable to open up the Streamlit UI from the Parallel Works platform.

#### Option 2 (Not Recommended): Run Ask PW on your local computer (requires cloning this repo)

To run Ask PW on your local computer, please follow these instructions:

1. Clone this repository using `git clone $URL`.
2. Set your OpenAI API Key environment variable (see `Note` below for instructions on how to do this).
3. Run `./run_app.sh`. A Streamlit UI will open up in your browser under `localhost`.
    1. For INTERNAL Use: If it is your first time running this repository and you <i>do not</i> have DVC set-up, you will need to add the flags `-t -u` <i>in that order</i> to download the Parallel Works documentation repository, and train the required models. If you are not a Parallel Works employee, this method is unavailable to you.
    2. For EXTERNAL Use: If you are not a Parallel Works employee, you must set up Data Version Control (DVC) in order to download the required Semantic Search models. The Parallel Works `demoworkflows-bucket` (<i>This needs to change to a publically accessible cloud storage bucket</i>) contains the required models. Once you have access, simply run `dvc pull`, and the models will be pulled to their required locations.
5. Enjoy!

### Note: OpenAI API Key Required for Use of this Repository

In order to run the Ask PW interface, you will need to set up your cluster or system with an OpenAI API Key environment variable. This section contains steps for setting this up.

#### Option 1: Set up your Parallel Works Cluster Bootstrap with your API Key

If you are running the Ask PW interface on the Parallel Works platform, then setting up your OpenAI API Key is very easy! All you have to do is navigate to the `Resources` tab, select the resource you would like to run Ask PW on, go to `Definitions`, and in the `User Bootstrap` section, paste the following text:
```
echo "export OPENAI_API_KEY=<Enter your key here>" >> ~/.bashrc
```
where `\<Enter your key here\>` should be replaced with your OpenAI API Key. For example, if my key is "HelloParallelWorks!", your text should look like:
```
echo "export OPENAI_API_KEY=HelloParallelWorks!" >> ~/.bashrc
```

Doing this will automatically set the `OPENAI_API_Key` environment variable to your OpenAI API Key upon resource launch every time, so you don't need to do anything else!

<i>Note:</i> This is also handy if you would like to use a `gpt` model for another project you are working on!

#### Option 2: Run the `set_api.sh` script to set your API key environment variable locally

If you would like to run the Ask PW interface locally, you can choose to run the `set_api.sh` script, which will prompt you for your API key and load it into an environment file in your local directory (called `openai_api_key.env`). This repository already ignores the file (see `.gitignore`), so it will not be pushed to Github or DVC in any way. If you choose this option, the Ask PW source code will automatically load it from your environment file, so there is nothing else you need to do after entering your API key with the script.

<i>Note 1:</i> If you choose this method, make sure you <i>never</i> share you API key with anyone.

<i>Note 2:</i> If you choose this method and you want to run Ask PW in cloud, you will need to re-set your API key each run unless you store the file in your `/contrib` directory. If you do, you will need to modify the path to the environment file in the `helper_funcs.py` script.
