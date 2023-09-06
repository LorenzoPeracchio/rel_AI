Usage
=====

.. _installation:

Installation
------------

To use Rel-AI, first make sure you have the latest version of pip installed

.. code-block:: console

   (.venv) $ pip install --upgrade pip

Then install it using pip:

.. code-block:: console

   (.venv) $ python -m pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple ReliabilityPackage 


Usage
----------------

Here's a simple example of usage of the ``RelAI`` with the ``breast_cancer`` dataset of ``sklearn``.


1. import the needed functions from the package


.. code-block:: console 

   from ReliabilityPackage.ReliabilityFunctions import *


2. Import all the other relevant packages

.. code-block:: console 

   import numpy as np
   from sklearn import datasets
   from sklearn.model_selection import train_test_split
   from sklearn.ensemble import RandomForestClassifier
   import plotly.offline as pyo

3. load the breast cancer dataset and split it in a training, a validation, and a test set

.. code-block:: console 

   X, y = datasets.load_breast_cancer(return_X_y=True)
   X_seventy, X_test, y_seventy, y_test = train_test_split(X, y, test_size=0.30, random_state=42)
   X_train, X_val, y_train, y_val = train_test_split(X_seventy, y_seventy, test_size=0.30, random_state=42)

4. Train a classifier on the training set

.. code-block:: console 

   clf = RandomForestClassifier(random_state=42, min_samples_leaf=10, n_estimators=100)
   clf.fit(X_train, y_train)

5. Create and train an autoencoder for the implementation of the Density Principle
(Please note that if the layer_sizes are not specified, the default autoencoder is built as follows: [dim_input, dim_input + 4, dim_input + 8, dim_input + 16, dim_input + 32];
if needed, specify a more suitable architecture)

.. code-block:: console

      ae = create_and_train_autoencoder(X_train, X_val, batchsize=80, epochs=1000)

6. Generate the dataset of the synthetic points and their associated values of accuracy

.. code-block:: console

      syn_pts, acc_syn_pts = generate_synthetic_points(clf.predict, X_train, y_train, method="GN", k = 5)

7. Define a Mean Squared Error threshold and an Accuracy threshold
(the ``mse_threshold_plot`` can be generated to see how the performances change based on percentiles of the MSE of the validation set)

.. code-block:: console

   fig_mse_thresh = mse_threshold_plot(ae, X_val, y_val, clf.predict, metric = 'balanced_accuracy')
   fig_mse_thresh.show()

   mse_thresh = perc_mse_threshold(ae, X_val, perc=95)
   acc_thresh = 0.90


8. Generate an instance of the ReliabilityDetector class

.. code-block:: console

   RD = create_reliability_detector(ae, syn_pts, acc_syn_pts, mse_thresh=mse_thresh, acc_thresh=acc_thresh, proxy_model="MLP")

9. It is now possible to compute the Reliability of the test_set

.. code-block:: 
   
   test_reliability= compute_dataset_reliability(RD, X_test, mode='total')
   reliable_test = X_test[np.where(test_reliability == 1)]
   unreliable_test = X_test[np.where(test_reliability == 0)]
