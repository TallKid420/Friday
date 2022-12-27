const express = require('express');
var app = express()
const path = require('path'); // For working with file paths

const port = 80;

app.get('/image/:imageFile', (req, res, next) => {
  const imageFile = req.params.imageFile;
  res.sendFile(path.join(__dirname, imageFile), (err) => {
    if (err) {
      res.status(404).sendFile(path.join(__dirname, '404.html'));
      next(err);
    }
  });
});

app.get('/', (req, res) => {
  const imageFile = 'pexels-athena-2582937.jpg'
  res.sendFile(path.join(__dirname, 'homepage.html'))
});

app.use((req, res) => {
  // Use the `sendFile` method to send the 404.html file as the response
  res.status(404).sendFile(path.join(__dirname, '404.html'));
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});