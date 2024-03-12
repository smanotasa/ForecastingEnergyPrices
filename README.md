# Predictive Modeling for Day-Ahead Pricing in Electricity Markets
- Presented by Sam Minors and Santiago Manotas-Arroyave in partial fulfillment of the MSc. in Data Science @ BSE, 2023.

The PDF report provides a comprehensive overview of the use of machine learning and deep learning methodologies in predicting spot prices in liberalized electricity markets, with a focus on the Colombian wholesale energy market; it pprovides a tool for assessing pricing power and price forecasting for possible anomalies.

## Abstract
The literature review highlights the limitations of traditional inferential statistical methods and emphasizes the necessity for more sophisticated techniques to capture the complexities and non-linearities inherent in electricity markets. The study’s findings underscore the need for ongoing research in this domain and offer a comprehensive understanding of the field, constructing a robust foundation for a more profound comprehension of the multifaceted dynamics of energy markets and allowing for the envisioning of potential market trajectories in the face of emerging technologies and methodologies. Overall, this study provides valuable insights into the potential for predictive modeling to improve decision-making in the Colombian energy market and beyond; as well as providing exhaustive metrics for out-of-sample architecture comparison.

## Overview of Sections
- **Introduction:** Provides an overview of the study's objectives and motivation, as well as an introduction to the Colombian energy market and the use of predictive modeling in electricity markets.
- **Literature Review:** Highlights the limitations of traditional inferential statistical methods and emphasizes the necessity for more sophisticated techniques to capture the complexities and non-linearities inherent in electricity markets.
- **Methodology:** Describes the study's methodological framework, including data collection and preprocessing, market concentration indicators, and model selection.
- **Data**: Does a comprehensive review of publicly available data used in the project.
- **Results:** Presents the study's findings, including the performance of 4 machine learning archetypes in predicting spot prices in the Colombian energy market.
    - **Discussion:** This subsection discusses the implications of the study's findings for improving decision-making in the Colombian energy market and beyond, as well as potential avenues for future research.
- **Conclusion:** Summarizes the study's main findings and contributions, as well as its limitations and potential for future research.

Our most relevant result is the out-of-sample metrics comparing the models we've set out to concur:
| Model          | RMSE     | MAE     | sMAPE(0-200) | R-squared |
|----------------|----------|---------|--------------|-----------|
| Overlap RNN    | 0.1327   | 0.0854  | 11.8221%     | 0.9316    |
| Non-overlap RNN| 0.1361   | 0.0865  | 12.0120%     | 0.9281    |
| ARIMA(5,1,3)   | 0.2065   | 0.0590  | 19.6500%     | 0.9205    |
| AR(1)          | 0.2175   | 0.0619  | 29.2700%     | 0.9118    |

## Acknowledgements
We thank our supervisors for support and commentaries through the development of this research:
- Elliot Gaston Motte
- Hannes Müller
- Christian Brownlees

## Structure repository

- In the folder `src` you can find all the functions used for calculating metrics, graphing, processing data, as well as recurrent functions.
- In the folder `code` you can find the different notebooks used by stages of our project. **Disclaimer**: the results are not perfectly reproduceable due to the set-up of some models.

## Data
The final data `fulldata.csv` contains all variables ever used within the study, the file is considerably large. This is the case for many files given the time granularity, data is available in their respective drives as found in `.md` files in their directories.

