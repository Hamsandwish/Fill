import cv2
import pandas as pd
from pyzbar.pyzbar import decode
import os
import subprocess

# Read the database
database = pd.read_csv('database.csv')

# Initialize the camera
cap = cv2.VideoCapture(0)

while True:

    x = input('Press enter for New Scan')
    
    ret, frame = cap.read()

    # Decode QR codes
    decoded_qrs = decode(frame)

    for qr in decoded_qrs:
        id = qr.data.decode('utf-8')
        print(f'Decoded ID: {id}')

        row_number = database[database['A'] == id].index
        print(row_number)
        # Search for the ID in the database
        row = database.loc[database['A'] == id]

        if not row.empty:
            print('Attended')
            database.loc[database['A'] == id, 'C'] = 'Present'
            

            # Save the updated database
            database.to_csv('database.csv', index=False)

            # Open and print the PDF
            pdf_path = f'C:\\Users\\user\\Desktop\\AfroMine\\Scanner\\u\\{id}.pdf'
            if os.path.exists(pdf_path):
                # Open and print the PDF
                command = f'"{pdf_path}"'
                subprocess.run(command, shell=True)
            else:
                print('PDF not found')

        else:
            print('Not Founded')


    # Display the camera feed
    cv2.imshow('QR Scanner', frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        

        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()