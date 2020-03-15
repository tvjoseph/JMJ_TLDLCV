'''
JMJPFU
15-Mar-2020
This is the script for transfer learning
Lord bless this attempt of yours
'''

import h5py
import os

# Defining the class for HDF5 writer

class HDF5DatasetWriter:
    def __init__(self,dims,outputPath,dataKey='images',bufSize=1000):
        # Check if the output path exists and if so raise an exception
        if os.path.exists(outputPath):
            raise ValueError("The supplied 'outputPath' already exist and cannot be overwritten. Manually delete the file before continuing", outputPath)

            # Open the HDF5 database for writing and create two data sets, one to store the labels and the other to store class labels
        self.db = h5py.File(outputPath,'w')
        self.data = self.db.create_dataset(dataKey,dims,dtype='float')
        self.labels = self.db.create_dataset('labels',(dims[0],),dtype='int')

        # Store the buffer sizes and initialize the buffer along with the index into the datasets
        self.bufSize = bufSize
        self.buffer = {'data': [],'labels': []}
        self.idx = 0

    # Defining the add method to write data to buffer
    def add(self,rows,labels):
        # Add rows and labels to the buffer
        self.buffer['data'].extend(rows)
        self.buffer['labels'].extend(labels)
        # Check if the buffer size to be flushed to disk
        if len(self.buffer['data']) >= self.bufSize:
            self.flush()

    # Defining the function for flush which writes the buffer to disk and reset the buffer

    def flush(self):
        i = self.idx + len(self.buffer['data'])
        self.data[self.idx:i] = self.buffer['data']
        self.labels[self.idx:i] = self.buffer['labels']
        self.idx = i
        self.buffer = {'data': [], 'labels': []}

    def storeClassLabels(self,classLabels):
        # Create a data set to store the actual class labels
        dt = h5py.special_dtype(vlen = unicode)
        labelSet = self.db.create_dataset('label_names',(len(classLabels),),dtype = dt)
        labelSet[:] = classLabels

    # Method to close the operations

    def close(self):
        # Checking to see if there are any entries in the buffer
        if len(self.buffer['data']) > 0:
            self.flush()

        # Close the dataset
        self.db.close()