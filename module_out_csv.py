import os
import csv


def write_local_csv(filename, write_data):
    # Check if file exists
    if os.path.isfile(filename):
        mode = 'a'  # Append mode
    else:
        mode = 'w'  # Write mode
    try:
        # Open file in appropriate mode
        with open(filename, mode, newline='') as csvfile:
            # Create a csv writer object
            writer = csv.writer(csvfile)

            # If file is empty, write header row
            if mode == 'w':
                writer.writerow(['LEAD', 'DEAL_TYPE', 'CONTACT_NAME',
                                 'CONTACT_INFO', 'PROPERTY_TYPE', 'PROPERTY_SIZE',
                                 'PROPERTY_LOCATION', 'BUDGET', 'EMAIL_DRAFT'])

            # Write data rows
            writer.writerow([write_data.get('LEAD'), write_data.get('DEAL_TYPE'), write_data.get('CONTACT_NAME'),
                             write_data.get('CONTACT_INFO'), write_data.get('PROPERTY_TYPE'), write_data.get('PROPERTY_SIZE'),
                             write_data.get('PROPERTY_LOCATION'), write_data.get('BUDGET'), write_data.get('EMAIL_DRAFT')])
    except:
        return -1
    return 1