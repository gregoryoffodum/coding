import pandas as pd
from os import path, listdir

def coding_exercise():
# create a list to store final results for each json file
    output = []

    # specify directory/path of json files
    json_dir = '.'
    json_files = [file for file in listdir(json_dir) if file.endswith(".json")]

    # loop through each json file
    for json_file in json_files:
        #  open, read as pandas dataframe and close file automatically
        try:
            with open(path.join(json_dir, json_file), 'r') as file:
                data = pd.read_json(json_file)
                data = data.rename_axis("vendor").reset_index()
        # Questions
                #1. Format the date fields in UTC for selected columns
                date_columns = ['scan_date', 'first_seen', 'last_seen']
                for col in date_columns:
                    data[col] = pd.to_datetime(data[col], utc=True)
        #             data[col] = data[col].apply(lambda x: round(int(x.timestamp())/(3600*24)))

                #2. Calculate the days between scan and first_seen, scan and last_seen
                data['days_btw_scan_first_seen'] = (data['scan_date'] - data['first_seen']).dt.days
                data['days_btw_scan_last_seen'] = (data['scan_date'] - data['last_seen']).dt.days

                #3. Select scans for traditional_vendors
                traditional_vendors = ['Microsoft', 'Symantec', 'BitDefender', 'McAfee']
                scans = data[data['vendor'].isin(traditional_vendors)]

                #4. count number of scans detected for the traditional vendors
                scans_detected = scans[scans['scans'].apply(lambda x: x.get('detected')) == True]
                count_scans_detected = len(scans_detected)

                #5. Calculate which vendors agree the most
                vendor_details = scans.groupby('vendor')['scans']\
                                    .apply(lambda x: x.apply(lambda y: y.get('detected')).sum())
                list_vendor_max_detected = vendor_details[vendor_details == vendor_details.max()].index.tolist()

                # Append the results to the output list
                output.append({
                    'File': json_file,
                    'Days btw scan and first seen': data[['vendor', 'days_btw_scan_first_seen']].head(),
                    'Days btw scan and last seen': data[['vendor', 'days_btw_scan_last_seen']].head(),
                    'Detected Scans Count': count_scans_detected,
                    'Vendor Most Agreed': list_vendor_max_detected
                })

        except Exception as e:
            print(f"Error reading {json_file}: {str(e)}")
    # view output
    for result in output:
        print('File:', result['File'])
        print('************************')
        print('Days between Scan and First Seen:')
        print(result['Days btw scan and first seen'])
        print('-------------------------')
        print('Days between Scan vs. First Seen:')
        print(result['Days btw scan and last seen'])
        print('-------------------------')
        print('Number of scans detected:', result['Detected Scans Count'])
        print('Vendor Most Agreed:', list_vendor_max_detected)
        print(result['Vendor Most Agreed'])
        print('\n')

coding_exercise()
