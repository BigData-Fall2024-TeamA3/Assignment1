# Assignment1

### TBD
- [ ] Check with deliverables
- [ ] Add to do list for each and update issues page
- [ ] Lock main branch (niv)

# TO DO
- [ ] Setup
    - [ ] Preprocessing data and Migration script for s3 - Niv
    - [ ] Mock DB for visualization - Niv
    - [ ] DB design validation 
- [x] Set up template Streamlit app - Niv
- [ ] Workflow 
    - [ ] Diagrams (Lucid chart) - Deepak
    - [ ] Pages
        - [ ] Sign up / Login Page (to maintain unique instance) - Extra
        - [ ] (Landing page) Validation test selection page
        - [ ] Validation case page
- [ ] Skeleton Diagrams
    - [ ] Update Task List - Mau
- [ ] StreamLit functionalities
    - [ ] Skeleton APIs (Streamlit)
        - [ ] "Amazon S3 / snowflake" + "ORM" - Niv 
        - [x] "LLM" - Deepak 
        - [ ] Functionality 1: A user would select a specific test case available from the validation test file
    - [ ] Deployment with streamlit env
    - 
    (metadata.jsonl) (Logic) - Niv
- [ ] Visualization - Deepak
- [ ] Deployment: Deploy the streamlit app on the Streamlit public cloud

# Ref
2. A user would select a specific test case available from the validation test file
(metadata.jsonl)
3. You should design a system to send the context data and question to OpenAI model
to answer it for you.
4. Give an option to user to compare the answer from OpenAI model to the final
answer from the metadata file, if the answer from the OpenAI model is incorrect,
you should give option to user to modify the Annotator steps present in the
Metadata file and evaluate the Model again. (Note: Review the steps and ensure
you are not giving away the answer to the model)
5. Record the feedback/response of user on each evaluation which user perform and
generate the reports and visualization [4] for the results on streamlit applications.

# Deliverables
1. GitHub Repo Link with
    a. Diagrams
    b. A fully documented codelabs
    c. Video of the submission (5 minutes)
    d. Link to working application
    e. GitHub project

2. Checklist
    1. Required attestation and contribution declaration on the GitHub page:
    ```
        WE ATTEST THAT WE HAVEN’T USED ANY OTHER STUDENTS’ WORK IN OUR
        ASSIGNMENT AND ABIDE BY THE POLICIES LISTED IN THE STUDENT HANDBOOK
        Contribution:
        a. member1: 33%
        b. member2: 33%
        c. member3: 33%
    ```
    2. Make sure you do not push anything to your GitHub after submission date
    3. Create a Code lab document describing everything you did. In your GitHub you
    should have a readme.md files which would tell what all things are there in this
    GitHub repository.
    4. Keep your repository private until the deadlines. In case of any plagiarism cases
    both the teams which be equally held responsible


### DO NOT PUSH TO THE MAIN BRANCH
### Procedure to push code
- (first time) create a branch with your name with "main" as base
- (Every time) Pull code from main branch before making changes to your branch
- (Every time) make changes
- (Every time) commit the changes
- (Every time) push the code to "your branch"
- (Every time) Create a PR to main with the changes

# Detailed git instructions of above
- `git checkout "name"`
    - [ ] Created "origin/deepak" for deepak
    - [ ] created "origin/aish" for aish
    - [ ] created "origin/niv" for niv
    - [ ] created "origin/backup" for backup
- `git pull origin main`
    - ALWAYS run this BEFORE YOU START WORKING ON CHANGESSSS!!!
    - Note: Work on changes in your local system
- `git add .`
- `git commit -m "What changes desc"`
    - Note: Good practice is frequent commit so that if you fuck up, you can go back to your last save/commit
    - Resource: https://www.freecodecamp.org/news/git-reverting-to-previous-commit-how-to-revert-to-last-commit/
- `git push origin <branch name>`
    - branch name is "deepak" for deepak
    - branch name is "aish" for aish
    - branch name is "niv" for niv

- Raise a PR to main and let me know :). We will merge once we talk through the changes
- LETS GOOO!

# Quickstart ref
1. https://docs.streamlit.io/develop/tutorials/databases/aws-s3
2. https://docs.streamlit.io/develop/tutorials/multipage
3. https://docs.streamlit.io/develop/api-reference/charts/st.plotly_chart


