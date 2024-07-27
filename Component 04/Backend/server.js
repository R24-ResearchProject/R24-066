const express = require('express');
const fs = require('fs');
const path = require('path');
const { stringify } = require('csv-stringify');
const http = require('http');

const app = express();
const PORT = process.env.PORT || 30000;

// Middleware to parse JSON bodies
app.use(express.json());

// Define the path to your CSV file
const csvFilePath = path.join(__dirname, 'Dataset', '/Users/minu/Desktop/R24-066/Component 04/Backend/Dataset/worker_defect_production_data_test.csv');

// CSV headers
const csvHeaders = ['Worker_ID', 'Date', 'Run_Off', 'Open_Seam', 'SPI_Errors', 'High_Low', 'Production_Volume', 'Shift', 'defect_count', 'count'];

// Function to append data to the existing CSV file
function appendDataToCSV(data) {
    // Validate Worker ID format
    if (!/^W_\d{5}$/.test(data.workerId)) {
        throw new Error('Invalid Worker ID format');
    }

    // Map data to the CSV headers format
    const newData = {
        Worker_ID: data.workerId,
        Date: data.date,
        Run_Off: data.defect1,
        Open_Seam: data.defect2,
        SPI_Errors: data.defect3,
        High_Low: data.defect4,
        Production_Volume: data.productionVolume,
        Shift: data.shift,
        defect_count: data.defect_count,
        count: data.count,
    };

    const records = [newData];

    try {
        // Append to existing file or create new with headers if not exists
        if (!fs.existsSync(csvFilePath)) {
            console.log('CSV file does not exist, creating new one with headers.');
            stringify(records, { header: true, columns: csvHeaders }, (err, output) => {
                if (err) throw err;
                fs.writeFileSync(csvFilePath, output, 'utf-8');
            });
        } else {
            console.log('Appending data to existing CSV file.');
            stringify(records, { header: false }, (err, output) => {
                if (err) throw err;
                fs.appendFileSync(csvFilePath, output, 'utf-8');
            });
        }
    } catch (err) {
        console.error('Error during CSV processing:', err);
        throw err;
    }
}

// Route to handle form submissions
app.post('/api/saveData', (req, res) => {
    console.log('Received data:', req.body);
    try {
        appendDataToCSV(req.body);
        res.status(200).json({ message: 'Data saved successfully!' });
    } catch (error) {
        console.error('Error saving data:', error.message);
        res.status(500).json({ message: 'Error saving data', error: error.message });
    }
});

// Create the HTTP server and listen on the specified port
const server = http.createServer(app);

server.listen(PORT, '0.0.0.0', () => {
    console.log(`Server running on port ${PORT}`);
});

// Handle server errors, particularly EADDRINUSE
server.on('error', (err) => {
    if (err.code === 'EADDRINUSE') {
        console.error(`Port ${PORT} is already in use.`);
    } else {
        console.error(`Server error: ${err.message}`);
    }
});
