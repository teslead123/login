import React from 'react';
// import './Dashboard.css';

function Dashboard() {

    const backgroundStyle={
      background: `url(${process.env.PUBLIC_URL}/images/dashboard1.jpg) no-repeat center center fixed`,
    //   backgroundSize: 'cover',
    //   backgroundRepeat: 'no-repeat',
    //   backgroundAttachment: 'fixed',
    //   backgroundPosition: 'center',
    //   margin: 0,
    //   height: '100vh',
    backgroundSize: 'cover',
    margin: 0,
    minHeight: '100vh', // Use minHeight instead of height in case content grows
    overflow: 'hidden',
    };
  return (


    // <div className="dashboard-background">
      
     <div style={backgroundStyle}>
        <div style={{height:'90vh'}}>
      <h1>Hi</h1>
      <div>
        <button 
          onClick={() => window.location.href = 'http://127.0.0.1:8000/login/'}
        >
          Login 
        </button>

        <button 
          style={{ marginLeft: '10px' }}
          onClick={() => window.location.href = 'http://127.0.0.1:8000/register/'}
        >
          Register 
        </button>
        </div>
      </div>
    </div>
    // </div>
  );
}

export default Dashboard;
