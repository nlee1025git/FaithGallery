const express = require('express');
const cors = require('cors');
const app = express();
const port = 3001;

app.use(cors({
  origin: 'https://momentssnap.com', // Restrict to your domain
}));
app.use(express.json());

app.get('/api', (req, res) => {
  res.json({ message: 'Hello from the EC2 backend!' });
});

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
