import React, { useEffect, useState } from 'react';
import { Button, Modal, Form } from 'react-bootstrap'; 
import SideNavBar from '../../components/side-nav/SIdeNav';
import { Breadcrumb, Card, Col, ListGroup, Row } from 'react-bootstrap';
import ContentContainer from './ContentContainer';
import { Calendar, momentLocalizer } from 'react-big-calendar'; 
import moment from 'moment';
import DashboardNavigation from '../../components/nav/DashNavigation';
import 'react-big-calendar/lib/css/react-big-calendar.css';
import PlansService from '../../services/Plans.service';
import PersonaInfosService from '../../services/PersonaInfos.service';
import env from '../../data/env';
import {Chart as ChartJs, 
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
} from 'chart.js'
import {Line} from 'react-chartjs-2'
import { FaStar, FaTrashAlt } from 'react-icons/fa';
import RevuewsService from '../../services/Revuews.service';
import Notiflix from 'notiflix';
import { Link } from 'react-router-dom';

ChartJs.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
)

function ForgettingCurve() {
  const localizer = momentLocalizer(moment);
  const [isExpanded, setIsExpanded] = useState(false);
  const [notifications, setNotifications] = useState([]);
  const [plans, setPlans] = useState([]);
  const [personal, setPersonl] = useState(null);
  const [selected, setSelected] = useState(null);

  const [events, setEvents] = useState([]);
  const [mems, setMems] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [reviewData, setReviewData] = useState({
    total: 0,
    points: 0,
    user: localStorage.getItem('username'),
    subject: '',
    activity: '',
  });

  const toggleModal = () => setShowModal(!showModal);


  const loadReviews = async () => {
    if(selected){
      await RevuewsService.getReviewsByUsernameSubject(selected.subject, localStorage.getItem('username')).then((data) => {
        setMems(data);
      })
    }
    
  }

  const handleReviewSubmit = async () => {
    // Handle review submission
    reviewData.subject = selected.subject;
    reviewData.activity = selected.type;
    await RevuewsService.createReview(reviewData).then((data) => {
      Notiflix.Report.success(
          'Success',
          "Revuew is submitted Successfully",
          'Okay',
      );
      // Close the modal
      toggleModal();
    })
    
  };

  const data = {
    labels: ['2022-01', '2022-02', '2022-03', '2022-04', '2022-05', '2022-06'],
    datasets: [
      {
        label: 'SPI Errors',
        data: [50, 45, 56, 55, 70, 65], 
        fill: false,
        borderColor: 'red', 
      },
      {
        label: 'High-Low',
        data: [30, 35, 40, 45, 50, 55], 
        fill: false,
        borderColor: 'blue', 
      },
      {
        label: 'Runoffs',
        data: [34, 25, 26, 35, 40, 51], 
        fill: false,
        borderColor: 'green', 
      },
    ],
  };

  // Chart options
  const options = {
    scales: {
      y: {
        min: 0,
        max: 150,
        ticks: {
          stepSize: 10,
        },
      },
    },
  };

  const handleSidebarToggle = (isVisible) => {
    setIsExpanded(isVisible);
  };

  const loadPlans = async () => {
    // await PlansService.getPlansByUser(localStorage.getItem('username')).then((data) => {
    //   const loadedEvents = data.flatMap(plan => {
    //     const activities = plan.activities.map(activity => {
    //       // Find the method object corresponding to the activity type
    //       const method = env.METHODS.find(method => method.type === activity.type);
    //       // Create the event object with color included
    //       return {
    //         id: activity._id,
    //         type: activity.type,
    //         subject: activity.subject,
    //         start: new Date(activity.startTime),
    //         end: moment(activity.startTime).add(activity.hours, 'hours').toDate(),
    //         color: method ? method.color : '#10eb60', // Default color if method not found
    //       };
    //     });
    //     return activities;
    //   });
    //   setEvents(loadedEvents);
    // });
  };

  const loadPersonal = async () => {
    await PersonaInfosService.getLatestPersonalInfoByUsername(localStorage.getItem('username')).then((data) => {
      setPersonl(data);
    });
  };

  const getColorByType = (type) => {
    const method = env.METHODS.find(method => method.type === type);
    return method ? method.color : '#FFFFFF'; 
  };

  useEffect(() => {
    loadPlans();
    loadPersonal();
    loadReviews();
  }, []);

  


  return (
    <>
      <SideNavBar onToggle={handleSidebarToggle}/>
      <ContentContainer isExpanded={isExpanded} children={
        <>
        <DashboardNavigation />
        <div className="fluid-container custom mt-4">
        <Row>
                            <Col lg={12}>
                                <Card className="shadow">
                                    <Card.Header>
                                        <h1>History Curves</h1>
                                    </Card.Header>
                                    <Card.Body>
                                    <span><Link to={'/'}>Home</Link> / History Curve</span>
                                    </Card.Body>
                                    
                                </Card>
                            </Col>
          </Row>
          <div className="row justify-content-center mt-4">
            <div className="col-md-8">
              <Card className='shadow'>
                <Card.Body>
                  <Card.Title>Time Series Analysis</Card.Title>
                  <Row className='custom-row'>
                    <Col className="col-md-4">
                      {/* Create Fogetting Curve HERE */}
                      <div className='chart-container' >
                          <Line data={data} />
                      </div>
                    </Col>
                    
                  </Row>
                </Card.Body>
              </Card>
            </div>
            <div className="col-md-4">
              <Card className='shadow custom-table'>
                <Card.Body>
                  <h5>Available Activiites</h5>

                  {events.map(activity => {
                    return (
                    <div key={activity._id} className="activity-container" style={{ backgroundColor: getColorByType(activity.type), cursor: 'pointer' }}
                    onClick={() => {
                      setSelected(activity);
                      setMems([])
                      loadReviews()
                    }}>
                      <div className='image'>
                        <img src={process.env.PUBLIC_URL + "/images/logo-em.png"} height={40} alt="logo" />
                      </div>
                      <div>
                        <h6>{activity.type} <small>({activity.subject})</small></h6>
                        <p>{moment(activity.start).format('YYYY-MM-DD HH:mm')}</p>
                      </div>
                      
                        {/* Add review icon */}
                        <Button variant="primary" onClick={() => {}}>
                          <FaStar onClick={() => {
                            setSelected(activity);
                            toggleModal()
                            }} style={{ cursor: 'pointer'}} />
                        </Button>
                       
                      
                    </div>
                    )})
                  }
                  
                </Card.Body>
              </Card>
            </div>
          </div>
        </div>
        <Modal show={showModal} onHide={toggleModal}>
        <Modal.Header closeButton>
          <Modal.Title>Write a Review</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formTotal">
              <Form.Label>Total:</Form.Label>
              <Form.Control type="number" placeholder="Enter total" value={reviewData.total} onChange={e => setReviewData({ ...reviewData, total: e.target.value })} />
            </Form.Group>
            <Form.Group controlId="formPoints">
              <Form.Label>Points:</Form.Label>
              <Form.Control type="number" max={reviewData.total} placeholder="Enter points" value={reviewData.points} onChange={e => setReviewData({ ...reviewData, points: e.target.value })} />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={toggleModal}>
            Close
          </Button>
          <Button variant="primary" onClick={() => handleReviewSubmit()}>
            Submit Review
          </Button>
        </Modal.Footer>
      </Modal>
        </>
      } />
      
    </>
  );
}

export default ForgettingCurve;
