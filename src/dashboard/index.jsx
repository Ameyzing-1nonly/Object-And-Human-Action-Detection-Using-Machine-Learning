import React from 'react'
import Dashboard from './components/Dashboard'

function dashboadr() {
  return (
    <div className='p-20 md:px-20 lg:px-32'>
      <h2 className='font-bold text-3xl'>Object detection and Human Action Recognition</h2>
      <p>Select What want to do</p>
      <div className=''>
        <Dashboard/>
      </div>
    </div>
  )
}

export default dashboadr