'use client';
import { useEffect, useState } from 'react';

export default function Home() {
  const [message, setMessage] = useState('Loading...');
  const [uploadMessage, setUploadMessage] = useState('');

  useEffect(() => {
    //fetch('http://localhost:3001/api')  // Corrected to the correct backend port
    fetch('/api')
    .then((response) => response.json())
      .then((data) => setMessage(data.message))
      .catch((error) => {
        console.error('Fetch error:', error);
        setMessage('Error connecting to backend');
      });
  }, []);

  const handleSubmit = (event) => {
    event.preventDefault(); // Prevent default form submission (no page reload)

    const formData = new FormData(event.target); // Collect form data

    // Send the form data to the Flask backend asynchronously
    fetch('/upload', { 
    //fetch('http://localhost:3001/upload', {  // Corrected to the correct backend port

      method: 'POST',
      body: formData
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        if (data.message) {
          setUploadMessage(data.message); // Success message
          event.target.reset(); // Reset form inputs
        } else if (data.error) {
          setUploadMessage(`Error: ${data.error}`); // Error message
        }
      })
      .catch((error) => {
        console.error('Upload error:', error);
        setUploadMessage('Error uploading file');
      });
  };

  return (
    <div>
      <head>
        <title>Upload Photos</title>
      </head>

      <main>
        <h1>Upload Photo?</h1>
        <p>{message}</p>

        {/* Form for file upload */}
        <form onSubmit={handleSubmit} encType="multipart/form-data">
          <label htmlFor="name">Name:</label>
          <input type="text" id="name" name="name" required />
          <br />
          <br />

          <label htmlFor="file">Choose file:</label>
          <input type="file" id="file" name="file" required />
          <br />
          <br />

          <input type="submit" value="Upload" />
        </form>

        {/* Display upload success or error message */}
        <p>{uploadMessage}</p>

        <h2>Search Photos</h2>
        <form action="/search" method="get">
          <label htmlFor="search_name">Search by name:</label>
          <input type="text" id="search_name" name="name" />
          <input type="submit" value="Search" />
        </form>
      </main>
    </div>
  );
}
