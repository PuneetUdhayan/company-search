# company-search

Service to provide URLs for companies.

## Requirements:

Python 3.8.3 

## Setup

1. Install the required libraries by running `pip install -r requirements` from root folder of the repository

2. Run the following command to start the server `uvicorn app.main:app`

## Usage

1. Open the swagger docs

Visit the URL

```
http://localhost:8000/docs
```

this will lead to the swagger documentation

2. Upload file

Use the endopint __/companies-search/upload-file/__ to upload a file.

This can done on swagger docs by expanding the endponit and clicking try it out on the top right.

This endpoint will return a *dataset_id* for your file in the response body. This dataset_id will be used to retrieve results.

3. Retreive results

Use the endpoint __/companies-search/get-results/{datset_id}__ to fetch the results.

Use the try it functionality of swagger to provide the dataset ID of your file. 
If the dataset is still processing, you will be given a response status as the response body.
If the dataset processing has completed, a download link will be provided. Please use this link to download results.

If there was any error in processing your reqquests, an error_message will be displayed in the response body, else this field will be blank.



