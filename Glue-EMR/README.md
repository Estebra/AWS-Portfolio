# AWS Glue and EMR

Enable the trasformation and processing of large amount of data.

## Scenario

A company processes a multitude of transaction files daily which detail billing, product sold, and their quantities. This data is stored in different CSV files within S3. There’s a need to consolidate this data, analyze it and derive insights like the gross profit. You are tasked with automating the data processing and analytics pipeline using AWS Glue and EMR.

## Overview

1.Store the raw CSV data in S3 buckets
2.Use Glue Crawlers to catalog this data
3.Spin up an EWR cluster, withc we’ll use to run a PySpark script

* This script will read the data from the Glue catalog and determine the gross profit for each product sold
* Store pross profit results back into S3 for reporting

## Prerequisites

## Hands-on lesson

