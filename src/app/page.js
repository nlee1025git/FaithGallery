'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('Loading...');

  useEffect(() => {
    fetch('/api')  // Relative URL, should resolve to https://myaddress.com/api
      .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error('Fetch error:', error);
        setMessage('Error connecting to backend');
      });
  }, []);

  return (
    <div>
    <head>
      <title>Upload Photo</title>
    </head>

    <main>
    <h1>Upload Photo</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required/><br/><br/>
        
        <label for="file">Choose file:</label>
        <input type="file" id="file" name="file" required/><br/><br/>
        
        <input type="submit" value="Upload"/>
    </form>
    
    <h2>Search Photos</h2>
    <form action="/search" method="get">
        <label for="search_name">Search by name:</label>
        <input type="text" id="search_name" name="name"/>
        <input type="submit" value="Search"/>
    </form>







</main>
</div>    


  );
}
