import React, { useEffect, useState } from 'react'
import { GoogleMap, LoadScript, Marker,  InfoWindow  } from '@react-google-maps/api';
import { jsPDF } from 'jspdf';
import 'jspdf-autotable'; 
import Navigation from '../components/nav/Navigation'
import Footer from '../components/footer/Footer'
import IssuesService from '../services/Issues.service';
import Button from 'react-bootstrap/Button';

function MapWindow() {
  const [issues, setIssues] = useState([])
  const [selectedIssue, setSelectedIssue] = useState(null);

  const mapStyles = {
    height: '100vh',
    width: '100%'
  };

  const defaultCenter = {
    lat: 7.8731, lng: 80.7718
  };

  const loadIssues = async () => {
    await IssuesService.getIssues().then((data) => {
      console.log(data)
      setIssues(data)
    })
  }

  const generateReport = () => {
    // Create a new PDF document
    const doc = new jsPDF();

    // Define table headers
    const headers = [['Title', 'Description', 'Status']];

    // Extract issue data for the table
    const tableData = issues.map((issue) => [issue.title, issue.description, issue.status]);

    // Add table headers and data to the PDF document using jspdf-autotable plugin
    doc.autoTable({ head: headers, body: tableData });

    // Save the PDF
    doc.save('issues_report.pdf');
  };

  useEffect(() => {
    loadIssues()
  }, [])

  return (
    <div>
        <Navigation />

        {/* Generate Report */}
        <div className='options-container'>
          <h5>Generate Reports</h5>
          <Button variant="info" onClick={() => generateReport()}>
              Generate PDF
          </Button>
        </div>
        

        {/* Map Container */}
        <LoadScript googleMapsApiKey={'AIzaSyDAsJYZSQ92_NQAz9kiSpW1XpyuCxRl_uI'}>
          <GoogleMap
            mapContainerStyle={mapStyles}
            zoom={10}
            center={defaultCenter}
          >
            {/* <Marker position={defaultCenter} /> */}
            {issues.map((issue) => (
            <Marker
              key={issue._id}
              position={issue.location}
              onClick={() => setSelectedIssue(issue)}
            />
          ))}

            {selectedIssue && (
              <InfoWindow
                position={selectedIssue.location}
                onCloseClick={() => setSelectedIssue(null)}
              >
                <div style={{ maxWidth: '200px' }}>
                  <img
                    src={selectedIssue.image}
                    alt="Issue Thumbnail"
                    style={{ width: '100px', height: 'auto', marginRight: '10px' }}
                  />
                  <h3>{selectedIssue.title}</h3>
                  <p>{selectedIssue.description}</p>
                  <p>Status: {selectedIssue.status}</p>
                </div>
              </InfoWindow>
            )}
          </GoogleMap>
        </LoadScript>

        <Footer />
    </div>
  )
}

export default MapWindow