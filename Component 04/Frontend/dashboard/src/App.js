import './App.css';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Signup from './pages/SignUp';
import SignIn from './pages/SignIn';
import Home from './pages/Home';
import Profile from './pages/dashboard/Profile';
import UsersManagement from './pages/dashboard/UsersManagement';
import Notifications from './pages/dashboard/Notifications';
import AboutUs from './pages/AboutUs';
import PageNotFound from './pages/PageNotFound';
import SurveyForm from './pages/SurveyForm';
import StudyPlan from './pages/dashboard/Calendar';
import StudyEntry from './pages/dashboard/StudyEntry';
import ForgettingCurve from './pages/dashboard/ForgettingCurve';
import DashboardHome from './pages/dashboard/DashboardHome';
import ProgressTracking from './pages/dashboard/ProgressTracking';
import FAQContainer from './pages/FAQs';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route element={<Home/>} path='/' />
          <Route element={<FAQContainer/>} path='/faq' />
          <Route element={<AboutUs/>} path='/aboutus' />
          <Route element={<Signup/>} path='/sign-up' />
          <Route element={<SignIn/>} path='/sign-in' />
          <Route element={<SurveyForm/>} path='/survey' />
          <Route  path='/dashboard' >
            <Route element={<DashboardHome/>} path='' />
            <Route element={<Profile/>} path='profile' />
            <Route element={<UsersManagement/>} path='users-management' />
            <Route element={<ProgressTracking/>} path='progress' />
            <Route element={<StudyPlan/>} path='calendar' />
            <Route element={<StudyEntry/>} path='study-entry' />
            <Route element={<ForgettingCurve/>} path='curve' />
            <Route element={<Notifications/>} path='notifications' />
          </Route>
          <Route path='*' element={<PageNotFound />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
