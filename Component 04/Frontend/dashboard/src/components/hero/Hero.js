import React from 'react';
import { Container, Row, Col, Button } from 'react-bootstrap';
import './hero.css';
import { Link, useNavigate } from 'react-router-dom';

const HeroContainer = () => {
  const navigate = useNavigate();
  return (
    <div className="hero-container">
      <Container fluid>
        <Row className="align-items-center"> {/* Vertically center content */}
          <Col className="text-center custom-frame">
            <h1>MAS<br></br>Production Quality Monitoring</h1>
            <p>MAS Holdings is a Sri Lankan apparel manufacturer. The company was founded in 1987 by Mahesh, Sharad and Ajay Amalean. MAS Holdings began as an underwear manufacturer and later diversified into sportswear, performance wear and swimwear.</p>
            <div className="button-group">
              <button className="custom-button light mr-3" onClick={() => {
                navigate('/map');
                window.location.reload();
              }}>Explore Our Features</button>
              <Link to={'/sign-in'}><button className="custom-button primary">Get Stored for Free</button></Link>
            </div>
            <br/>
            <div className='image-container'>
              <img src={process.env.PUBLIC_URL+'/images/bg.png'} alt='background' />
            </div>
          </Col>
        </Row>
      </Container>
    </div>
  );
};

export default HeroContainer;
