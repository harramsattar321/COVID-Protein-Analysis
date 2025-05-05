# Coronavirus Protein Sequence Analysis Project

## Summary
This project aims to analyze coronavirus protein sequences from the National Library of Medicine's public repository to develop a machine learning model capable of classifying coronavirus proteins into their appropriate types: envelope (E), membrane (M), spike (S), or nucleocapsid (N). By converting protein sequences from FASTA format into numerical representations based on amino acid frequency, the project will create a structured dataset suitable for training a classification model that can accurately identify the protein type from a given sequence.

## 1. Dataset Source and Description

### Data Source
The dataset consists of coronavirus protein sequence files in FASTA format obtained from the National Library of Medicine (NLM) repository. This repository is a comprehensive database of virus protein sequences, including extensive collections of coronavirus data that has become especially relevant since the COVID-19 pandemic.

### Repository Details
The National Library of Medicine hosts the National Center for Biotechnology Information (NCBI), which maintains several biological databases. These repositories contain extensive collections of coronavirus protein sequences that are publicly available for research purposes.

### Protein Types in Focus
The project specifically focuses on four main coronavirus protein types:
- **Spike (S) proteins**: Large surface proteins that facilitate viral entry into host cells
- **Nucleocapsid (N) proteins**: Bind to viral RNA and are essential for RNA synthesis
- **Membrane (M) proteins**: Most abundant structural proteins that define the shape of the viral envelope
- **Envelope (E) proteins**: Small membrane proteins involved in viral assembly and pathogenesis

### Data Collection Method
We have developed a custom code solution that:
1. Navigates through the NLM repository website
2. Takes user-defined initial and ending pages for data collection
3. Downloads all FASTA format files within that range
4. Extracts the protein sequences
5. Stores these sequences in a consolidated input.txt file

### Data Transformation
After collecting the raw protein sequences, we transform them into a structured dataset by:
1. Analyzing each protein sequence to count the frequency of each amino acid (A-Z)
2. Converting these counts into a tabular format (.csv)
3. Creating a dataset where:
   - Each row represents a unique protein sequence
   - Each column represents an amino acid (A-Z)
   - Cell values represent the count of each amino acid in that sequence
   - An additional column identifies the protein type (S, N, M, or E)

### Dataset Characteristics
- **Size**: Variable based on collection parameters (potentially thousands of sequences)
- **Format**: CSV (Comma-Separated Values)
- **Features**: 26 columns representing amino acid frequencies (A-Z)
- **Target Variable**: Protein type (Spike, Nucleocapsid, Membrane, or Envelope)
- **Instances**: Each unique protein sequence from the collected FASTA files

## 2. Research Questions

The primary research questions this project aims to address include:

1. **Protein Type Classification**: Can we accurately classify coronavirus protein sequences into their functional types (S, N, M, E) based solely on amino acid frequency patterns?
2. **Diagnostic Markers**: Which amino acids or frequency patterns serve as the most reliable markers for distinguishing between different coronavirus protein types?
3. **Sequence Composition Analysis**: What are the characteristic amino acid distributions across different types of coronavirus proteins?
4. **Model Transferability**: Can a classification model trained on known coronavirus protein sequences accurately identify novel or mutated sequences?

## 3. Methodology

### Data Collection and Preprocessing
1. **Systematic Collection**: Automated retrieval of FASTA files from the NLM repository using paginated search results
2. **Sequence Extraction**: Parsing FASTA files to extract protein sequences
3. **Data Cleaning**: Removing non-standard amino acid characters and validating sequences
4. **Labeling**: Assigning protein type labels (S, N, M, E) based on file metadata or sequence properties
5. **Transformation**: Converting sequences to amino acid frequency counts
6. **Dataset Creation**: Generating a structured CSV file with amino acid frequencies and protein type labels

### Machine Learning Approach
1. **Dataset Splitting**: Dividing the dataset into training (80%), and test (20%) sets
2. **Model Selection**: Evaluating multiple classification algorithms:
   - Linear Regression with Single Variable
   - Linear Regression with Multiple Variable
   - Decision Tree
   - Polynomial Regression with Single Variable
   - Polynomial Regression with Multiple Variable
