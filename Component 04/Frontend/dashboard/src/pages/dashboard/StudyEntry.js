import React, { useEffect, useState } from 'react';
import { Button, Card, Col, Form, Modal, Row } from 'react-bootstrap'; 
import SideNavBar from '../../components/side-nav/SIdeNav';
import { Breadcrumb } from 'react-bootstrap';
import UsersService from '../../services/Users.service';
import CustomBreadcrumb from '../../components/bredcrumb/BreadCrumb';
import ContentContainer from './ContentContainer';
import moment from 'moment';
import DashboardNavigation from '../../components/nav/DashNavigation';
import { FaEdit, FaPlus, FaTrashAlt } from 'react-icons/fa';
import PlansService from '../../services/Plans.service';
import PersonaInfosService from '../../services/PersonaInfos.service';
import Notiflix from 'notiflix';
import env from '../../data/env';
import { Link } from 'react-router-dom';

function StudyEntry() {
  const [isExpanded, setIsExpanded] = useState(false);
  const [showPlanModal, setShowPlanModal] = useState(false);
  const [showActivityModal, setShowActivityModal] = useState(false);
  const [plans, setPlans] = useState([]);
  const [personal, setPersonl] = useState(null);
  const [selectedPlan, setSelectedPlan] = useState(null);
  const [selectedActs, setSelectedActs] = useState([]);
  const [newPlan, setNewPlan] = useState({ title: '', description: '', activities: [], user: localStorage.getItem('username') });
  const [newActivity, setNewActivity] = useState({ type: '', subject: '', startDate: '', startTime: '', hours: '' });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);

  const loadStudyFactor = async (personal) => {
    if(!personal) return;
      try {
          const response = await fetch(env.ML_URL+'/factorPrediction', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  gender: personal.gender=='Male'?1:2, 
                  sleep: personal.sleepHours,
                  weekend: 0,
                  age: personal.age
              })
          });

          if (!response.ok) {
              throw new Error('Failed to fetch prediction');
          }

          const data = await response.json();
          setPrediction(data.prediction);
          setError(null);
      } catch (error) {
          setError(error.message);
          setPrediction(null);
      }
  };

  const handleSidebarToggle = (isVisible) => {
    setIsExpanded(isVisible);
  };

  const loadPlans = async () => {
    await PlansService.getPlansByUser(localStorage.getItem('username')).then((data) => {
      setPlans(data);
    });
  };

  const loadPersonal = async () => {
    await PersonaInfosService.getLatestPersonalInfoByUsername(localStorage.getItem('username')).then((data) => {
      setPersonl(data);
      
      loadStudyFactor(data)
    });
  };

  const generateAIPlan = () => {
    // Check if personal data is available
    if (!personal || !personal.favorite) {
        Notiflix.Notify.failure('Personal data or favorite subjects not available.');
        return;
    }

    const shuffledSubjects = shuffleArray(personal.favorite);
    const activityDuration = 1;
    const currentDate = moment();

    if(!(prediction&&prediction.length>0)) return;
    
    const predictionHours = Math.round(prediction[0]);
    const numSlots = Math.min(predictionHours, personal.favorite.length);
    const newActivities = [];

    // Generate activities for each slot
    for (let i = 0; i < numSlots; i++) {
        const type = ['Study', 'Reading', 'Audio Learning', 'Watching Videos'];
        const randomType = type[Math.floor(Math.random() * type.length)];
        const subject = shuffledSubjects[i];
        const startTime = currentDate.clone().add(i, 'hour').format('HH:mm');

        // Format start time
        const dateTime = moment(currentDate.format('YYYY-MM-DD') + ' ' + startTime, 'YYYY-MM-DD HH:mm');
        const formattedStartTime = dateTime.format('YYYY-MM-DDTHH:mm:ss');
        newActivities.push({
            type: randomType,
            subject: subject,
            startDate: currentDate.format('YYYY-MM-DD'),
            startTime: formattedStartTime,
            hours: activityDuration
        });
    }

    const remainingSlots = predictionHours - numSlots;
    if (remainingSlots > 0) {
        const secondaryTypes = ['Memorizing', 'Mind Mapping', 'Summarizing', 'Problem Solving', 'Drawing Diagrams'];
        for (let i = 0; i < remainingSlots; i++) {
            const randomSecondaryType = secondaryTypes[Math.floor(Math.random() * secondaryTypes.length)];
            const subject = shuffledSubjects[i]; 
            const startTime = currentDate.clone().add(numSlots + i, 'hour').format('HH:mm');
            const dateTime = moment(currentDate.format('YYYY-MM-DD') + ' ' + startTime, 'YYYY-MM-DD HH:mm');
            const formattedStartTime = dateTime.format('YYYY-MM-DDTHH:mm:ss');
            newActivities.push({
                type: randomSecondaryType,
                subject: subject,
                startDate: currentDate.format('YYYY-MM-DD'),
                startTime: formattedStartTime,
                hours: activityDuration
            });
        }
    }

    const remainingSubjects = personal.subjects.filter(subject => !personal.favorite.includes(subject));
    const last = remainingSubjects[Math.floor(Math.random() * remainingSubjects.length)];
    const startTime2 = currentDate.clone().add( remainingSlots+1, 'hour').format('HH:mm');
    const dateTime2 = moment(currentDate.format('YYYY-MM-DD') + ' ' + startTime2, 'YYYY-MM-DD HH:mm');
    const formattedStartTime2 = dateTime2.format('YYYY-MM-DDTHH:mm:ss');
    newActivities.push({
            type: 'Study',
            subject: last,
            startDate: currentDate.format('YYYY-MM-DD'),
            startTime: formattedStartTime2,
            hours: 1
    })

    // Update the selected activities state
    setSelectedActs(newActivities);
};



  useEffect(() => {
    loadPlans();
    loadPersonal();
    fetchActivities();
  }, []);

  

  const fetchActivities = async () => {
    // Fetch activities from backend for selected plan
    // setActivities(activitiesFromBackend);
  };

  const handlePlanSubmit = async () => {
    // Submit new plan to backend
    // Add newly created plan to plans state
    setPlans([...plans, newPlan]);
    setShowPlanModal(false);
    setNewPlan({title:'', description: '', activities: []})
  };

  const handleUpdatePlan = async (event, plan) => {
    event.stopPropagation();
    Notiflix.Confirm.show(
        'Confirmation',
        'Are you sure you want to Update this Plan?',
        'Yes',
        'No',
        async () => {
            const existingActivities = selectedActs.map(activity => ({
                type: activity.type,
                subject: activity.subject,
                startTime: activity.startTime,
                hours: activity.hours
            }));

            const newActivities = newPlan.activities.map(activity => ({
                type: activity.type,
                subject: activity.subject,
                startTime: activity.startTime,
                hours: activity.hours
            }));

            // Filter out any activities that are already in the plan
            const uniqueNewActivities = newActivities.filter(newActivity =>
                !existingActivities.some(existingActivity =>
                    existingActivity.type === newActivity.type && existingActivity.subject === newActivity.subject
                )
            );

            // Combine unique new activities with existing activities
            const updatedActivities = [...existingActivities, ...uniqueNewActivities];

            const updatedPlan = { ...plan, activities: updatedActivities };
            
            await PlansService.createPlan(updatedPlan).then(() => {
                Notiflix.Report.success(
                    'Success',
                    "Plan Updated Successfully",
                    'Okay',
                );
            });
            setInterval(4000, () => window.location.reload());
        }
    );
};

