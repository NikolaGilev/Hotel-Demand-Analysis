# Findings from https://ecommons.cornell.edu/server/api/core/bitstreams/57a614a3-3998-46a7-a31c-80c2309263f8/content

## Day 1

1. 'For instance, K-NN outperforms advance booking models by recognizing patterns using full historical booking curves; Random Forest samples out the highly correlated features to avoid overfitting' - pg.14 p.2

2. 'Tse and Poon (2015) visually defined the relationship between time and ROHs at a certain week as quadratic. They break down the booking window into several segments and fit quadratic regressions separately. The week t is the predictor used to forecast the ROHs at (90-t) days before the final arrival day.' - pg.18 p.2
    
    2.1 'Results show that exponential smoothing yields the lowest error rate when predicting final room arrivals'
    
    2.2 'This research uses a daily booking data which ranges from 364 arrivals dates with a booking window of 0-28 days. The results show that Poisson mixture models outperform standard models and linear regression models.'

3. 'Even if Box-Jenkins outperformed exponential smoothing models marginally, the authors suggest that exponential smoothing might be more feasible considering its interpretability.' - pg.20 p.1

4. 'He also adds the trigonometric framework to keep track of several seasonal complexities in the hotel demand forecast. The performances are measured in 1, 2, 4, and 8 weeks horizon and different room types.' - pg.20 p.2

5. 'Many research attempts to explore the additional effect exogenous to the system, such as local events, weather change, unemployment rate, etc. Schwartz et al. (2016) include hotel competitive set’s predicted occupancy as an input of the daily occupancy forecasting. They randomly generate hotel occupancy data for the target hotel and hotels in the competitive set, and use an evolutionary algorithm to reach the lowest forecast error' - pg.21 p.1

## Day 2

1. This chapter introduces the primary methodology applied in this study and the theoretical background of the models. The models covered in this session include: 
    1) Advance booking models (Additive and Multiplicative); 
    2) Regression models; 
    3) Machine learning models (K-NN, weighted K-NN, Decision Tree, Random Forest, SVM, and Neural Network). - pg.23 p.1

2. Pick-up Models, also widely known as advance booking models, use the accumulative reservations over time for a particular stay night to predict the final arrivals. The main idea of pick-up models is using the pick-up method to estimate the increments of reservations for a future day and then aggregate these increments to obtain a forecast of the total arrivals (Zakhary et al., 2008). - pg.23 p.2

3. Different from additive models, multiplicative pick-up models regard the ROH as a certain ratio of the final arrivals. In this case, the final arrival on a future date t is calculated by Ri PRi where the PRi is the average of the ratio of ROH to the final arrival on i days before arrival. -pg. 24. p.3

4. 

https://www.altexsoft.com/glossary/booking-window/



# Clustering Techniques:
1. Hierarchical Clustering:
Hierarchical clustering builds a tree-like structure of clusters, allowing you to explore different levels of granularity in the clustering results.

2. DBSCAN (Density-Based Spatial Clustering of Applications with Noise):
DBSCAN is effective for clusters of varying shapes and densities. It identifies core samples and expands clusters based on density.

3. Agglomerative Clustering with Ward's Method:
Agglomerative clustering with Ward's linkage method minimizes the sum of squared differences within all clusters. It is commonly used for Euclidean distance-based clustering.

4. Optimal Clustering Evaluation:
Use silhouette analysis or Davies-Bouldin index to evaluate the quality of clustering results and determine the optimal number of clusters.

# Regression Techniques:
1. Polynomial Regression:
Polynomial regression extends linear regression by introducing polynomial features. It can capture non-linear relationships between features and the target variable.

2. Regularized Regression (Lasso, Ridge, Elastic Net):
Regularization techniques penalize large coefficients to prevent overfitting. Lasso (L1 regularization) and Ridge (L2 regularization) are common options.

3. Random Forest Regression: 
Random Forest Regression is an ensemble method that combines multiple decision trees to improve predictive accuracy and handle complex relationships.

4. Gradient Boosting Regression:
Gradient Boosting builds an ensemble of weak learners sequentially, with each learner correcting errors made by the previous ones. XGBoost and LightGBM are popular implementations.

# Classification Techniques:

1. Random Forest Classification:
Random Forest Classification is an ensemble method that combines multiple decision trees for classification tasks. It's robust and handles non-linear relationships well.

2. Support Vector Machines (SVM):
SVM is effective for binary and multi-class classification. It finds the hyperplane that maximizes the margin between classes.

3. K-Nearest Neighbors (KNN):
KNN classifies data points based on the majority class of their k-nearest neighbors. It's simple and effective, but sensitive to the choice of k.

4. Ensemble Methods (AdaBoost, Gradient Boosting, Voting Classifier):
Ensemble methods combine multiple classifiers to improve overall performance. AdaBoost and Gradient Boosting are popular boosting techniques.

5. Neural Networks:
Deep learning models, such as neural networks, can be used for complex classification tasks. They automatically learn hierarchical features from the data.



These techniques provide a broad range of options for tackling different aspects of clustering, regression, and classification problems.