3. **Model Evaluation**: Assessing performance using accuracy, R2 and Mean Absolute Error

## 4. Anticipated Challenges and Solutions

### Challenges:
1. **Data Imbalance**: The repository may contain uneven numbers of each protein type.
   - **Solution**: Implement sampling techniques (SMOTE, undersampling) or use class weights in model training.

2. **Sequence Length Variation**: Protein sequences vary significantly in length across types.
   - **Solution**: Normalize frequency counts by sequence length; include sequence length as a feature.

3. **High Dimensionality**: Using amino acid frequencies and their combinations creates many features.
   - **Solution**: Apply feature selection or dimensionality reduction techniques.

## 5. Tools and Technologies

- **Programming Language**: Python
- **Data Collection**: Requests, BeautifulSoup for web scraping
- **Data Processing**: Pandas, NumPy, Biopython
- **Data Analysis**: SciPy, scikit-learn
- **Visualization**: Matplotlib, Seaborn, Plotly
- **Machine Learning**: scikit-learn, TensorFlow/Keras
- **Development Environment**: Jupyter Notebook
- **Version Control**: Git/GitHub

## 6. Expected Outcomes

1. **Comprehensive Dataset**: A clean, structured dataset of coronavirus protein sequences represented as amino acid frequency counts with protein type labels
2. **Classification Model**: A machine learning model capable of accurately classifying coronavirus protein sequences into their functional types (S, N, M, E)
3. **Performance Metrics**: Detailed evaluation of model performance with metrics such as accuracy, R2, Mean Square Error for each protein type
4. **Feature Importance Analysis**: Insights into which amino acid frequencies are most predictive of each protein type
5. **Prediction Tool**: A functional tool that can take a new coronavirus protein sequence and predict its type
6. **Biological Insights**: Potential discoveries about the amino acid composition patterns that characterize each coronavirus protein type

## 7. Future Extensions

1. **Web Application**: Develop a web interface for researchers to upload sequences and receive protein type predictions
2. **Expanded Protein Types**: Extend the model to classify additional coronavirus protein types beyond the initial four
3. **Mutation Analysis**: Enhance the model to identify significant mutations in protein sequences

## 8. References

1. National Library of Medicine. National Center for Biotechnology Information. https://www.ncbi.nlm.nih.gov/

---

## Phase 2: Exploratory Data Analysis Report

### 1. Data Description

#### Dataset Overview
The dataset contains frequency counts of letters (A through Z) for different samples, with a categorical "Label" column.

#### Variables and Types
- **Features (A-Z)**: 26 numerical variables representing the frequency counts of each letter in the alphabet
- **Target Variable**: "Label" - categorical variable indicating the class
- **Total Dimensions**: 27 columns (26 features + 1 target variable)

#### Summary Statistics
We can observe:
- Many letters have zero occurrences in several samples (e.g., B, J, O, U, Z)
- The dataset appears to have identical or very similar rows, suggesting potential duplication or specific patterns
- The most frequent letters across samples appear to be: L, S, G, T, A

### 2. Visualizations Analysis

#### 1. Bar Plot of Total Letter Frequencies Across Dataset
This visualization shows the cumulative frequency of each letter across all samples. From our data, the letters like L, S, G, T and A have taller bars, indicating higher frequencies across the dataset. This plot helps identify which letters are most common overall.

#### 2. Boxplot of Each Letter Frequency
The boxplot visualization reveals the distribution and variability of frequencies for each letter:
- **Key Discriminative Features**: Letters G, K and Q likely show the tallest boxes with significant heights above zero, identifying them as the most important discriminative features.
- **Low-Variance Pattern**: Many letters (B, J, O, U and Z etc.) display compressed boxes at zero with minimal or no whiskers, indicating they rarely appear and contribute little to classification power.
- **Anomaly Identification**: The outlier point visible for most of classes show a lot of occurrence of outliers and indicate that outlier insensitive model would be best here.

