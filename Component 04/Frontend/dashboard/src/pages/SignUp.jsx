import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import Notiflix from 'notiflix';
import usersService from '../services/Users.service';
import env from '../data/env';
import EventEmitter from '../utils/EventEmitter';
import Footer from '../components/footer/Footer';


const Signup = () => {
  const navigate = useNavigate();
  const [userRole, setUserRole] = useState('Student');
  const [qualifications, setQualifications] = useState([]);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [email, setEmail] = useState('');
  const [avatar, setAvatar] = useState(null);

  const handleUserRoleChange = (e) => {
    setUserRole(e.target.value);
  };



  const handleSignUp = async () => {
    console.log(username)
      // if ((userRole === '')) {
      //   Notiflix.Report.failure(
      //     'Registration Failed',
      //     'UserRole is required for Registration',
      //     'Okay',
      //   );
      //   return;
      // }
      if ((username === '')) {
        Notiflix.Report.failure(
          'Registration Failed',
          'Username required for Registration',
          'Okay',
        );
        return;
      }
      
      if ((email === '')) {
        Notiflix.Report.failure(
          'Registration Failed',
          'Email and Contact number required for Registration',
          'Okay',
        );
        return;
      }
      if ((password === '')) {
        Notiflix.Report.failure(
          'Registration Failed',
          'Password can not be empty',
          'Okay',
        );
        return;
      }
      if (!(password === confirmPassword)) {
        Notiflix.Report.failure(
          'Registration Failed',
          'Password doesn\'t match with confirmation password',
          'Okay',
        );
        return;
      }

      // Cloudinary Upload
      const formData = new FormData();
      formData.append('file', avatar);
      formData.append('upload_preset', 'gtnnidje'); 

      try {
        const response = await fetch('https://api.cloudinary.com/v1_1/dkox7lwxe/image/upload', {
          method: 'POST',
          body: formData,
        });

        const cloudinaryData = await response.json();

        if (userRole === 'Student') {
          let obj = {
            username: username,
            email: email,
            password: password,
            role: userRole,
            avatar: cloudinaryData.secure_url,
          };

          await usersService.addUser(obj).then(() => {
            Notiflix.Report.success(
              'Success',
              'Registration Successful as a Student',
              'Okay',
            );
                localStorage.setItem('username', username);
                localStorage.setItem('role', userRole);
                localStorage.setItem('avatar', 'https://cdn-icons-png.flaticon.com/512/1533/1533506.png');
                EventEmitter.emit("loginCompleted", {logged: true});
            navigate('/sign-in');
            // window.location.reload();
          });
        } 

      } catch (error) {
        console.error('Error uploading image to Cloudinary:', error);
        Notiflix.Notify.failure('Error uploading image. Please try again.');
      }
    
  };

  useEffect(() => {
    let listner = EventEmitter.addListener("registerCompleted", () => {
      Notiflix.Report.success(
        'Success',
        'Registration Successful as Garbage Collector',
        'Okay',
      );
      navigate('/survey');
    });
    let listner2 = EventEmitter.addListener("registerFailed", () => {
      Notiflix.Notify.failure('Provided email is already being using.');
    });

    return () => {
      listner.remove();
      listner2.remove();
    }
  }, [])

  return (
    <>
    <div className='form-body'>
    <div className="max-w-md mx-auto mt-8 p-6 rounded-md shadow-md container form-container">
      <div className='image-container text-center'>
              <img src={process.env.PUBLIC_URL+'/images/logo-em.png'} height={60} alt='background' />
              <span className='custom-title'>MASS</span>
      </div>
      <br/><br/>
      <h1 className="text-3xl font-semibold mb-6">Sign Up</h1>
      <label className="block text-gray-700 text-sm font-bold mb-2">
          Create Your Free Account
      </label>

      {/* <div className="mb-4">
        <br/> 
        <select
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          onChange={handleUserRoleChange}
        >
          <option value="">Select User Role</option>
          <option value="user">Citizen</option>
          <option value="garbage collector">Garbage Collector</option>
        </select>
      </div> */}

      <div className="mb-4">
        <input
          type="text"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          value={username}
          placeholder='Username'
          onChange={(e) => setUsername(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <input
          type="email"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          value={email}
          placeholder='Email'
          onChange={(e) => setEmail(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <input
          type="password"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          value={password}
          placeholder='Password'
          onChange={(e) => setPassword(e.target.value)}
        />
      </div>

      <div className="mb-4">
        <input
          type="password"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          value={confirmPassword}
          placeholder='Retype Password'
          onChange={(e) => setConfirmPassword(e.target.value)}
        />
      </div>

      <div className="mb-4">
        {/* <label className="block text-gray-700 text-sm font-bold mb-2">
          Avatar (Upload)
        </label> */}
        <input
          type="file"
          className="w-full px-4 py-2 border rounded-md focus:outline-none focus:border-blue-500"
          onChange={(e) => setAvatar(e.target.files[0])}
        />
      </div>

      {/* Submit Button */}
      <div className='text-center'>
        <button
          className="custom-button"
          onClick={handleSignUp}
        >
          Sign Up
        </button>
      </div>
      
      <p className="mt-4 text-center text-gray-600">
        Don't have an account?{' '}
        <Link to="/sign-in" className="custom-link">
          Sign In
        </Link>
      </p>
    </div>
    </div>
    <Footer />
    </>
  );
};

export default Signup;
