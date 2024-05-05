import React, { useEffect, useState } from 'react';
import { Breadcrumb, Container, Row, Col, Card, Table } from 'react-bootstrap';
import { Link } from 'react-router-dom';
import SideNavBar from '../../components/side-nav/SIdeNav';
import ContentContainer from './ContentContainer';
import NotificationsService from '../../services/Notifications.service';
import Notiflix from 'notiflix';
import env from '../../data/env';
import PlansService from '../../services/Plans.service';
import DashboardNavigation from '../../components/nav/DashNavigation';
import { AiFillCheckSquare, AiFillMessage, AiFillRedEnvelope, AiOutlineBarChart, AiOutlineUser } from 'react-icons/ai';
import moment from 'moment';

function DashboardHome() {
    const [isExpanded, setIsExpanded] = useState(false);
    const [notifications, setNotifications] = useState([]);
    const [plans, setPlans] = useState([]);
    const [events, setEvents] = useState([]);

    const loadNotifications = async () => {
        await NotificationsService.getNotifications().then((data) => {
            setNotifications(data);
        });
    };

    const loadPlans = async () => {
        await PlansService.getPlansByUser(localStorage.getItem('username')).then((data) => {
            setPlans(data);
        });
    };

    const loadEvents = async () => {
        // await PlansService.getPlansByUser(localStorage.getItem('username')).then((data) => {
        //   const loadedEvents = data.flatMap(plan => {
        //     const activities = plan.activities.map(activity => {
        //       // Find the method object corresponding to the activity type
        //       const method = env.METHODS.find(method => method.type === activity.type);
        //       // Create the event object with color included
        //       return {
        //         id: activity._id,
        //         title: activity.type + ' - ' + activity.subject,
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

    const handleSidebarToggle = (isVisible) => {
        setIsExpanded(isVisible);
    };

    useEffect(() => {
        loadNotifications();
        loadPlans();
        loadEvents();
    }, []);

    return (
        <div>
            <SideNavBar onToggle={handleSidebarToggle} />
            <ContentContainer isExpanded={isExpanded} children={
                <>
                <DashboardNavigation/>
                <div className="fluid-container custom mt-4">
                    <Container fluid className="p-0">
                        <Row>
                            <Col lg={12}>
                                <Card className="shadow">
                                    <Card.Header>
                                        <h1>Dashboard</h1>
                                    </Card.Header>
                                    <Card.Body>
                                    <span><Link to={'/'}>Home</Link> / Dashboard</span>
                                    </Card.Body>
                                    
                                </Card>
                            </Col>
                        </Row>
                        <Row className="mt-4">
                            {events&&<Col lg={4}>
                                <Card className="shadow">
                                    <Card.Body>
                                        <div className="d-flex justify-content-between align-items-center">
                                            <div className="card-number">{events.length}</div>
                                            <div className="card-icon"><AiFillCheckSquare /></div>
                                        </div>
                                        <p>User Activiites</p>
                                        <div className="card-bar primary"></div>
                                    </Card.Body>
                                </Card>
                            </Col>}
                            {plans&&<Col lg={4}>
                                <Card className="shadow">
                                    <Card.Body>
                                        <div className="d-flex justify-content-between align-items-center">
                                            <div className="card-number">{plans.length}</div>
                                            <div className="card-icon"><AiOutlineBarChart /></div>
                                        </div>
                                        <p>Created Plans</p>
                                        <div className="card-bar warning"></div>
                                    </Card.Body>
                                </Card>
                            </Col>}
                            <Col lg={4}>
                                <Card className="shadow">
                                    <Card.Body>
                                        <div className="d-flex justify-content-between align-items-center">
                                            <div className="card-number">10</div>
                                            <div className="card-icon"><AiFillMessage /></div>
                                        </div>
                                        <p>User Achievements</p>
                                        <div className="card-bar success"></div>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                        <Row className="mt-4">
                            <Col lg={12}>
                                <Card className="shadow custom-table">
                                    <Card.Body>
                                        <Table responsive bordered>
                                            <thead>
                                                <tr>
                                                    <th>#</th>
                                                    <th>Title</th>
                                                    <th>Start Date</th>
                                                    <th>End Date</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {events.length>0 && events.map((plan, index) => (
                                                    <tr key={index}>
                                                        <td>{index + 1}</td>
                                                        <td>{plan.title}</td>
                                                        <td>{moment(plan.start).format('YYYY-MM-DD HH:mm')}</td>
                                                        <td>{moment(plan.end).format('YYYY-MM-DD HH:mm')}</td>
                                                    </tr>
                                                ))}
                                            </tbody>
                                        </Table>
                                    </Card.Body>
                                </Card>
                            </Col>
                        </Row>
                    </Container>
                </div>
                </>
            } />
        </div>
    );
}

export default DashboardHome;