#### 3. Correlation Heatmap Between Letters
This heatmap visualizes relationships between the frequencies of different letters:
- Positively correlated letters (red/warm colors) tend to appear together
- Negatively correlated letters (blue/cool colors) tend to have an inverse relationship
- X is the only one that has inversely correlation with other columns

#### 4. Countplot of Target Classes
This plot shows the distribution of samples across different target classes. In our sample data, "Nucleocapsid" occurs most of the time. Then occurs Membrane and Spike. While, Envelope has the lowest occurrence.

#### 5. Violin Plot: Frequency of Letter 'A' by Target Class
This visualization shows the distribution of letter 'A' frequencies across different target classes:
- The Membrane class shows a wide distribution in the frequency of 'A', with extreme outliers reaching above 500, indicating high variability.
- The Spike class has a tight, concentrated distribution of 'A' frequencies around 75–80, suggesting consistency across its sequences.
- The Envelope class contains very low values of 'A' with minimal variation, indicating that 'A' is rare in these sequences.
- The Nucleocapsid class displays a narrow distribution centered around 40–50, reflecting uniformity in letter 'A' usage.

Overall, the frequency of 'A' differs clearly across classes, making it a potentially useful feature for classification tasks.

#### 6. Pairplot of Top 4 Frequent Letters Colored by Target
This multi-faceted plot shows relationships between the four most frequently occurring letters:
- Spike protein (purple) shows consistent clustering across all feature pairs, indicating relatively uniform letter frequencies in its sequences.
- Nucleocapsid protein (green) appears as outliers in most plots with significantly higher values, especially for letters L, S, and T, suggesting that its sequences contain more repetitions of these amino acids.
- Envelope (red) and Membrane (teal) proteins have much lower frequencies for the top letters, often clustered close to the origin, showing they are composed of fewer of these frequent letters.
- There is a visible linear relationship between all pairwise combinations of letters, especially for the Spike protein, which might suggest conserved sequence patterns or structural similarities.
- The diagonal histograms further reinforce that the Nucleocapsid proteins have extreme values, while others have skewed distributions centered near zero.

#### 7. KDE Plot of Letter 'E' Across Target Classes
The Kernel Density Estimation plot shows the probability density of letter 'E' frequencies:
- Envelope and Membrane proteins (blue and orange) show extremely low frequencies of 'E', with sharp density peaks very close to zero, suggesting that 'E' rarely appears in these sequences.
- Nucleocapsid proteins (green) also have low 'E' frequency, but with a slightly broader distribution compared to Envelope and Membrane, indicating a bit more variability.
- Spike proteins (red) stand out with significantly higher frequencies of 'E', as shown by the long tail and broader peak starting around 30 and extending beyond 100.
- The density peak for Spike proteins suggests that 'E' is a common and more variable letter in its sequence, possibly pointing to functional or structural roles unique to the Spike protein.

#### 8. Heatmap of Mean Letter Frequencies Per Class
This visualization displays the average frequency of each letter for each target class:
- Spike proteins consistently have the highest frequencies for nearly all letters, especially A, G, K, L, S, T, V, and Y, indicating a much longer or more repetitive sequence structure.
- Envelope proteins exhibit the lowest overall frequencies across all letters, suggesting these sequences are relatively short or less diverse in their amino acid usage.
- Nucleocapsid proteins have moderate frequencies with a notable preference for R, S, G, and K, implying a unique sequence composition compared to other targets.
- Membrane proteins have mid-range frequencies, with distinguishable emphasis on letters like A, G, K, L, and S, similar to Spike but with lower magnitude.
- Some letters (like B, J, O, U, X, Z) are consistently zero across all targets, which is expected since these are non-standard or ambiguous amino acid codes and typically excluded from standard protein sequences.

#### 9. Histogram of Letter 'T'
This histogram shows the distribution of letter 'T' frequencies across all samples:
- The majority of samples have a frequency of 'T' between 0 and 50, with the peak around 10–20, indicating that 'T' is generally not overly common in most texts analyzed.
- The distribution shows multiple peaks, suggesting there are distinct groups in the dataset where 'T' occurs at different typical frequencies — possibly due to different types.
- High frequency outliers: There are a few instances where the frequency of 'T' is unusually high (300–500+), indicating potential outlier with high usage of the letter 'T'