const shuffleArray = (array) => {
  const shuffledArray = [...array];
  for (let i = shuffledArray.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffledArray[i], shuffledArray[j]] = [shuffledArray[j], shuffledArray[i]];
  }
  return shuffledArray;
};



  
  const handleActivitySubmit = async () => {
    // Combine date and time into a single timestamp
      const dateTime = moment(newActivity.startDate + ' ' + newActivity.startTime, 'YYYY-MM-DD HH:mm');
      const formattedStartTime = dateTime.format('YYYY-MM-DDTHH:mm:ss');
      
      // Submit new activity to backend
      // Add newly created activity to activities state
      setSelectedActs([...selectedActs, { ...newActivity, startTime: formattedStartTime }]);
      setSelectedPlan(prevPlan => {
        const updatedPlan = { ...prevPlan };
        updatedPlan.activities.push({ ...newActivity, startTime: formattedStartTime });
        return updatedPlan;
      });
      setShowActivityModal(false);
  };

  const handleDeleteActivity = async (type, subject) => {
    // Delete activity from backend
    // Remove activity from activities state
    // setSelectedActs(prevActivities => prevActivities.filter(activity => activity._id !== type));
    setSelectedPlan(prevPlan => {
      const updatedPlan = { ...prevPlan };
      updatedPlan.activities = updatedPlan.activities.filter(activity => activity.type !== type && activity.subject !== subject);
      return updatedPlan;
    });

    // Update selectedActs state
    setSelectedActs(prevActs => prevActs.filter(activity => activity.type !== type && activity.subject !== subject));

    // Update plans array item in correct index
    const updatedPlans = plans.map(plan => {
      if (plan.title === selectedPlan.title) {
        return {
          ...plan,
          activities: plan.activities.filter(activity => activity.type !== type && activity.subject !== subject)
        };
      }
      return plan;
    });

    setPlans(updatedPlans);
  };

  const getColorByType = (type) => {
    const method = env.METHODS.find(method => method.type === type);
    return method ? method.color : '#FFFFFF'; 
  };

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
                                        <h1>Study Entry</h1>
                                    </Card.Header>
                                    <Card.Body>
                                    <span><Link to={'/'}>Home</Link> / Study Entry</span>
                                    </Card.Body>
                                    
                                </Card>
                            </Col>
          </Row>
            <div className="row justify-content-center mt-4">
              <div className="col-md-6">
                <Card className='shadow custom-table'>
                  <Card.Body>
                    <Card.Title>Your Study Plans</Card.Title>
                    <div className="add-plan-container" onClick={() => setShowPlanModal(true)}>
                      <span>Add a Study Plan</span> <FaPlus size={30} />
                    </div>
                    {plans.map((plan,index) => (
                      <div style={{display:'flex', justifyContent:'space-between', flexWrap: 'wrap', width: '100%'}}>
                        <div key={index} className="plan-container" style={{flex:1, display:'flex', justifyContent:'space-between', alignItems: 'center'}} onClick={() => {
                          if(!selectedPlan||(selectedPlan && selectedPlan.title !== plan.title)){
                            setSelectedPlan(plan); 
                            setSelectedActs(plan.activities);
                          } 
                          }}>
                            <div>
                            <h5>{plan.title}</h5>
                            <p>{plan.description}</p>
                            </div>
                            
                            <FaEdit className="update-icon" style={{fontSize: 20}} onClick={(event) => handleUpdatePlan(event, plan)} />
                        </div>
                        
                      </div>
                    ))}
                    
                  </Card.Body>
                </Card>
              </div>
              <div className="col-md-6">
                <Card className='shadow custom-table'>
                  <Card.Body>
                    <h5>Activities</h5>
                    {selectedActs && selectedActs.length > 0 ? (
                      <div>
                        {selectedPlan && (<div className='custom-flex'>
                          <div className="add-plan-container" onClick={() => setShowActivityModal(true)}>
                            <span>Add Activities</span><FaPlus size={30} />
                          </div>
                          <div className="add-plan-container" onClick={() => generateAIPlan()}>
                            <span>Add Using AI</span><FaPlus size={30} />
                          </div>
                        </div>
                        )}
                      {selectedActs.map(activity => {

                        return (
                        <div key={activity._id} className="activity-container" style={{ backgroundColor: getColorByType(activity.type) }}>
                          <div className='image'>
                            <img src={process.env.PUBLIC_URL + "/images/logo-em.png"} height={40} alt="logo" />
                          </div>
                          <div>
                            <h6>{activity.type}</h6>
                            <p>{activity.subject}</p>
                          </div>
                          <Button variant="danger" onClick={() => handleDeleteActivity(activity.type, activity.subject)}>
                            <FaTrashAlt />
                          </Button>
                        </div>
                      )})
                      }</div>) : (
                      <div className="empty-container">
                        <p>Crate and Select PLAN to add Activitird.</p>
                        {selectedPlan && (<div className='custom-flex'>
                          <div className="add-plan-container" onClick={() => setShowActivityModal(true)}>
                            <span>Add Activities</span><FaPlus size={30} />
                          </div>
                          <div className="add-plan-container" onClick={() => generateAIPlan()}>
                            <span>Add Using AI</span><FaPlus size={30} />
                          </div>
                        </div>
                        )}
                      </div>
                    )}
                  </Card.Body>
                </Card>
              </div>

            </div>
          </div>
        </>
      } />
      
      {/* Plan Modal */}
      <Modal show={showPlanModal} onHide={() => setShowPlanModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Create New Plan</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formPlanTitle">
              <Form.Label>Title</Form.Label>
              <Form.Control 
                type="text" 
                placeholder="Enter title" 
                value={newPlan.title} 
                onChange={(e) => setNewPlan({ ...newPlan, title: e.target.value })} 
              />
            </Form.Group>
            <Form.Group controlId="formPlanDescription">
              <Form.Label>Description</Form.Label>
              <Form.Control 
                as="textarea" 
                rows={3} 
                placeholder="Enter description" 
                value={newPlan.description} 
                onChange={(e) => setNewPlan({ ...newPlan, description: e.target.value })} 
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowPlanModal(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={handlePlanSubmit}>
            Create Plan
          </Button>
        </Modal.Footer>
      </Modal>

      {/* Activity Modal */}
      <Modal show={showActivityModal} onHide={() => setShowActivityModal(false)}>
        <Modal.Header closeButton>
          <Modal.Title>Add New Activity</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form>
            <Form.Group controlId="formActivityType">
              <Form.Label>Type</Form.Label>
              <Form.Control 
                as="select" 
                value={newActivity.type} 
                onChange={(e) => setNewActivity({ ...newActivity, type: e.target.value })} 
              >
                <option value="">Select Type</option>
                { env.METHODS.map((item) => <option value={item.type}>{item.type}</option>)}
                {/* Add more options as needed */}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="formActivitySubject">
              <Form.Label>Subject</Form.Label>
              <Form.Control 
                as="select" 
                value={newActivity.subject} 
                onChange={(e) => setNewActivity({ ...newActivity, subject: e.target.value })} 
              >
                <option value="">Select Subject</option>
                {personal&& personal.subjects.length>0 && personal.subjects.map((item) => <option value={item}>{item}</option>)}
                {!personal&& env.SUBJECTS.map((item) => <option value={item}>{item}</option>)}
                {/* Add more options as needed */}
              </Form.Control>
            </Form.Group>
            <Form.Group controlId="formActivityStartDate">
              <Form.Label>Start Date</Form.Label>
              <Form.Control 
                type="date" 
                value={newActivity.startDate} 
                onChange={(e) => setNewActivity({ ...newActivity, startDate: e.target.value })} 
              />
            </Form.Group>
            <Form.Group controlId="formActivityStartTime">
              <Form.Label>Start Time</Form.Label>
              <Form.Control 
                type="time" 
                value={newActivity.startTime} 
                onChange={(e) => setNewActivity({ ...newActivity, startTime: e.target.value })} 
              />
            </Form.Group>
            
            <Form.Group controlId="formActivityHours">
              <Form.Label>Hours</Form.Label>
              <Form.Control 
                type="number" 
                min="1" 
                max="6" 
                value={newActivity.hours} 
                onChange={(e) => setNewActivity({ ...newActivity, hours: e.target.value })} 
              />
            </Form.Group>
          </Form>
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => setShowActivityModal(false)}>
            Close
          </Button>
          <Button variant="primary" onClick={handleActivitySubmit}>
            Add Activity
          </Button>
        </Modal.Footer>
      </Modal>

    </>
  );
}

export default StudyEntry;
