import React, { useEffect, useState } from 'react';
import nextbillion, { NBMap } from '@nbai/nbmap-gl'
const LocationTracker = () => {

    let origin,stop;
    const apiKey = nextbillion.setApiKey('b98e9dd2f9414231bae19340b76feff0')
    
  const[currLocation,setcurrLocation]=useState({})

  const school = [
    {
    latitude:10.0331373,
    longitude:76.2723346,
    origin:10.0331373+" "+76.2723346
    }
  ]


  useEffect(()=>{
    geoLocation();
    nextbillion.apiKey = apiKey;
  },[]);
    const geoLocation=()=>{
        navigator.geolocation.getCurrentPosition((position)=>{
            console.log(position)
            const {latitude,longitude} = position.coords
            setcurrLocation({ latitude,longitude })
            stop = latitude+" "+longitude
        })
    }

   const getDistance =()=>{
    const resultElement=document.getElementById("result")
    
    fetch(`https://api.nextbillion.io/distancematrix/json?origins=${origin}&destinations=${stop}&mode=4w&key=${apiKey}`)
    .then(resp=>resp.json())
    .then(data=>{
        console.log(data)
        data.rows.forEach(function (row) {
        row.elements.forEach(function (element) {
          resultElement.style.display = "block";
          resultElement.innerText = "Distance: " + ((element.distance.value > 999) ? (element.distance.value / 1000) + " KM" : element.distance.value + " M") + " | Duration: " + secondsToHms(element.duration.value)
        });
      })
    })
}

const secondsToHms = (d) => {
    d = Number(d);
    const h = Math.floor(d / 3600);
    const m = Math.floor(d % 3600 / 60);
    const s = Math.floor(d % 3600 % 60);

    const hDisplay = h > 0 ? h + (h === 1 ? " hour, " : " hours, ") : "";
    const mDisplay = m > 0 ? m + (m === 1 ? " minute, " : " minutes, ") : "";
    const sDisplay = s > 0 ? s + (s === 1 ? " second" : " seconds") : "";
    return hDisplay + mDisplay + sDisplay;
  }


    return (
        <div>
        <div id="map" style={{ width: '100%', height: '100px' }}></div>
        <h1>latitude:{currLocation.latitude}</h1>
        <h1>longitude:{currLocation.longitude}</h1>


        {school.map(school=>(
            <div>
            <h1>latitude:{school.latitude}</h1>
            <h1>longitude:{school.longitude}</h1>
            </div>
        ))}
        
            <button onClick={getDistance}>Get distance</button>
            <div id='result' >Result:</div>
        </div>

    );
};

export default LocationTracker;