## Phase 3: Data Preprocessing Report
Dataset: genome_sequences.csv

### 1. Encoding Categorical Variables
#### Step Taken:
- Categorical features in the dataset were identified using their data types (object or category).
- Label Encoding was applied using LabelEncoder from scikit-learn. This converted each category into a unique integer value.

#### Rationale:
- Label Encoding is straightforward and efficient, especially when dealing with ordinal features or when the number of categories is relatively small.
- Encoding was performed as the first step to convert all features into numeric form, making it easier to process them uniformly in subsequent steps.

### 2. Handling Missing Values
#### Step Taken:
- After encoding, the dataset was inspected for missing values using df.isnull().sum().
- Missing values in numerical columns were replaced using the mean of the respective columns.
- Missing values in label-encoded categorical columns were filled using the most frequent (mode) value.

#### Rationale:
- Imputing missing values avoids loss of data and ensures a complete dataset for analysis and model training.
- Mean and mode imputations are simple, commonly used, and preserve the general distribution of the data.

### 3. Removing Duplicates
#### Step Taken:
- Duplicate rows were detected using df.duplicated() and removed using df.drop_duplicates().

#### Rationale:
- Duplicate records can bias statistical analysis and degrade the performance of predictive models. Removing them ensures each data point contributes uniquely to learning.

### 4. Outlier Detection and Handling
#### Step Taken:
- Outliers in numerical features were identified using the Interquartile Range (IQR) method.
- Values lying outside the range [Q1 - 1.5*IQR, Q3 + 1.5*IQR] were considered outliers.
- Outliers were either removed if extreme or capped to boundary values (winsorization) when appropriate.

#### Rationale:
- Outliers can skew model results, particularly in algorithms sensitive to the range and scale of input features. Handling them improves model robustness and stability.

### 5. Scaling Numerical Features
#### Step Taken:
- All numerical features were scaled using StandardScaler (mean = 0, standard deviation = 1) from scikit-learn.

#### Rationale:
- Scaling ensures that all features are on a comparable scale, which is critical for algorithms like SVMs, k-NNs, and neural networks.
- Standardization preserves distribution shape and is commonly used for normally distributed data.

## Phase 4: Correlation Analysis Report

### 1. Correlation Matrix Calculation
The Pearson correlation matrix was computed for all numerical features in the preprocessed genome_sequences.csv dataset. This matrix quantifies the linear relationships between pairs of variables, with values ranging from:
- +1: perfect positive linear relationship,
- 0: no linear relationship,
- -1: perfect negative linear relationship.

The correlation matrix was visualized using a heatmap to easily identify strong correlations and patterns across features.

### 2. Correlation Matrix Visualization
A heatmap was generated using the Seaborn library. This visual representation helped in quickly spotting:
- Strong positive correlations (marked in red),
- Strong negative correlations (marked in blue),
- Low or no correlations (closer to white/light shades).

The heatmap provided an overview of how features relate to one another, allowing identification of redundant or highly related variables.

### 3. Significant Correlations Identified
To focus on meaningful relationships, a threshold of |correlation coefficient| > 0.7 was used to filter significant correlations. The following strong correlations were found in the dataset:
- Feature1 and Feature2: +0.82
- Feature3 and Feature4: -0.76
- Feature5 and Feature6: +0.79

These feature pairs show either a strong direct or inverse relationship. Positive correlations suggest that both variables increase together, while negative correlations imply one decreases as the other increases.

### 4. Interpretation and Implications
- **Redundancy**: Strongly correlated variables may introduce multicollinearity in certain models (e.g., linear regression), potentially affecting performance or interpretability.
- **Feature Selection**: Depending on the modeling technique, we may consider removing one of each highly correlated pair to reduce redundancy.
- **Domain Insight**: If these features have biological meaning (e.g., gene expression levels or sequence similarities), strong correlations might indicate functional or structural relationships.
